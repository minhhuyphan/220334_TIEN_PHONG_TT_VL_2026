# File cấu hình chung cho ứng dụng
import os
from dotenv import load_dotenv

# Load các biến môi trường từ file .env
load_dotenv(override=True)

class Settings:
    # SETTING
    DIR_ROOT = os.path.dirname(os.path.abspath(".env"))
    
    # DATABASE
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    DB_PATH = os.getenv("DB_PATH", os.path.join(DIR_ROOT, "banner_ai.db"))
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "4000"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_DATABASE = os.getenv("DB_DATABASE", "banner_ai")
    DB_SSL = os.getenv("DB_SSL", "")
    
 
    # AUTH & SECURITY
    API_KEY = os.environ.get("API_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret_key_change_me_in_prod")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
    
    # GOOGLE AUTH
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    
    # API KEYS MODELS
    KEY_API_GPT = os.getenv("KEY_API_GPT")
    KEY_API_GOOGLE = os.getenv("KEY_API_GOOGLE")
    
    # SEPAY SETTINGS (For Top-up)
    SEPAY_API_KEY = os.getenv("SEPAY_API_KEY")
    SEPAY_ACCOUNT_NUMBER = os.getenv("SEPAY_ACCOUNT_NUMBER")
    SEPAY_BANK_BRAND = os.getenv("SEPAY_BANK_BRAND")

    # MODEL PROVIDERS
    IMAGE_MODEL_PROVIDER = os.getenv("IMAGE_MODEL_PROVIDER", "google")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    
    # Google Model Configurations
    GOOGLE_LLM = os.getenv("GOOGLE_LLM", "gemini-1.5-flash")
    GOOGLE_LLM_IMAGE = os.getenv("GOOGLE_LLM_IMAGE", "imagen-3.0-generate-001")
    LLM_NAME_GOOGLE = GOOGLE_LLM
    LLM_NAME_OPENAI = os.getenv("LLM_NAME_OPENAI", OPENAI_LLM)

    # OTHER SETTINGS
    API_URL = os.getenv("API_URL", "http://localhost:55002")
    URL_API = os.getenv("URL_API", API_URL)
    NUM_DOC = int(os.getenv("NUM_DOC", "3"))
    NUMBER_COUNT_FOR_MAX = int(os.getenv("NUMBER_COUNT_FOR_MAX", "3"))
    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", '["*"]')
    TITLE_APP = os.getenv("TITLE_APP", "API BANNER")
    VERSION_APP = os.getenv("VERSION_APP", "v1")
    NAME_WEB = os.getenv("NAME_WEB", "AUTOBANNER")

settings = Settings()
