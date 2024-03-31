from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QWidget, QStyle, QCheckBox, QButtonGroup, QRadioButton, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer
from gui.video_player import VideoPlayer
from utils.video_utils import find_loop_segments, extract_and_save_loop_segment, create_loop_gif
from PIL import Image
import cv2

class ProcessingThread(QThread):
    progress_updated = pyqtSignal(int)
    processing_finished = pyqtSignal(list)

    def __init__(self, video_path, express_mode):
        super().__init__()
        self.video_path = video_path
        self.express_mode = express_mode

    def run(self):
        best_pairs = find_loop_segments(self.video_path, express_mode=self.express_mode, top_n=5, progress_callback=self.progress_callback)
        self.processing_finished.emit(best_pairs)

    def progress_callback(self, progress):
        self.progress_updated.emit(progress)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loopdy-do")
        self.setGeometry(100, 100, 800, 600)

        self.video_player = VideoPlayer()
        self.select_video_button = QPushButton(QIcon(self.style().standardIcon(QStyle.SP_FileDialogStart)), "Select Video")
        self.select_video_button.clicked.connect(self.select_video)
        self.process_button = QPushButton(QIcon(self.style().standardIcon(QStyle.SP_MediaPlay)), "Process Video")
        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.process_video)
        self.loop_start_end_label = QLabel("Loop Start/End Indexes:")
        self.loop_start_end_combo = QComboBox()
        self.loop_start_end_combo.setEnabled(False)
        self.loop_start_end_combo.currentIndexChanged.connect(self.update_loop_segment)
        self.preview_button = QPushButton(QIcon(self.style().standardIcon(QStyle.SP_MediaPlay)), "Preview Loop")
        self.preview_button.setEnabled(False)
        self.preview_button.clicked.connect(self.preview_loop)
        self.save_button = QPushButton(QIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton)), "Save Loop")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_loop)
        self.mute_button = QPushButton(QIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted)), "Mute")
        self.mute_button.setCheckable(True)
        self.mute_button.clicked.connect(self.toggle_mute)
        self.express_mode_checkbox = QCheckBox("Express Mode")
        self.output_format_group = QButtonGroup()
        self.video_radio = QRadioButton("Video")
        self.video_radio.setChecked(True)
        self.gif_radio = QRadioButton("GIF")
        self.output_format_group.addButton(self.video_radio)
        self.output_format_group.addButton(self.gif_radio)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_player)
        main_layout.addWidget(self.select_video_button)
        main_layout.addWidget(self.process_button)
        main_layout.addWidget(self.loop_start_end_label)
        main_layout.addWidget(self.loop_start_end_combo)
        main_layout.addWidget(self.preview_button)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.mute_button)
        main_layout.addWidget(self.express_mode_checkbox)
        main_layout.addWidget(self.video_radio)
        main_layout.addWidget(self.gif_radio)
        main_layout.addWidget(self.progress_bar)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.video_path = None
        self.loop_start_end_pairs = []
        self.current_loop_segment = None

    def select_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4 *.avi *.mov)")
        if self.video_path:
            self.video_player.set_video(self.video_path)
            self.process_button.setEnabled(True)

    def process_video(self):
        express_mode = self.express_mode_checkbox.isChecked()
        self.progress_bar.setVisible(True)
        self.processing_thread = ProcessingThread(self.video_path, express_mode)
        self.processing_thread.progress_updated.connect(self.update_progress)
        self.processing_thread.processing_finished.connect(self.processing_finished)
        self.processing_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def processing_finished(self, best_pairs):
        self.loop_start_end_pairs = []
        self.loop_start_end_combo.clear()

        for start_time, end_time in best_pairs:
            self.loop_start_end_pairs.append((start_time, end_time))
            self.loop_start_end_combo.addItem(f"Start: {start_time:.2f}s, End: {end_time:.2f}s")

        self.loop_start_end_combo.setEnabled(True)
        self.progress_bar.setVisible(False)

    def update_loop_segment(self, index):
        if index >= 0:
            start_time, end_time = self.loop_start_end_pairs[index]
            self.current_loop_segment = (start_time, end_time)
            self.preview_button.setEnabled(True)
            self.save_button.setEnabled(True)

    def preview_loop(self):
        if self.current_loop_segment:
            start_time, end_time = self.current_loop_segment
            self.video_player.set_loop_segment(start_time, end_time)

    def save_loop(self):
        if self.current_loop_segment:
            start_time, end_time = self.current_loop_segment
            if self.video_radio.isChecked():
                output_path, _ = QFileDialog.getSaveFileName(self, "Save Loop", "", "Video Files (*.mp4)")
                if output_path:
                    extract_and_save_loop_segment(self.video_path, start_time, end_time, output_path)
                    reencode_video(output_path, output_path)  # Re-encode the video
            else:
                output_path, _ = QFileDialog.getSaveFileName(self, "Save Loop", "", "GIF Files (*.gif)")
                if output_path:
                    create_loop_gif(self.video_path, start_time, end_time, output_path)
                    reencode_gif(output_path, output_path)  # Re-encode the GIF

    def toggle_mute(self):
        if self.mute_button.isChecked():
            self.video_player.media_player.setMuted(True)
        else:
            self.video_player.media_player.setMuted(False)

def reencode_video(input_path, output_path):
    input_video = cv2.VideoCapture(input_path)
    fps = input_video.get(cv2.CAP_PROP_FPS)
    width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while True:
        ret, frame = input_video.read()
        if not ret:
            break
        output_video.write(frame)

    input_video.release()
    output_video.release()

def reencode_gif(input_path, output_path):
    gif = Image.open(input_path)
    frames = []
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frames.append(gif.convert('RGB'))

    frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0)