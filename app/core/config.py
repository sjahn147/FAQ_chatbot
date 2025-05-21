from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 경로 설정
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# 환경 변수 로드
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# 환경 변수 검증
if not CLAUDE_API_KEY:
    raise ValueError("CLAUDE_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str
    MODEL_NAME: str = "claude-3-sonnet-20240229"
    MAX_TOKENS: int = 1000

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 