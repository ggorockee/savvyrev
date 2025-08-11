import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from core import config
from fastapi import Request
import json


# logger
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}')
handler.setFormatter(formatter)
logger.addHandler(handler)


class RichLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 요청 처리
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000  # ms 단위

        log_dict = {
            "client_host": request.client.host,
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "status_code": response.status_code,
            "process_time_ms": round(process_time, 2),
            # 필요에 따라 추가 정보 포함 가능
            # "user_id": request.state.user.id if hasattr(request.state, 'user') else None
        }
        
        # JSON 문자열로 변환하여 로그 기록
        logger.info(json.dumps(log_dict))
        
        return response