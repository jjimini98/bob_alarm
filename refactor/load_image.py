from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import pickle
import os
from PIL import Image
load_dotenv(verbose=True)


def get_google_drive_service():
    """Google Drive API 서비스 객체를 생성합니다."""
    # 1. API 권한 범위 설정
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None

    # 2. token.pickle 파일에서 인증 정보 로드
    if os.path.exists('final_token.pickle'):
        with open('final_token.pickle', 'rb') as token:
            creds = pickle.load(token)
            print("기존 토큰을 성공적으로 로드했습니다.")


    try:
        # 4. Drive API 서비스 객체 생성
        service = build('drive', 'v3', credentials=creds)
        print("Google Drive 서비스 객체가 성공적으로 생성되었습니다.")
        return service

    except Exception as e:
        print(f"서비스 객체 생성 중 오류가 발생했습니다: {str(e)}")
        return None


def check_folder_contents(service, folder_name):
    """특정 폴더의 내용을 자세히 확인합니다."""
    try:
        # 먼저 폴더 찾기
        folder_results = service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name)"
        ).execute()

        folders = folder_results.get('files', [])

        if not folders:
            print(f"'{folder_name}' 폴더를 찾을 수 없습니다.")
            return

        folder_id = folders[0]['id']
        print(f"\n'{folder_name}' 폴더 (ID: {folder_id}) 내용:")

        # 폴더 내 모든 파일 검색
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="files(id, name, mimeType)",
            pageSize=100
        ).execute()

        files = results.get('files', [])

        if not files:
            print("폴더가 비어있습니다.")
            return

        for file in files:
            print(f"\n파일명: {file['name']}")
            print(f"ID: {file['id']}")
            print(f"타입: {file['mimeType']}")
            print("-" * 50)

    except Exception as e:
        print(f"폴더 내용 확인 중 오류 발생: {str(e)}")


def save_image(image, file_name, save_dir='../test_image'):
    """
    PIL Image 객체를 로컬에 저장합니다.

    Args:
        image (PIL.Image): 저장할 이미지 객체
        file_name (str): 원본 파일 이름
        save_dir (str): 저장할 디렉토리 경로

    Returns:
        str: 저장된 파일의 전체 경로 또는 None
    """
    try:
        # 저장 디렉토리가 없으면 생성
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            print(f"'{save_dir}' 디렉토리를 생성했습니다.")

        # 파일 이름에서 확장자 추출
        file_extension = os.path.splitext(file_name)[1]
        if not file_extension:
            file_extension = '.png'  # 기본 확장자

        # 현재 시간을 포함한 파일 이름 생성 (중복 방지)
        new_file_name = f"{os.path.splitext(file_name)[0]}{file_extension}"

        # 전체 저장 경로 생성
        save_path = os.path.join(save_dir, new_file_name)

        # 이미지 저장
        image.save(save_path, quality=95, optimize=True)
        print(f"이미지를 저장했습니다: {save_path}")

        return save_path

    except Exception as e:
        print(f"이미지 저장 중 오류가 발생했습니다: {str(e)}")
        return None






def get_and_save_image(service, image_name, folder_name="bob_alarm",save_dir='../test_image'):
    """
    이미지 이름으로 Google Drive에서 이미지를 검색하고 불러옵니다.

    Args:
        service: Google Drive API 서비스 객체
        image_name (str): 찾을 이미지 파일 이름
        folder_name (str): 검색할 폴더 이름 (기본값: "bob_alarm")

    Returns:
        PIL.Image: 찾은 이미지 객체 또는 None
    """
    try:
        # 1. 먼저 폴더 ID 찾기
        folder_results = service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name)"
        ).execute()

        folders = folder_results.get('files', [])
        if not folders:
            print(f"'{folder_name}' 폴더를 찾을 수 없습니다.")
            return None

        folder_id = folders[0]['id']
        print(f"'{folder_name}' 폴더를 찾았습니다.")

        # 2. 폴더 내에서 이미지 파일 검색
        query = f"name='{image_name}' and '{folder_id}' in parents and (mimeType contains 'image/')"
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType)"
        ).execute()

        files = results.get('files', [])
        if not files:
            print(f"'{image_name}' 이미지를 찾을 수 없습니다.")
            return None

        file_id = files[0]['id']
        print(f"'{image_name}' 이미지를 찾았습니다.")

        # 3. 이미지 파일 다운로드
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False

        while not done:
            _, done = downloader.next_chunk()

        # 4. PIL Image 객체로 변환
        file.seek(0)
        image = Image.open(file)
        print(f"이미지를 성공적으로 불러왔습니다. (크기: {image.size})")

        saved_path = save_image(image, image_name, save_dir)
        return image , saved_path

    except Exception as e:
        print(f"이미지 검색 및 로드 중 오류가 발생했습니다: {str(e)}")
        return None, None



if __name__ == "__main__":
    # 사용 예시
    service = get_google_drive_service()
    # check_folder_contents(service, "bob_alarm")
    if service:
        # 이미지 이름으로 검색 및 로드
        image_name = input("찾을 이미지 파일 이름을 입력하세요: ")  # 예: "example.jpg"
        image, saved_path = get_and_save_image(service, image_name)

        if image and saved_path:
            print("\n=== 이미지 처리 완료 ===")
            print(f"이미지 크기: {image.size}")
            print(f"저장된 경로: {saved_path}")

            # 저장된 이미지 확인 (선택사항)
            image.show()

