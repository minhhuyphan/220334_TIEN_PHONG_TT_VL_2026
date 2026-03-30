import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv(override=True)
api_key = os.getenv("KEY_API_GOOGLE")

if not api_key:
    print("❌ Không tìm thấy KEY_API_GOOGLE trong file .env!")
    exit()

def list_models():
    print(f"🔍 Đang truy vấn danh sách model từ Google với Key: {api_key[:8]}... \n")
    client = genai.Client(api_key=api_key)
    
    try:
        # Lấy danh sách tất cả các models mà Key này có quyền truy cập
        models = client.models.list()
        
        print(f"{'No.':<4} | {'Tên Model':<45} | {'Hành động hỗ trợ'}")
        print("-" * 100)
        
        for i, model in enumerate(models, 1):
            # Print available attributes for debugging
            # print(dir(model))
            # Just print the basic name and try to find methods
            name = getattr(model, 'name', 'Unknown')
            display_name = getattr(model, 'display_name', 'Unknown')
            methods = getattr(model, 'supported_generation_methods', [])
            if not methods:
                 # Try other names or just skip
                 methods = getattr(model, 'methods', [])
            
            print(f"{i:<4} | {name:<45} | {display_name:<30}")
            
    except Exception as e:
        print(f"❌ Lỗi khi lấy danh sách model: {str(e)}")

if __name__ == "__main__":
    list_models()
