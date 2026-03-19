from chatbot.chatbot.utils.custom_prompt import CustomPrompt  # noqa: I001
from chatbot.chatbot.utils.prompt_analyzer import PromptAnalyzerFormat
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel,  Field
from typing import Optional, Dict, List
from langchain_core.messages import SystemMessage, HumanMessage


class ResultsFormat(BaseModel):
    colors: bool = Field(..., description="Banner có những màu sắc theo yêu cầu hay không")
    reason_color: Optional[str] = Field(..., description="Lý do chọn kết quả cho colors")
    text: bool = Field(..., description="Banner có nội dung văn bản đúng theo yêu cầu hay không")
    reason_text: Optional[str] = Field(..., description="Lý do chọn kết quả cho text")
    image_elements: bool = Field(..., description="Banner có các thành phần hình ảnh đúng theo yêu cầu hay không")
    reason_image: Optional[str] = Field(..., description="Lý do chọn kết quả cho image_elements")

class BannerValidatorFormat(BaseModel):
    conditions: PromptAnalyzerFormat = Field(..., description="Điều kiện để đánh giá banner")
    results: ResultsFormat = Field(..., description="Kết quả kiểm tra từng phần của banner")
    all_passed: bool = Field(..., description="True nếu tất cả điều kiện được đáp ứng, False nếu không")


class BannerValidator:
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
            ("system", CustomPrompt.VALIDATE_BANNER),
            ("human", "Hãy kiểm tra banner với các điều kiện sau:\n{conditions}\nĐây là ảnh base64:\n{image_base64}")
        ])

        # prompt = ChatPromptTemplate.from_messages([
        #     SystemMessage(content=CustomPrompt.VALIDATE_BANNER),
        #     HumanMessage(
        #         content="""
        #             `
        #                 "type": "text",
        #                 "text": "Hãy kiểm tra banner với các điều kiện sau:\n{conditions}"
        #             `,
        #             `
        #                 "type": "image_url",
        #                 "image_url": "url": "{image_base64}"
        #             `
        #         """
        #     )
        # ])

        # Tạo pipeline đầu ra có cấu trúc với mô hình, dùng function_calling để tránh dùng JSON Schema chuẩn OpenAI
        structured_output = llm.with_structured_output(BannerValidatorFormat)

        # Xây dựng pipeline xử lý: nhận prompt -> xử lý với LLM -> trích xuất kết quả dạng có cấu trúc
        self.chain = prompt | structured_output


    def get_chain(self) -> RunnableSequence:
        """
        Trả về chuỗi pipeline xử lý để tạo câu trả lời.

        Returns:
            RunnableSequence: Chuỗi thực thi pipeline xử lý câu hỏi.
        """
        return self.chain
