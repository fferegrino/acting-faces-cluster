import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget
from scenedetect import detect, ContentDetector, split_video_ffmpeg

class SceneDetectorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Scene Detector')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.selectButton = QPushButton('Select Video', self)
        self.selectButton.clicked.connect(self.selectVideo)
        layout.addWidget(self.selectButton)

        self.detectButton = QPushButton('Detect Scenes', self)
        self.detectButton.clicked.connect(self.detectScenes)
        layout.addWidget(self.detectButton)

        self.resultText = QTextEdit(self)
        self.resultText.setReadOnly(True)
        layout.addWidget(self.resultText)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.videoPath = None

    def selectVideo(self):
        self.videoPath, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4 *.avi *.mov)")
        if self.videoPath:
            self.resultText.setText(f"Selected video: {self.videoPath}")

    def detectScenes(self):
        if not self.videoPath:
            self.resultText.setText("Please select a video first.")
            return

        scenes = detect(self.videoPath, ContentDetector())
        result = "Detected Scenes:\n"
        for i, scene in enumerate(scenes):
            result += f'Scene {i+1}: Start {scene[0].get_seconds():.2f}s, End {scene[1].get_seconds():.2f}s\n'
        
        self.resultText.setText(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SceneDetectorApp()
    ex.show()
    sys.exit(app.exec_())
