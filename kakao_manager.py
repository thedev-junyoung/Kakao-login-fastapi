import httpx
import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

load_dotenv()

# 카카오 인증 및 API 상호작용을 관리하는 클래스
class KakaoAPI:
    def __init__(self):
        self.client_id = os.getenv('KAKAO_CLIENT_ID')
        self.client_secret = os.getenv('KAKAO_CLIENT_SECRET')
        self.redirect_uri = os.getenv('KAKAO_REDIRECT_URI')
        self.rest_api_key = os.getenv('KAKAO_REST_API_KEY')
        self.logout_redirect_uri = os.getenv('KAKAO_LOGOUT_REDIRECT_URI')

    def getcode_auth_url(self, scope):
        return f'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={self.rest_api_key}&redirect_uri={self.redirect_uri}&scope={scope}'

    async def get_token(self, code):
        token_request_url = 'https://kauth.kakao.com/oauth/token'
        token_request_payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "code": code,
            "client_secret": self.client_secret
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_request_url, data=token_request_payload)
        result = response.json()
        return result

    async def get_user_info(self, access_token):
        userinfo_endpoint = 'https://kapi.kakao.com/v2/user/me'
        headers = {'Authorization': f'Bearer {access_token}'}

        async with httpx.AsyncClient() as client:
            response = await client.get(userinfo_endpoint, headers=headers)
        return response.json() if response.status_code == 200 else None
    
    async def logout(self, client_id, logout_redirect_uri):
        logout_url = f"https://kauth.kakao.com/oauth/logout?client_id={client_id}&logout_redirect_uri={logout_redirect_uri}"
        async with httpx.AsyncClient() as client:
            await client.get(logout_url)
    
    async def refreshAccessToken(self, clientId, refresh_token):
        url = "https://kauth.kakao.com/oauth/token"
        payload = {
            "grant_type": "refresh_token",
            "client_id": clientId,
            "refresh_token": refresh_token
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload)
        refreshToken = response.json()
        return refreshToken

