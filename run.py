import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # 프로덕션에서는 False
        workers=4  # CPU 코어 수에 따라 조정
    ) 