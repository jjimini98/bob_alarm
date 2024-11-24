from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os

# 사용할 SCOPE이 바뀔 때마다 token을 다시 생성해줘야함

def refresh_google_drive_token():
    """Google Drive API 토큰을 새로 생성합니다."""

    # 1. 기존 token.pickle 파일이 있다면 삭제
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')
        print("기존 token.pickle 파일이 삭제되었습니다.")

    # 2. 새로운 SCOPE으로 인증 진행
    SCOPES = ['https://www.googleapis.com/auth/drive']

    try:
        # 3. credentials.json으로부터 새로운 인증 진행
        flow = InstalledAppFlow.from_client_secrets_file('bob_alarm_desktop_credential.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # 4. 새로운 token.pickle 파일 생성
        with open('final_token.pickle', 'wb') as token:
            pickle.dump(creds, token)

        print("새로운 token.pickle 파일이 생성되었습니다.")

        # 5. 생성된 인증으로 테스트 (선택사항)
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(pageSize=1, fields="files(id, name)").execute()
        print("인증이 성공적으로 완료되었습니다.")

        return True

    except Exception as e:
        print(f"토큰 생성 중 오류가 발생했습니다: {str(e)}")
        return False


if __name__ == "__main__":
    print("Google Drive 토큰을 새로 생성합니다...")
    refresh_google_drive_token()