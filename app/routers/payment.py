from fastapi import APIRouter, HTTPException, Depends, Form
from app.models.banner_db import PaymentManager, UserManager
from app.config import settings
from app.security.jwt import get_current_user
import hashlib
import string
import requests
import time

import re

# SECRET_XOR_KEY for payment ID obfuscation
SECRET_XOR_KEY = 0x5EAFB

def encode_payment_id(p_id: int) -> str:
    return hex(p_id ^ SECRET_XOR_KEY)[2:].upper()

def decode_payment_id(hex_str: str) -> int:
    try:
        return int(hex_str, 16) ^ SECRET_XOR_KEY
    except:
        return None

router = APIRouter(prefix="/payment", tags=["payment"])

def get_payment_manager():
    manager = PaymentManager()
    try:
        yield manager
    finally:
        manager.close()

def get_user_manager():
    manager = UserManager()
    try:
        yield manager
    finally:
        manager.close()

@router.get("/packages")
async def get_packages(payment_manager: PaymentManager = Depends(get_payment_manager)):
    return payment_manager.get_packages()

@router.post("/create")
async def create_payment(
    package_id: int = Form(...),
    current_user: dict = Depends(get_current_user),
    payment_manager: PaymentManager = Depends(get_payment_manager)
):
    user_id = current_user['id']
    
    packages = payment_manager.get_packages()
    package = next((p for p in packages if p['id'] == package_id), None)
    
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
        
    # Tạo record payment trước để có ID
    # Lưu ý: payment_code ban đầu để tạm, sẽ update sau khi có ID
    payment_id = payment_manager.create_payment(
        user_id, 
        package_id, 
        package['amount_vnd'], 
        package['tokens'], 
        "PENDING" 
    )
    
    # Sinh mã nội dung chuyển khoản theo thuật toán XOR
    hex_id = encode_payment_id(payment_id)
    payment_code = f"{settings.NAME_WEB}NAPTOKEN{hex_id}"
    
    # Update payment_code vào DB
    sql = "UPDATE payments SET payment_code = ? WHERE id = ?"
    payment_manager.cursor.execute(sql, (payment_code, payment_id))
    payment_manager.conn.commit()
    
    return {
        "payment_id": payment_id,
        "amount_vnd": package['amount_vnd'],
        "tokens_received": package['tokens'],
        "transaction_content": payment_code,
        "bank_account": settings.SEPAY_ACCOUNT_NUMBER,
        "bank_brand": settings.SEPAY_BANK_BRAND,
        # QR URL updated to use the new content
        "qr_url": f"https://qr.sepay.vn/img?acc={settings.SEPAY_ACCOUNT_NUMBER}&bank={settings.SEPAY_BANK_BRAND}&amount={package['amount_vnd']}&des={payment_code}"
    }

@router.get("/history")
async def get_history(
    current_user: dict = Depends(get_current_user),
    payment_manager: PaymentManager = Depends(get_payment_manager)
):
    return payment_manager.get_user_payments(current_user['id'])

@router.post("/check-status/{payment_id}")
async def check_payment_status(
    payment_id: int,
    current_user: dict = Depends(get_current_user),
    payment_manager: PaymentManager = Depends(get_payment_manager),
    user_manager: UserManager = Depends(get_user_manager)
):
    # Lấy thông tin thanh toán từ DB check sở hữu
    payment_manager.cursor.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
    payment_row = payment_manager.cursor.fetchone()
    
    if not payment_row:
        raise HTTPException(status_code=404, detail="Payment not found")
        
    payment = dict(payment_row)
    if payment['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Nếu đã completed thì trả về luôn
    if payment['status'] == 'completed':
        return {"status": "completed", "message": "Payment success"}

    # Nếu chưa có Key SePay, trả về status hiện tại
    if not settings.SEPAY_API_KEY:
        return {"status": payment['status'], "message": "SePay API Key not configured"}

    # Logic So khớp (Reconciliation Logic) theo Guide
    try:
        url = "https://my.sepay.vn/userapi/transactions/list"
        headers = {"Authorization": f"Bearer {settings.SEPAY_API_KEY}"}
        params = {"account_number": settings.SEPAY_ACCOUNT_NUMBER, "limit": 20}
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            transactions = response.json().get('transactions', [])
            
            # Target HEX ID cần tìm
            target_hex = encode_payment_id(payment_id)
            
            # Regex pattern: {NAME_WEB}NAPTOKEN([A-Fa-f0-9]+)
            prefix = settings.NAME_WEB + "NAPTOKEN"
            pattern = rf"{prefix}([A-Fa-f0-9]+)"
            
            found = False
            matched_tx_id = None
            
            for tx in transactions:
                content = tx.get('transaction_content', '')
                amount_in = float(tx.get('amount_in', 0))
                
                # Kiểm tra nội dung chứa mã nạp logic
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    found_hex = match.group(1).upper()
                    
                    # So sánh HEX ID và Số tiền (chấp nhận >=)
                    if found_hex == target_hex and amount_in >= payment['amount_vnd']:
                        matched_tx_id = str(tx.get('id'))
                        found = True
                        break
            
            if found:
                # Update status completed
                payment_manager.update_payment(payment_id, 'completed', matched_tx_id)
                user_manager.update_token(payment['user_id'], payment['tokens_received'])
                return {"status": "completed", "message": "Payment success"}
            else:
                 return {"status": payment['status'], "message": "Transaction not found yet"}
                 
    except Exception as e:
        print(f"Error checking SePay: {e}")
        
    return {"status": payment['status']}
