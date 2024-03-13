# FastAPI Kakao Login Integration

FastAPI를 사용하여 카카오 소셜 로그인 기능을 구현하는 방법을 보여줍니다. 사용자는 카카오 계정을 통해 애플리케이션에 로그인할 수 있으며, 액세스 토큰을 사용하여 사용자의 프로필 정보에 접근할 수 있습니다.

## 기능

- 카카오 인증을 통한 로그인
- 카카오 로그아웃
- 카카오 사용자 프로필 정보 접근
- 액세스 토큰 갱신

## 설치

프로젝트에 필요한 패키지를 설치합니다:

```bash
pip install fastapi uvicorn httpx python-dotenv jinja2
```
## 환경 설정

`.env` 파일을 생성하고 다음 환경 변수를 설정합니다:

```makefile
KAKAO_CLIENT_ID=your_kakao_client_id 
KAKAO_CLIENT_SECRET=your_kakao_client_secret 
KAKAO_REDIRECT_URI=your_kakao_redirect_uri   //KAKAO_CLIENT_ID == AKAO_REDIRECT_URI
KAKAO_REST_API_KEY=your_kakao_rest_api_key 
KAKAO_LOGOUT_REDIRECT_URI=your_kakao_logout_redirect_uri
```

## 실행

애플리케이션을 실행하기 위해 다음 명령어를 사용합니다:

`uvicorn app:app --reload`

## 사용 방법

웹 브라우저를 열고 `http://localhost:8000`으로 이동하여 로그인 페이지를 확인합니다. 카카오 로그인 버튼을 클릭하여 카카오 인증을 진행합니다.

인증이 성공하면 사용자 정보 페이지로 리다이렉트되며, 사용자의 프로필 정보가 표시됩니다.

## 참고 자료

- FastAPI 공식 문서
- 카카오 로그인 REST API 가이드

---