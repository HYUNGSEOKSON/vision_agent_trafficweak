import cv2
import numpy as np
from PyQt6.QtWidgets import *
import sys
import winsound
import os


class TrafficWeak(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("교통약자 보호")
        self.setGeometry(200, 200, 700, 200)

        signButton = QPushButton("표지판 등록", self)
        roadButton = QPushButton("도로 영상 불러옴", self)
        recognitionButton = QPushButton("인식", self)
        quitButton = QPushButton("나가기", self)
        self.label = QLabel("환영합니다!", self)

        signButton.setGeometry(10, 10, 100, 30)
        roadButton.setGeometry(110, 10, 100, 30)
        recognitionButton.setGeometry(210, 10, 100, 30)
        quitButton.setGeometry(510, 10, 100, 30)
        self.label.setGeometry(10, 40, 600, 170)

        signButton.clicked.connect(self.signFunction)
        roadButton.clicked.connect(self.roadFunction)
        recognitionButton.clicked.connect(self.recognitionFunction)
        quitButton.clicked.connect(self.quitFunction)

        # 현재 작업 디렉토리 확인
        self.current_dir = os.getcwd()
        print(f"현재 작업 디렉토리: {self.current_dir}")

        # 표지판 이미지의 상대 경로 설정
        self.signFiles = [
            ["child.png", "어린이"],
            ["elder.png", "노인"],
            ["disabled.png", "장애인"],
        ]
        self.signImgs = []

    def signFunction(self):
        self.label.clear()
        self.label.setText("교통약자 표지판을 등록합니다.")

        # 표지판 이미지 등록 (현재 작업 디렉토리 기준)
        if not self.signImgs:
            for fname, label in self.signFiles:
                # 현재 디렉토리에서 파일을 읽어오기
                full_path = os.path.join(self.current_dir, fname)
                img = cv2.imread(full_path)
                if img is not None:
                    self.signImgs.append(img)
                    cv2.imshow(label, img)
                else:
                    print(f"이미지 파일 {full_path}을(를) 찾을 수 없습니다.")
                    self.label.setText(f"이미지 파일 {fname}을(를) 찾을 수 없습니다.")

    def roadFunction(self):
        if not self.signImgs:
            self.label.setText("먼저 표지판을 등록하세요.")
            return
        fname, _ = QFileDialog.getOpenFileName(self, "도로 영상 파일 읽기", "./")
        if not fname:
            self.label.setText("파일이 선택되지 않았습니다.")
            return
        self.roadImg = cv2.imread(fname)
        if self.roadImg is None:
            self.label.setText("파일을 찾을 수 없습니다.")
            return
        cv2.imshow("Road scene", self.roadImg)

    def recognitionFunction(self):
        if not hasattr(self, "roadImg"):
            self.label.setText("먼저 도로 영상을 입력하세요.")
            return

        try:
            sift = cv2.SIFT_create()
        except AttributeError:
            self.label.setText("OpenCV에서 SIFT를 사용할 수 없습니다.")
            return

        KD = []
        for img in self.signImgs:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            KD.append(sift.detectAndCompute(gray, None))

        grayRoad = cv2.cvtColor(self.roadImg, cv2.COLOR_BGR2GRAY)
        road_kp, road_des = sift.detectAndCompute(grayRoad, None)

        matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        GM = []

        for sign_kp, sign_des in KD:
            knn_match = matcher.knnMatch(sign_des, road_des, 2)
            T = 0.7
            good_match = [m[0] for m in knn_match if len(m) > 1 and (m[0].distance / m[1].distance) < T]
            GM.append(good_match)

        best = GM.index(max(GM, key=len))

        if len(GM[best]) < 4:
            self.label.setText("표지판이 없습니다.")
        else:
            sign_kp = KD[best][0]
            good_match = GM[best]

            points1 = np.float32([sign_kp[gm.queryIdx].pt for gm in good_match])
            points2 = np.float32([road_kp[gm.trainIdx].pt for gm in good_match])

            H, _ = cv2.findHomography(points1, points2, cv2.RANSAC)

            h1, w1 = self.signImgs[best].shape[:2]
            box1 = np.float32([[0, 0], [0, h1 - 1], [w1 - 1, h1 - 1], [w1 - 1, 0]]).reshape(4, 1, 2)
            box2 = cv2.perspectiveTransform(box1, H)

            self.roadImg = cv2.polylines(self.roadImg, [np.int32(box2)], True, (0, 255, 0), 4)
            self.label.setText(self.signFiles[best][1] + " 보호구역입니다. 30km로 서행하세요.")
            cv2.imshow("Detection Result", self.roadImg)

    def quitFunction(self):
        cv2.destroyAllWindows()
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TrafficWeak()
    win.show()
    sys.exit(app.exec())