from app.models.banner_db import BannerDetails
from app.models.banner_db import Banners
from app.models.banner_db import Users
import time
from app.config import settings
import os
from io import BytesIO
import base64
from chatbot.chatbot.utils.prompt_analyzer import PromptAnalyzer
from chatbot.chatbot.utils.llm import LLM
from chatbot.chatbot.utils.prompt_generator import PromptGenerator
from typing import Optional
from PIL import Image
from google import genai
import io
from google.genai import types
from chatbot.chatbot.utils.banner_validator import BannerValidator
from chatbot.chatbot.utils.prompt_analyzer import PromptAnalyzerFormat


def parse_description_conditions(description: str):
    """
    Phân tích mô tả (description) từ người dùng và trích xuất các điều kiện kiểm tra cho hình ảnh AI.
    Parameters:
    - description (str): Mô tả đầu vào từ người dùng (ví dụ: "Một banner công nghệ có robot và nền xanh dương").
    Returns:
    - conditions (dict hoặc list): Các điều kiện được phân tích từ mô tả.
    """
    # THAY ĐỔI: Chuyển từ XAI sang OpenAI GPT để phân tích điều kiện
    llm_generate = PromptAnalyzer(
        LLM().get_llm(settings.LLM_NAME_OPENAI)
    ).get_chain()

    conditions = llm_generate.invoke({"description": description})
    return conditions


def generate_prompt(aspect_ratio: str, user_request: str, size_images: str):
    """
    Tạo prompt mô tả chi tiết để sinh hình ảnh AI dựa trên chủ đề, kích thước và yêu cầu của người dùng.
    Parameters:
    - theme (str): Chủ đề của hình ảnh (ví dụ: "công nghệ", "giáo dục").
    - aspect_ratio (str): Tỉ lệ khung hình.
    - user_request (str): Yêu cầu cụ thể từ người dùng (ví dụ: "có robot, tông màu xanh").
    Returns:
    - prompt (str): Prompt chi tiết đã được LLM sinh ra, sẵn sàng để dùng với AI tạo ảnh.
    """

    llm_generate = PromptGenerator(
        LLM().get_llm(settings.LLM_NAME_OPENAI)
    ).get_chain()

    prompt = llm_generate.invoke(
        {
            "aspect_ratio": {aspect_ratio},
            "user_request": {user_request},
            "size_images": {size_images},
        }
    )
    return prompt


def generate_banner(prompt: str) -> Optional[Image.Image]:
    from openai import OpenAI
    import base64

    _prompt = """
    Sử dụng font “Inter” hoặc “Roboto” để đảm bảo hỗ trợ Unicode.
    Dùng “advanced text renderer” và bật “full unicode glyph support”.
    không tách dấu khỏi ký tự” và “giữ nguyên vị trí dấu.
    """
    client = OpenAI(
        api_key=os.environ.get("KEY_API_GPT", "your-openai-api-key-here")
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f" {_prompt} \n\n {prompt}",
        tools=[{"type": "image_generation"}],
    )

    # Save the image to a file
    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]

    if image_data:
        img_b64 = image_data[0]  # lấy phần tử đầu tiên
        img_bytes = base64.b64decode(img_b64)
        image = Image.open(BytesIO(img_bytes))
        return image
    return None


def resize_and_encode_image(pil_image: Image.Image, max_size=512) -> str:
    """
    Resize ảnh PIL.Image giữ tỉ lệ, sau đó encode base64 dạng data URL (image/jpeg).
    """
    # Copy để tránh chỉnh sửa ảnh gốc
    img = pil_image.copy()
    img.thumbnail((max_size, max_size))
    # Lưu vào buffer dạng JPEG
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    # Encode base64 thành data:image/jpeg;base64,...
    b64_encoded = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_encoded}"


def check_banner_with_conditions(image_base64: str, conditions: PromptAnalyzerFormat):
    """
    Kiểm tra hình ảnh banner (dưới dạng base64) xem có đáp ứng các điều kiện mô tả hay không.
    Parameters:
    - image_base64 (str): Chuỗi base64 của hình ảnh banner cần kiểm tra.
    - conditions (List[str]): Danh sách các điều kiện cần được thoả mãn.
    Returns:
    - result (dict hoặc str): Kết quả đánh giá từ LLM, bao gồm nhận xét hoặc nhãn cho biết hình ảnh có đúng yêu cầu không.
    """
    # THAY ĐỔI: Chuyển từ XAI sang OpenAI GPT để validation banner
    llm_generate = BannerValidator(LLM().get_llm(settings.LLM_NAME_OPENAI)).get_chain()

    # CODE CŨ (XAI): Đã comment để backup
    # llm_generate = BannerValidator(LLM().get_llm(settings.LLM_NAME_XAI)).get_chain()

    result = llm_generate.invoke(
        {
            "conditions": conditions,
            "image_base64": image_base64,
        }
    )
    return result


def create_image(
    width=400,
    height=400,
    aspect_ratio="3:3",
    number=1,
    user_request="tạo 1 banner",
    NUMBER_COUNT_FOR_MAX=int(os.getenv("NUMBER_COUNT_FOR_MAX", "3")),
):
    # NUMBER_COUNT_FOR_MAX = os.getenv("NUMBER_COUNT_FOR_MAX", "3")

    size_images = f"s {width}, h {height}"
    max_attempts = number * 1

    conditions = parse_description_conditions(user_request)
    print(f"Dieu kien: {conditions}")

    print(f"\n🔧 [PHASE 0] Khởi tạo tạo banner...")  # noqa: F541
    print(f"📏 Kích thước yêu cầu: {width}x{height}")
    print(f"🎯 Độ phân giải: {aspect_ratio}")
    # print(f"🔢 Số lượng banner cần tạo: {number}")
    print(f"🔄 Giới hạn attempts: {max_attempts}")
    print(f"📝 Yêu cầu người dùng: {user_request}")
    print(f"🔍 Điều kiện phân tích: {conditions}")

    print(f"\n🚀 [ATTEMPT {max_attempts}] Bắt đầu tạo banner...")

    # 📝 PHASE 1: Tạo prompt
    print(f"📝 [PHASE 1] Tạo prompt mô tả chi tiết...")  # noqa: F541
    # Tạo prompt mô tả chi tiết để sinh hình ảnh AI
    prompt = generate_prompt(aspect_ratio, user_request, size_images)
    print(f"✅ [PHASE 1] Prompt được tạo thành công")  # noqa: F541
    print("prompt", prompt)

    NUMBER_LOOP = 0

    for _ in range(0, 1):
        print("tạo ảnh")
        banner = generate_banner(prompt)
        NUMBER_LOOP += 1

        file_name = f"banner_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        # banner.show()
        image_path = os.path.join(settings.DIR_ROOT, "utils", "download", file_name)
        banner.save(image_path)

        # Chuyển đổi sang base64 để validation
        print(f"🔍 [PHASE 3.1] Chuyển đổi ảnh sang base64...")  # noqa: F541
        image_base64 = resize_and_encode_image(banner)
        print(f"✅ [PHASE 3.1] Chuyển đổi base64 thành công")  # noqa: F541

        # Kiểm tra banner với điều kiện
        print(f"🔍 [PHASE 3.2] Kiểm tra banner với điều kiện...")  # noqa: F541
        check_banner = check_banner_with_conditions(image_base64, conditions)
        print(f"✅ [PHASE 3.2] Validation hoàn tất")  # noqa: F541

        print("check_banner", check_banner)

        if check_banner.all_passed:
            return file_name, NUMBER_LOOP

    return file_name, NUMBER_LOOP


def main():
    bd = BannerDetails()
    try:
        pending = bd.get_pending()
        if pending:
            print("Pending:", pending)
            banner_details_token = pending["tokens"]
            user_id = pending["user_id"]
            banner_details_id = pending["id"]

            for _ in range(int(pending["number"])):
                user_obj = Users()
                try:
                    user_data = user_obj.get_by_id(user_id)
                    user_token = user_data["tokens"]

                    if user_token < banner_details_token * settings.NUMBER_COUNT_FOR_MAX:
                        number_count_for_max = 1
                    else:
                        number_count_for_max = settings.NUMBER_COUNT_FOR_MAX

                    print("🖼️ Đang tạo ảnh...")

                    file_name, number_loop = create_image(
                        width=pending["width"],
                        height=pending["height"],
                        aspect_ratio=pending["proportion"],
                        number=1,
                        user_request=pending["description"],
                        NUMBER_COUNT_FOR_MAX=number_count_for_max,
                    )

                    link_image = (
                        f"{settings.URL_API}/api/v1/upload-file/view/{file_name}"
                    )

                    banners_obj = Banners()
                    try:
                        new_banner_id = banners_obj.create(
                            banner_details_id,
                            link_image,
                            False,
                            0,
                        )
                        print(f"✅ Đã thêm ảnh mới vào banners ID: {new_banner_id}")
                    finally:
                        banners_obj.close()

                    bd.update_status(banner_details_id, 1)
                    print(
                        f"✅ Cập nhật status banner_details ID {banner_details_id} thành 1"
                    )

                    token_now = int(user_token) - (
                        int(banner_details_token) * number_loop
                    )
                    user_obj.update_token(user_id, str(token_now))
                    print(f"🔑 Đã cập nhật tokens user ID {user_id} = {token_now}")

                finally:
                    user_obj.close()

        else:
            print("⏳ Không có banner_details nào đang chờ.")
    finally:
        bd.close()


if __name__ == "__main__":
    while True:
        try:
            main()
            print("..RUNING..")
            time.sleep(1)
        except:  # noqa: E722
            pass

# Export app for Render (FastAPI Support)
from app.main import app
