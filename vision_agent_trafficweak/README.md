# 교통 약자 보호 표지판 인식 프로그램 🚸

### 소개
이 프로그램은 도로 영상에서 **교통 약자 보호 표지판**(어린이, 노인, 장애인)을 인식하고 경고 메시지를 표시해주는 데 목적이 있습니다. SIFT 알고리즘을 사용하여 도로 영상 속 표지판을 인식합니다.

---

### 📋 기능
- **표지판 등록**: 어린이, 노인, 장애인 보호 표지판 이미지를 등록합니다.
- **도로 영상 등록**: 표지판이 포함된 도로 사진 또는 동영상을 불러옵니다.
- **표지판 인식**: 도로 영상에서 표지판을 감지하여 경고 메시지를 표시합니다.

---

### 🛠️ 설치 및 실행 방법

#### **1. 필수 요구 사항**
- Python 3.10 이상
- OpenCV
- PyQt6
- NumPy

#### **2. 설치**
먼저 이 저장소를 클론합니다.
```bash
# git clone https://github.com/yourusername/traffic-weak-sign-detection.git
# cd traffic-weak-sign-detection
필요한 라이브러리를 설치합니다.
pip install -r requirements.txt

3. 실행
python main.py
📁 파일 구조
css
코드 복사
traffic-weak-sign-detection/
├── child.png
├── elder.png
├── disabled.png
├── main.py
├── README.md
├── pyproject.toml
└── requirements.txt

child.png, elder.png, disabled.png: 프로그램에서 사용하는 표지판 이미지 파일입니다.
main.py: 프로그램의 메인 코드입니다.
requirements.txt: 필요한 Python 라이브러리 목록입니다.
pyproject.toml: 프로젝트 설정 파일입니다.

🖼️ 사용 방법
프로그램 실행 후, 표지판 이미지를 등록합니다.
도로 사진 또는 동영상을 불러옵니다.
인식 버튼을 눌러 표지판이 인식되면 경고 메시지가 출력됩니다.

⚠️ 주의 사항
표지판 이미지는 프로그램과 같은 폴더에 저장해야 합니다.
프로그램은 SIFT 알고리즘을 사용하기 때문에 OpenCV 4.4.0 이상이 필요합니다.
