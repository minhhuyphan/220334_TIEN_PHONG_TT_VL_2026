import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env ở thư mục gốc
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)


class Settings:
    DIR_ROOT = os.path.dirname(os.path.abspath(dotenv_path))
    KEY_API_GPT = os.getenv("KEY_API_GPT")
    NUM_DOC = int(os.getenv("NUM_DOC", "3"))
    LLM_NAME = os.getenv("LLM_NAME")
    OPENAI_LLM = os.getenv("OPENAI_LLM")

settings = Settings()

