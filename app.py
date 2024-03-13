from fastapi import FastAPI, Request, Form, HTTPException, Depends
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from kakao_manager import KakaoAPI  # KakaoAPI 클래스 임포트
import uvicorn

app = FastAPI()

# 여기서 'your-secret-key'는 실제 사용할 때 안전한 랜덤 값으로 변경해야 합니다.
app.add_middleware(SessionMiddleware, secret_key='your-secret-key')
templates = Jinja2Templates(directory="templates")
kakao_api = KakaoAPI()


@app.get("/getcode")
def get_kakao_code(request: Request):
    # 카카오 인증 URL 생성
    scope = 'profile_nickname, profile_image'
    kakao_auth_url = kakao_api.getcode_auth_url(scope)
    # 생성된 인증 URL로 사용자를 리다이렉트
    return RedirectResponse(kakao_auth_url)

@app.get("/callback")
async def kakao_callback(request: Request, code: str):
    # 카카오로부터 받은 인증 코드로 액세스 토큰 요청
    token_info = await kakao_api.get_token(code)
    if "access_token" in token_info:
        # 액세스 토큰을 세션에 저장하고 사용자 정보 페이지로 리다이렉트
        request.session['access_token'] = token_info['access_token']
        return RedirectResponse(url="/user_info", status_code=302)
    else:
        # 인증 실패 시 에러 메시지와 함께 홈페이지로 리다이렉트
        return RedirectResponse(url="/?error=Failed to authenticate", status_code=302)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    logged_in = 'access_token' in request.session
    return templates.TemplateResponse("index.html", {"request": request, "client_id": kakao_api.client_id, "redirect_uri": kakao_api.redirect_uri, "logged_in": logged_in})
@app.post("/login")
async def login(request: Request, code: str = Form(...)):
    token_info = await kakao_api.get_token(code)
    if "access_token" in token_info:
        request.session['access_token'] = token_info['access_token']
        return RedirectResponse(url="/user_info", status_code=302)
    else:
        raise HTTPException(status_code=400, detail="Kakao login failed")

@app.get("/logout")
async def logout(request: Request):
    client_id = kakao_api.client_id
    logout_redirect_uri = kakao_api.logout_redirect_uri
    await kakao_api.logout(client_id, logout_redirect_uri)
    request.session.pop('access_token', None)
    return RedirectResponse(url="/")

@app.get("/user_info", response_class=HTMLResponse)
async def user_info(request: Request):
    access_token = request.session.get('access_token')
    if access_token:
        user_info = await kakao_api.get_user_info(access_token)
        return templates.TemplateResponse("user_info.html", {"request": request, "user_info": user_info})
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/refresh_token")
async def refresh_token(refresh_token: str = Form(...)):
    client_id = kakao_api.client_id
    new_token_info = await kakao_api.refreshAccessToken(client_id, refresh_token)
    return new_token_info


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)