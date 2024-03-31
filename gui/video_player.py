from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

class VideoPlayer(QVideoWidget):
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self)
        self.media_player.mediaStatusChanged.connect(self.handle_media_status_changed)
        self.playlist = QMediaPlaylist()
        self.media_player.setPlaylist(self.playlist)
        self.loop_start_time = None
        self.loop_end_time = None
        self.video_path = None

    def set_video(self, video_path):
        self.video_path = video_path
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.media_player.play()

    def set_loop_segment(self, start_time, end_time):
        self.loop_start_time = start_time
        self.loop_end_time = end_time
        self.playlist.clear()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.video_path)))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.media_player.setPosition(int(start_time * 1000))

    def handle_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia and self.loop_start_time is not None and self.loop_end_time is not None:
            self.media_player.setPosition(int(self.loop_start_time * 1000))