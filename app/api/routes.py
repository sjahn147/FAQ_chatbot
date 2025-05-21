from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.claude import ClaudeService
from app.core.context import get_context

router = APIRouter()
claude_service = ClaudeService()

class ChatRequest(BaseModel):
    message: str
    context_id: str = None

class ChatResponse(BaseModel):
    response: str
    context_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 컨텍스트 가져오기
        context = get_context(request.context_id) if request.context_id else None
        
        # Claude API 호출
        response = await claude_service.generate_response(
            message=request.message,
            context=context
        )
        
        return ChatResponse(
            response=response,
            context_id=request.context_id or "new_context"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 