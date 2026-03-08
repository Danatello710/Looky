from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

Window.size = (360, 640)

KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<VideoPost>:
    orientation: 'vertical'
    MDFloatLayout:
        Video:
            id: video_player
            source: root.video_source
            state: 'play' if root.is_playing else 'pause'
            options: {'eos': 'loop'}
            allow_stretch: True
            keep_ratio: False
            pos_hint: {"center_x": 0.5, "center_y": 0.5}

        # Кнопка паузы
        MDIcon:
            icon: "play-outline"
            font_size: "64sp"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 0.3 if not root.is_playing else 0
            pos_hint: {"center_x": 0.5, "center_y": 0.5}

        Button:
            background_color: 0, 0, 0, 0
            on_release: root.toggle_video()

        # Правая панель
        BoxLayout:
            orientation: 'vertical'
            size_hint: None, None
            size: "45dp", "180dp"
            pos_hint: {"right": 0.98, "center_y": 0.4}
            spacing: "5dp"

            MDIconButton:
                id: like_icon
                icon: "heart"
                user_font_size: "26sp"
                theme_icon_color: "Custom"
                icon_color: 1, 1, 1, 1
                on_release: root.press_like()

            MDIconButton:
                icon: "comment-text-outline"
                user_font_size: "26sp"
                theme_icon_color: "Custom"
                icon_color: 1, 1, 1, 1

            MDIconButton:
                icon: "share-outline"
                user_font_size: "26sp"
                theme_icon_color: "Custom"
                icon_color: 1, 1, 1, 1

        # Описание видео (упрощено)
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: "80dp"
            padding: ["15dp", "0dp", "60dp", "10dp"]
            pos_hint: {"bottom": 1}

            MDLabel:
                text: root.username
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                bold: True
                font_style: "Subtitle1"

            MDLabel:
                text: root.description
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.8
                font_style: "Caption"

MDBoxLayout:
    orientation: 'vertical'
    md_bg_color: 0, 0, 0, 1

    ScreenManager:
        id: screen_manager
        transition: FadeTransition(duration=0.1)

        Screen:
            name: 'feed_screen'
            Carousel:
                id: slide_container
                direction: 'bottom'
                on_index: app.manage_video_playback(self.index)

        Screen:
            name: 'profile_screen'
            MDBoxLayout:
                orientation: 'vertical'
                md_bg_color: 0, 0, 0, 1

                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    padding: [0, "20dp", 0, "20dp"]
                    spacing: "10dp"

                    MDIcon:
                        icon: "account-circle"
                        font_size: "80sp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1

                    MDLabel:
                        text: "@Даня"
                        halign: "center"
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        adaptive_height: True

                    # ИСПРАВЛЕННАЯ СТАТИСТИКА
                    MDBoxLayout:
                        orientation: 'horizontal'
                        adaptive_height: True
                        size_hint_x: None
                        width: "250dp"
                        pos_hint: {"center_x": .5}

                        MDLabel:
                            text: "[b]0[/b]\\nПодписчики"
                            markup: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                        MDLabel:
                            text: "[b]0[/b]\\nЛайки"
                            markup: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1

                MDSeparator:
                    md_bg_color: 0.2, 0.2, 0.2, 1

                ScrollView:
                    MDGridLayout:
                        cols: 3
                        adaptive_height: True
                        spacing: "2dp"
                        padding: "2dp"

                        # Квадраты-заглушки
                        Widget:
                            size_hint_y: None
                            height: self.width
                            canvas:
                                Color:
                                    rgba: 0.1, 0.1, 0.1, 1
                                Rectangle:
                                    pos: self.pos
                                    size: self.size

    # НИЖНИЙ БАР
    MDBoxLayout:
        size_hint_y: None
        height: "50dp"
        md_bg_color: 0, 0, 0, 1

        MDIconButton:
            icon: "home-variant" if screen_manager.current == 'feed_screen' else "home-variant-outline"
            theme_icon_color: "Custom"
            icon_color: (1, 1, 1, 1) if screen_manager.current == 'feed_screen' else (0.5, 0.5, 0.5, 1)
            size_hint_x: 0.5
            on_release: 
                screen_manager.current = 'feed_screen'
                app.resume_current_video()

        MDIconButton:
            icon: "account" if screen_manager.current == 'profile_screen' else "account-outline"
            theme_icon_color: "Custom"
            icon_color: (1, 1, 1, 1) if screen_manager.current == 'profile_screen' else (0.5, 0.5, 0.5, 1)
            size_hint_x: 0.5
            on_release: 
                screen_manager.current = 'profile_screen'
                app.stop_all_videos()
'''


class VideoPost(BoxLayout):
    video_source = StringProperty("")
    username = StringProperty("")
    description = StringProperty("")
    is_playing = BooleanProperty(False)

    def toggle_video(self):
        self.is_playing = not self.is_playing

    def press_like(self):
        self.ids.like_icon.icon_color = [1, 0, 0, 1] if self.ids.like_icon.icon_color == [1, 1, 1, 1] else [1, 1, 1, 1]


class TikTokApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.root_widget = Builder.load_string(KV)
        self.posts_list = []
        self.current_idx = 0

        carousel = self.root_widget.ids.slide_container

        # Твои данные с коротким описанием
        posts_data = [
            {"u": "@Даня", "d": "роылоарпуро", "v": "videos/1.mp4"},
            {"u": "@Даня", "d": "роылоарпуро", "v": "videos/2.mp4"},
        ]

        for data in posts_data:
            post = VideoPost(username=data["u"], description=data["d"], video_source=data["v"])
            carousel.add_widget(post)
            self.posts_list.append(post)

        if self.posts_list:
            self.posts_list[0].is_playing = True

        return self.root_widget

    def stop_all_videos(self):
        for post in self.posts_list:
            post.is_playing = False

    def resume_current_video(self):
        if self.posts_list:
            self.posts_list[self.current_idx].is_playing = True

    def manage_video_playback(self, current_index):
        self.current_idx = current_index
        for i, post in enumerate(self.posts_list):
            if i == current_index:
                post.is_playing = True
                post.ids.video_player.seek(0)
            else:
                post.is_playing = False


if __name__ == "__main__":
    TikTokApp().run()