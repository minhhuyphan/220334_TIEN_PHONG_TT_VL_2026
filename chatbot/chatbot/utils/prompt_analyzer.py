from chatbot.chatbot.utils.custom_prompt import CustomPrompt  # noqa: I001
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel,  Field
from typing import List, Optional, Tuple


class ImageElement(BaseModel):
    type: str = Field(..., description="Loại đối tượng, ví dụ: 'cốc cà phê', 'laptop', ...")
    position: Optional[str] = Field(..., description="Vị trí của đối tượng trên banner nếu có trong mô tả, nếu không có trả về null, ví dụ: 'top-left', 'right', ...")


class TextElement(BaseModel):
    content: str = Field(..., description="Nội dung văn bản")
    font_suggestion: str = Field(..., description="Gợi ý tên font (ví dụ: 'BeVietnamPro-Bold', 'DancingScript-Bold', 'PlayfairDisplay-Bold')")
    color_suggestion: str = Field(..., description="Gợi ý màu sắc (ví dụ: 'Gold', 'White', 'Red', '#FFD700')")
    position_suggestion: str = Field(..., description="Gợi ý vị trí (ví dụ: 'top', 'center', 'bottom', 'bottom-right')")

class PromptAnalyzerFormat(BaseModel):
    topic: Optional[str] = Field(..., description="Chủ đề tổng quan của banner")
    text: Optional[str] = Field(..., description="Toàn bộ nội dung chữ (dùng để tham khảo tổng quát)")
    text_elements: Optional[List[TextElement]] = Field(..., description="Danh sách các đoạn văn bản riêng biệt kèm theo style gợi ý")
    art_style: Optional[str] = Field(..., description="Phong cách nghệ thuật mong muốn")
    colors: Optional[List[str]] = Field(..., description="Danh sách các màu sắc chủ đạo")
    image_elements: Optional[List[ImageElement]] = Field(..., description="Danh sách các đối tượng hình ảnh xuất hiện")
    composition: Optional[str] = Field(..., description="Mô tả bố cục sắp xếp")
    background_lighting: Optional[str] = Field(..., description="Bối cảnh và ánh sáng")
    aspect_ratio: Optional[str] = Field(..., description="Tỉ lệ khung hình")
    size_images: Optional[str] = Field(..., description="Kích thước ảnh")
    text_language: Optional[str] = Field(..., description="Ngôn ngữ của văn bản")
    special_requirements: Optional[str] = Field(..., description="Yêu cầu đặc biệt khác")

class PromptAnalyzer:
    """
    Lớp AnswerGenerator chịu trách nhiệm tạo câu trả lời dựa trên câu hỏi của người dùng
    và ngữ cảnh được cung cấp.
    """

    def __init__(self, llm) -> None:
        """
        Khởi tạo AnswerGenerator với mô hình ngôn ngữ (LLM).

        Args:
            llm: Mô hình ngôn ngữ được sử dụng để tạo câu trả lời.
        """

        # Xây dựng prompt cho chatbot với ngữ cảnh và câu hỏi của người dùng

        prompt = ChatPromptTemplate.from_messages([
            ("system", CustomPrompt.ANALYZE_PROMPT),
            ("human", "Mô tả: {description}"),
        ])

        # Tạo pipeline đầu ra có cấu trúc với mô hình
        structured_output = llm.with_structured_output(PromptAnalyzerFormat)

        # Xây dựng pipeline xử lý: nhận prompt -> xử lý với LLM -> trích xuất kết quả dạng có cấu trúc
        self.chain = prompt | structured_output


    def get_chain(self) -> RunnableSequence:
        """
        Trả về chuỗi pipeline xử lý để tạo câu trả lời.

        Returns:
            RunnableSequence: Chuỗi thực thi pipeline xử lý câu hỏi.
        """
        return self.chain
