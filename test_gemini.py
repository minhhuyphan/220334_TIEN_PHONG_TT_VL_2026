import asyncio
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

load_dotenv(override=True)

async def test_gemini_connection():
    print(f"🔍 Đang kiểm tra siêu vũ khí 3.1 Image với Key: {settings.KEY_API_GOOGLE[:4]}...")
    client = genai.Client(api_key=settings.KEY_API_GOOGLE)
    
    try:
        # TEST COMPREHENSIVE: Gemini 3.1 Flash Image (Brain + Image)
        target_model = "models/gemini-3.1-flash-image-preview"
        print(f"\n🎨 TEST: Đang thử thách bản 3.1 vẽ chữ 'TIEN PHONG' lên Banner...")
        
        # Dùng trực tiếp SDK để tạo ảnh (Gemini Multimodal)
        response = client.models.generate_content(
            model=target_model,
            contents="Tạo một banner công nghệ hiện đại, có dòng chữ 'TIEN PHONG' rực rỡ ở giữa.",
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
            )
        )
        
        if response.candidates:
            print("✅ Đã nhận được phản hồi từ Gemini 3.1!")
            image_found = False
            for i, part in enumerate(response.candidates[0].content.parts):
                if part.inline_data:
                    with open(f"test_vip_ structure_3_1_{i}.png", "wb") as f:
                        f.write(part.inline_data.data)
                    print(f"🖼️ Đã lưu ảnh thành công vào file: test_vip_structure_3_1_{i}.png")
                    image_found = True
            
            if not image_found:
                 print("⚠️ Model phản hồi Text nhưng không có ảnh. Nội dung: ", response.candidates[0].content.parts[0].text)
        else:
            print("⚠️ Model phản hồi trống rỗng.")

    except Exception as e:
        print(f"\n❌ LỖI RỒI: {str(e)}")
        import traceback
        traceback.print_exc()
        
    except Exception as e:
        print(f"\n❌ LỖI RỒI: {str(e)}")
        if "404" in str(e):
            print("💡 Gợi ý: Google chưa tìm thấy tên model. Anh hãy kiểm tra xem KEY này có quyền truy cập v1beta không nhé.")

if __name__ == "__main__":
    asyncio.run(test_gemini_connection())
