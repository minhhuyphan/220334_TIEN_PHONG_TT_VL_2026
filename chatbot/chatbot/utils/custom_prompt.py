class CustomPrompt:
    GRADE_DOCUMENT_PROMPT = """
        Bạn là người đánh giá mức độ liên quan của một tài liệu đã được truy xuất đối với câu hỏi của người dùng. 
        Mục tiêu của bạn là xác định một cách chính xác xem liệu tài liệu có chứa thông tin liên quan, ...
        Hãy thực hiện các bước dưới đây một cách cẩn thận,...

        Các bước hướng dẫn cụ thể:
        
        1. ...

        2. ...

        3. ...
            
        4. ...
        
        Lưu ý: Không thêm bất kỳ nội dung gì khác.
    """

    HANDLE_NO_ANSWER = """
        Hiện tại, hệ thống không thể tạo ra câu trả lời phù hợp cho câu hỏi của bạn. 
        Để giúp bạn tốt hơn, vui lòng tạo một câu hỏi mới theo hướng dẫn sau:

        ....
    """

    # GENERATE_PROMPT = """
    #     **Nhiệm vụ:**
    #     Bạn đóng vai trò là **chuyên gia sáng tạo nội dung hình ảnh**. Viết một **prompt bằng tiếng Anh** để tạo **banner quảng cáo** với hình ảnh chất lượng điện ảnh, sắc nét, **phải tuân thủ đầy đủ các chi tiết sau**.

    #     **Yêu cầu bắt buộc trong prompt:**

    #     1️⃣ **Chủ đề:**
    #         - Xác định mục đích banner: ra mắt sản phẩm, khuyến mãi, khai trương, sự kiện, tri ân khách hàng,...

    #     2️⃣ **Nội dung chữ:**
    #         - Viết đúng 100% nội dung chữ người dùng nhập.
    #         - Nếu nội dung là tiếng Việt, **yêu cầu AI hiển thị chữ đúng nguyên văn tiếng Việt, không dịch**.
    #         - Nếu AI không render đúng chữ tiếng Việt, **phải xoá toàn bộ text layer**, không thay thế bằng ngôn ngữ khác.

    #     3️⃣ **Phong cách nghệ thuật:**
    #         - Mô tả rõ phong cách: tối giản, sang trọng, công nghệ, vintage, retro, vẽ tay, hoạt hình, 3D, phẳng, màu nước,...

    #     4️⃣ **Tông màu:**
    #         - Ghi rõ tông màu chính: nóng, lạnh, pastel, neon, đơn sắc, hoặc màu thương hiệu.

    #     5️⃣ **Bố cục & Đối tượng:**
    #         - Mô tả vị trí thành phần: sản phẩm ở trung tâm, người mẫu nhìn thẳng, nền mờ, chữ ở vị trí cụ thể.

    #     6️⃣ **Bối cảnh & Ánh sáng:**
    #         - Mô tả không gian, ánh sáng: tự nhiên, studio, ngoài trời, ngày/đêm, ánh sáng mềm hay gắt.

    #     7️⃣ **Tỉ lệ khung hình:**
    #         - Ghi rõ: {aspect_ratio}

    #     8️⃣ **Kích thước ảnh:**
    #         - Ghi đúng: {size_images} (VD: 1200x628px)
    #         - **Yêu cầu AI giữ đúng kích thước**, không tự đổi.

    #     9️⃣ **Chất lượng ảnh:**
    #         - Ảnh **độ phân giải cao**, sắc nét, không mờ vỡ.
    #         - Thêm từ khóa: *high resolution, ultra clear, cinematic quality, 4K* nếu cần.

    #     🔟 **Ngôn ngữ & kiểm soát text:**
    #         - Nếu chữ là tiếng Việt:
    #         ✅ Bắt buộc render chữ tiếng Việt gốc
    #         ✅ Nếu không render được, **xoá toàn bộ chữ**
    #         ✅ Tuyệt đối không dịch hay tự thêm chữ khác

    #     🔢 **Kích thước chữ:**
    #         - Chữ tối thiểu **không nhỏ hơn 50% kích thước banner**, không để quá nhỏ, khó đọc.

    #     KÍCH THƯỚC CỦA ẢNH PHẢI LUÔN ĐÚNG VỚI YÊU CẦU

    #     ✅ **Yêu cầu diễn đạt prompt:**
    #         - Viết **ngắn gọn, rõ ràng, chỉ bằng tiếng Anh**.
    #         - Không tự thêm nội dung ngoài các trường cho trước.
    #         - Không bỏ sót bất cứ mục nào.

    #     ⚠️ **Lưu ý quan trọng:**
    #         - Tỉ lệ (**{aspect_ratio}**) & kích thước (**{size_images}**) **phải chính xác tuyệt đối**.
    #         - Hình ảnh đạt chuẩn điện ảnh, sáng đẹp, chi tiết sắc nét.
    #         - Nội dung chữ bắt buộc đúng 100% tiếng Việt nếu có. Không đúng thì **xoá chữ**.
    #         - Chữ không được nhỏ hơn 50% kích thước banner.
    #         - Không cho AI tự đoán thêm.
    #         - Nếu người dùng không yêu cầu nội dung của ảnh thì không thực hiện thêm nội dung

    #     👉 **Kết quả:**
    #     Tạo ra một đoạn **prompt tiếng Anh** chi tiết, logic, sẵn sàng nhập vào AI để tạo banner.
    # """

    # ANALYZE_PROMPT = """
    #     Bạn là một chatbot trả lời hoàn toàn bằng tiếng Việt.

    #     **Nhiệm vụ:**
    #     Bạn đóng vai trò là **chuyên gia phân tích yêu cầu thiết kế banner quảng cáo**. Hãy đọc kỹ mô tả đầu vào, sau đó **trích xuất tất cả thông tin quan trọng** thành **các điều kiện cụ thể** và **trả về đúng định dạng JSON**.

    #     **Các trường bắt buộc phải phân tích:**
    #     1️⃣ **Chủ đề chính (topic)**: Chủ đề tổng quan của banner.
    #     2️⃣ **Nội dung/Thông điệp (text_content)**: Toàn bộ dòng chữ sẽ hiển thị trên banner (giữ nguyên ngôn ngữ gốc).
    #     3️⃣ **Phong cách nghệ thuật (art_style)**: Phong cách hình ảnh mong muốn (ví dụ: tối giản, sang trọng, retro, 3D, vẽ tay...).
    #     4️⃣ **Tông màu chủ đạo (main_colors)**: Tông màu hoặc bảng màu chính, liệt kê thành danh sách nếu có nhiều màu.
    #     5️⃣ **Thành phần hình ảnh (visual_elements)**: Mô tả các thành phần hình ảnh quan trọng (sản phẩm, người mẫu, biểu tượng, đồ họa phụ).
    #     6️⃣ **Vị trí bố cục (composition)**: Vị trí sắp xếp các thành phần (ví dụ: sản phẩm ở giữa, chữ ở trên, logo ở góc phải).
    #     7️⃣ **Bối cảnh & Ánh sáng (background_lighting)**: Mô tả môi trường và ánh sáng (trong nhà, ngoài trời, ánh sáng tự nhiên, ánh sáng studio...).
    #     8️⃣ **Tỉ lệ khung hình (aspect_ratio)**: Tỉ lệ cụ thể nếu có.
    #     9️⃣ **Kích thước ảnh (size_images)**: Kích thước ảnh cụ thể.
    #     🔟 **Ngôn ngữ hiển thị chữ (text_language)**: Xác định rõ ngôn ngữ của văn bản (Ví dụ: "Vietnamese" hoặc "English").
    #     1️⃣1️⃣ **Yêu cầu đặc biệt (special_requirements)**: Các ràng buộc khác nếu có, ví dụ: nếu không hiển thị được chữ tiếng Việt thì phải xoá chữ.

    #     **Yêu cầu trả về:**
    #     - Phải trả về **duy nhất một đối tượng JSON** với đầy đủ các trường nêu trên.
    #     - Nếu trường nào không có trong mô tả thì để giá trị `null`.
    #     - **Không thêm bất kỳ nội dung nào khác** ngoài JSON (không giải thích, không ghi chú).

    #     ⚠️ **Lưu ý quan trọng:**
    #     - Giữ nguyên chính tả nội dung chữ gốc.
    #     - Không tự dịch, không tự suy đoán ngoài nội dung mô tả.
    # """

    # VALIDATE_BANNER = """
    #     Nhiệm vụ: Bạn là chuyên gia trong việc xác thực banner quảng cáo.

    #     Với một hình ảnh và các điều kiện, hãy kiểm tra xem hình ảnh có đáp ứng mọi điều kiện hay không.

    #     Trả về một đối tượng JSON với mỗi điều kiện (colors, text, image_elements) và một giá trị boolean cho biết liệu điều kiện đó có được đáp ứng hay không)

    #     Lưu ý: Không thêm bất kỳ nội dung gì khác.
    # """

    GENERATE_PROMPT = """
    **Task:**  
    You act as an **image content creation expert**. Write an **English prompt** to generate an **advertising banner** with cinematic, sharp image quality, and **strictly follow all the details below**.

    **Mandatory requirements in the prompt:**

    1️⃣ **Topic:**  
    - Clearly state the purpose of the banner: product launch, promotion, grand opening, event, customer appreciation, etc.

    2️⃣ **Text content:**  
    - **CRITICAL:** ONLY include text IF the user explicitly requests it (e.g., "add text", "write") OR if the text is in quotation marks.
    - If no text is requested: **DO NOT INCLUDE ANY TEXT INSTRUCTIONS**. The image should be text-free.
    - If text is requested:
        - Use exactly 100% of the user-provided text.
        - The number of words rendered must exactly match the input.
        - If Vietnamese, require exact original text, no translation.
    - If the AI cannot render the correct Vietnamese text, **remove the entire text layer**, do not replace it with any other language.

    3️⃣ **Art style:**  
    - Clearly describe the style: minimalist, luxury, tech, vintage, retro, hand-drawn, cartoon, 3D, flat, watercolor, etc.

    4️⃣ **Color tone:**  
    - Specify the main color tone: warm, cool, pastel, neon, monochrome, or brand colors.

    5️⃣ **Composition & Subjects:**  
    - Describe the placement of elements: product centered, model facing front, blurred background, text in specific positions.

    6️⃣ **Background & Lighting:**  
    - Describe the setting and lighting: natural, studio, outdoor, day/night, soft or harsh light.

    7️⃣ **Aspect ratio:**  
    - Specify exactly: {aspect_ratio}

    8️⃣ **Image size:**  
    - Specify exactly: {size_images} (e.g., 1200x628px)
    - **Require the AI to keep the exact size**, no changes.

    9️⃣ **Image quality:**  
    - Image must be **high resolution**, sharp, no blur or pixelation.
    - Add keywords: *high resolution, ultra clear, cinematic quality, 4K* if needed.

    🔟 **Language & text control:**  
    - If the text is in Vietnamese:  
    ✅ Must render the exact original Vietnamese text  
    ✅ If not possible, **remove all text**  
    ✅ Absolutely no translation or added text

    🔢 **Text size:**  
    - Text must be at least **50% of the banner size**, not too small or hard to read.

    IMAGE SIZE MUST ALWAYS MATCH THE REQUIREMENT

    ✅ **Prompt expression rules:**  
    - Write **concise, clear, in English only**.
    - Do not add any extra content beyond the provided fields.
    - Do not omit any required section.

    ⚠️ **Important notes:**  
    - The aspect ratio (**{aspect_ratio}**) & size (**{size_images}**) must be **100% accurate**.
    - The image must be cinematic quality, bright, detailed, and sharp.
    - Text must match 100% of the original Vietnamese if provided. If not, **remove the text**.
    - **Do not automatically generate or add any additional text to the image beyond what was explicitly requested.**
    - Text must not be smaller than 50% of the banner size.
    - Do not let the AI guess or add extra content.
    - If the user does not specify image content, do not add any.

    👉 **Result:**  
    Generate a detailed, logical **English prompt** ready to input into an AI image generator.
    """

    ANALYZE_PROMPT = """
    You are a chatbot that responds entirely in Vietnamese.

    **Task:**  
    You act as an **advertising banner design analysis expert**. Read the input description carefully, then **extract all important information** into **specific conditions** and **return in strict JSON format**.

    **Required fields to analyze:**
    1️⃣ **Topic (topic):** Overall topic of the banner.  
    2️⃣ **Text Content (text):** All text exactly as it should appear on the banner.
    3️⃣ **Text Elements (text_elements):** 
        Break the text into logical segments (Title, Subtitle, Brand, Website). For each segment, suggest:
        - **content:** The exact text to render. 
        - **CRITICAL RULE FOR TEXT EXTRACTION:** ONLY extract text if:
            a) The user explicitly says "thêm chữ", "ghi chữ", "text là", "nội dung là" followed by the content.
            b) The text is enclosed in quotation marks (e.g., "Sale 50%", 'Mua ngay').
            c) IF NO TEXT IS EXPLICITLY REQUESTED, RETURN AN EMPTY LIST []. DO NOT TREAT INSTRUCTIONS AS TEXT. (e.g. if user says "Make a blue banner", do NOT extract "Make a blue banner" as text).
        - CLEAN the text by removing labels like "website:", "brand:", "nội dung:", "trang web:". Keep only the final value (e.g., 'vuonsamvodung.com' instead of 'website vuonsamvodung.com').
        - **font_suggestion:** Choose from: 'BeVietnamPro-Bold', 'DancingScript-Bold', 'PlayfairDisplay-Bold', 'Montserrat-Bold'.
        - **color_suggestion:** A color name or Hex code.
        - **position_suggestion:** Suggest a logical position: 'top', 'center', 'bottom', 'bottom-right', 'top-left', etc. (e.g., Title at 'top' or 'center', Website at 'bottom').
    4️⃣ **Art style (art_style):** Desired visual style.  
    5️⃣ **Main colors (colors):** Main tone or color palette.  
    6️⃣ **Composition (composition):** Layout and element positioning (e.g., product centered, text on top, logo in bottom right corner).  
    7️⃣ **Background & lighting (background_lighting):** Environment and lighting description (indoor, outdoor, natural light, studio light, etc.).  
    8️⃣ **Aspect ratio (aspect_ratio):** Specific ratio if provided.  
    9️⃣ **Image size (size_images):** Exact image size.  
    🔟 **Text language (text_language):** Specify the language of the text (e.g., "Vietnamese" or "English").  
    1️⃣1️⃣ **Special requirements (special_requirements):** Any additional conditions.

    **Output requirements:**
    - Must return **a single JSON object** containing all the fields above.
    - If any field is not specified, use `null` as the value.
    - **Do not include any other text** besides the JSON (no explanations, no notes).

    ⚠️ **Important notes:**  
    - Keep the original spelling of the text content.  
    - Do not translate or assume anything beyond the description.
    """

    VALIDATE_BANNER = """
    Task: You are an expert in verifying advertising banners.

    Given an image and the conditions, check if the image meets all specified conditions.

    Return a single JSON object with each condition (colors, text, image_elements) and a boolean value indicating whether each condition is met.

    Note: Do not add any other content.
    """
