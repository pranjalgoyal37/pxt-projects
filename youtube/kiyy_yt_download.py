import os
from pytube import YouTube, Playlist
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import pandas as pd

class YoutubeDownloaderApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', spacing=10, padding=(10, 10))
        
        self.dir_text = TextInput(multiline=False, hint_text="Enter directory", font_size=16)
        self.root.add_widget(self.dir_text)

        self.url_text = TextInput(multiline=False, hint_text="Enter YouTube video or playlist URL", font_size=16)
        self.url_text.bind(focus=self.on_textbox_click)
        self.root.add_widget(self.url_text)

        self.source_urls_text = TextInput(multiline=True, readonly=True, font_size=16)
        scroll_view = ScrollView(size=(500, 200), bar_width=10, scroll_type=['bars'], scroll_wheel_distance=20)
        scroll_view.add_widget(self.source_urls_text)
        self.root.add_widget(scroll_view)

        btn_show_videos = Button(text="Show Videos", size_hint=(1, 0.2), font_size=16)
        btn_show_videos.bind(on_press=self.show_videos)
        self.root.add_widget(btn_show_videos)

        btn_download_playlist = Button(text="Download Playlist", size_hint=(1, 0.2), font_size=16)
        btn_download_playlist.bind(on_press=self.download_playlist)
        self.root.add_widget(btn_download_playlist)

        btn_download_video = Button(text="Download Video", size_hint=(1, 0.2), font_size=16)
        btn_download_video.bind(on_press=self.download_video)
        self.root.add_widget(btn_download_video)

        self.video_info_text = TextInput(multiline=True, readonly=True, font_size=16)
        scroll_view = ScrollView(size=(500, 200), bar_width=10, scroll_type=['bars'], scroll_wheel_distance=20)
        scroll_view.add_widget(self.video_info_text)
        self.root.add_widget(scroll_view)

    def on_textbox_click(self, instance, value):
        if self.url_text.text == "Enter YouTube video or playlist URL":
            self.url_text.text = ""

    def show_videos(self, instance):
        url = self.url_text.text.strip()
        playlist = Playlist(url)
        
        for video_url in playlist:
            threading.Thread(target=self.download_video_info, args=(video_url,)).start()

    def download_video_info(self, video_url):
        try:
            video = YouTube(video_url)
            video_info = f"Title: {video.title}\nLength: {video.length}\nLink: {video_url}\n"
            self.video_info_text.text += video_info
        except Exception as e:
            print(f"Error retrieving video information: {str(e)}")

    def download_playlist(self, instance):
        url = self.url_text.text.strip()
        dir_name = self.dir_text.text.strip()

        try:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            
            for video_url in Playlist(url).video_urls:
                threading.Thread(target=self.download_video, args=(video_url,)).start()
        except:
            print("Please try after some time")

    def download_video(self, video_url):
        try:
            yt = YouTube(video_url)
            video_stream = yt.streams.get_highest_resolution()
            video_stream.download(output_path=self.dir_text.text.strip())
            print(f"Download of {yt.title} completed successfully!")
        except Exception as e:
            print(f"An error occurred while downloading {video_url}: {str(e)}")

YoutubeDownloaderApp().run()
