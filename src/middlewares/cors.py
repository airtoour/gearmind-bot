from starlette.requests import Request

from src.db.config import app
from get_env import get_env


@app.middleware('http')
@app.middleware('https')
async def subdomain_cors_middleware(request: Request, call_next):
    response = await call_next(request)
    origin = request.headers.get('origin')
    if origin and origin.endswith(f'https://{get_env("FLASK_PORT")}'):
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Headers, ' \
                                                           'Authorization, X-Requested-With'
    return response