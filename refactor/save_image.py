from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os


class GoogleDriveUploader:
    def __init__(self, credentials_path):
        """
        Google Drive API 업로더 초기화

        Args:
            credentials_path (str): 서비스 계정 키 파일 경로 (.json)
        """
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self.credentials_path = credentials_path
        self.service = None

    def authenticate(self):
        """서비스 계정을 사용하여 Google Drive API 인증"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            # Drive API 서비스 생성
            self.service = build('drive', 'v3', credentials=credentials)
            return True

        except Exception as e:
            print(f"인증 오류: {str(e)}")
            return False

    def upload_image(self, image_path, folder_id=None, shared_with=None):
        """
        이미지를 Google Drive에 업로드

        Args:
            image_path (str): 업로드할 이미지 파일 경로
            folder_id (str, optional): 업로드할 폴더 ID
            shared_with (list, optional): 공유할 이메일 주소 리스트

        Returns:
            dict: 업로드된 파일 정보
        """
        if not self.service:
            raise Exception("먼저 authenticate() 메서드를 호출하여 인증을 수행하세요.")

        try:
            # 파일 메타데이터 설정
            file_metadata = {
                'name': os.path.basename(image_path)
            }

            # 특정 폴더에 업로드하는 경우
            if folder_id:
                file_metadata['parents'] = [folder_id]

            # 미디어 파일 객체 생성
            media = MediaFileUpload(
                image_path,
                mimetype='image/png',
                resumable=True
            )

            # 파일 업로드
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink',
                supportsAllDrives=True
            ).execute()

            # 파일 공유 설정 (지정된 경우)
            if shared_with and isinstance(shared_with, list):
                for email in shared_with:
                    permission = {
                        'type': 'user',
                        'role': 'reader',
                        'emailAddress': email
                    }
                    self.service.permissions().create(
                        fileId=file['id'],
                        body=permission,
                        sendNotificationEmail=False
                    ).execute()

            return file

        except Exception as e:
            print(f"업로드 오류: {str(e)}")
            return None


def main():
    # 서비스 계정 키 파일 경로
    credentials_path = 'service_account_credentials.json'

    # 업로더 인스턴스 생성
    uploader = GoogleDriveUploader(credentials_path)
    # print("here")

    # Google Drive API 인증
    if uploader.authenticate():
        # 이미지 업로드 예시
        image_path = "../test_image/test37.png"
        # folder_id = "your_folder_id"  # 선택사항
        # shared_with = ["user@example.com"]  # 선택사항
        result = uploader.upload_image(
            image_path=image_path
            # folder_id=folder_id,
            # shared_with=shared_with
        )

        if result:
            print("파일 업로드 성공!")
            print(f"File ID: {result['id']}")
            print(f"File Name: {result['name']}")
            print(f"Web View Link: {result['webViewLink']}")
    else:
        print("인증 실패")


if __name__ == '__main__':
    main()