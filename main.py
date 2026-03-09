import os
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineAvatarListItem, IconLeftWidget

if platform != 'android':
    Window.size = (380, 720)

class CommentsPanel(MDFloatLayout):
    def dismiss(self):
        anim = Animation(pos_hint={"top": 0}, duration=0.2, t='in_quad')
        anim.bind(on_complete=lambda *x: self.parent.remove_widget(self))
        anim.start(self)

class VideoPost(BoxLayout):
    video_source = StringProperty("")
    username = StringProperty("")
    description = StringProperty("")
    is_playing = BooleanProperty(False)
    is_liked = BooleanProperty(False)
    like_size = NumericProperty(26)

    def toggle_video(self):
        self.is_playing = not self.is_playing

    def press_like(self):
        self.is_liked = not self.is_liked
        anim = Animation(like_size=35, duration=0.1) + Animation(like_size=26, duration=0.1)
        anim.start(self)

KV = '''
<CommentsPanel>:
    Button:
        background_color: 0, 0, 0, 0.5
        on_release: root.dismiss()

    MDBoxLayout:
        orientation: "vertical"
        size_hint_y: 0.75
        pos_hint: {"bottom": 0}
        md_bg_color: 0.1, 0.1, 0.1, 1
        radius: [20, 20, 0, 0]
        padding: "15dp"

        MDBoxLayout:
            adaptive_height: True
            MDLabel:
                text: "Комментарии"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
            MDIconButton:
                icon: "close"
                on_release: root.dismiss()

        ScrollView:
            MDList:
                id: comments_list
                OneLineAvatarListItem:
                    text: "Как*шка!!"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    IconLeftWidget:
                        icon: "account-circle-outline"

        MDBoxLayout:
            adaptive_height: True
            spacing: "10dp"
            MDTextField:
                id: comment_input
                hint_text: "Написать..."
                mode: "line"
            MDIconButton:
                icon: "send"
                on_release: app.add_comment(comment_input)

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

        Button:
            background_color: 0, 0, 0, 0
            on_release: root.toggle_video()

        MDIcon:
            icon: "play-circle-outline"
            font_size: "80sp"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 0.3 if not root.is_playing else 0
            pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDBoxLayout:
            orientation: 'vertical'
            adaptive_size: True
            pos_hint: {"right": 0.98, "center_y": 0.5}
            spacing: "15dp"

            MDBoxLayout:
                orientation: 'vertical'
                adaptive_size: True
                MDIconButton:
                    icon: "heart"
                    theme_icon_color: "Custom"
                    icon_color: (1, 0.2, 0.4, 1) if root.is_liked else (1, 1, 1, 1)
                    user_font_size: str(root.like_size) + "sp"
                    on_release: root.press_like()
                MDLabel:
                    text: "-1"
                    halign: "center"
                    font_style: "Caption"
                    text_color: 1,1,1,1

            MDIconButton:
                icon: "comment-text-multiple"
                theme_icon_color: "Custom"
                icon_color: 1, 1, 1, 1
                on_release: app.open_comments()

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: "110dp"
            padding: "15dp"
            pos_hint: {"bottom": 1}
            MDLabel:
                text: root.username
                bold: True
                text_color: 1, 1, 1, 1
            MDLabel:
                text: root.description
                font_style: "Caption"
                text_color: 1, 1, 1, 0.8

MDFloatLayout:
    md_bg_color: 0, 0, 0, 1

    MDBoxLayout:
        orientation: 'vertical'
        ScreenManager:
            id: screen_manager
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
                    MDTopAppBar:
                        title: "danya_looky"
                        anchor_title: "center"
                        md_bg_color: 0, 0, 0, 1
                        elevation: 0

                    ScrollView:
                        MDBoxLayout:
                            orientation: 'vertical'
                            adaptive_height: True
                            padding: "20dp"
                            spacing: "20dp"

                            MDBoxLayout:
                                adaptive_height: True
                                spacing: "20dp"
                                MDFloatLayout:
                                    size_hint: None, None
                                    size: "80dp", "80dp"
                                    canvas.before:
                                        Color:
                                            rgba: 0.15, 0.15, 0.15, 1
                                        Ellipse:
                                            pos: self.pos
                                            size: self.size
                                    MDIcon:
                                        icon: "account-circle"
                                        font_size: "80sp"
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}

                                MDGridLayout:
                                    cols: 3
                                    spacing: "10dp"
                                    adaptive_height: True
                                    pos_hint: {"center_y": 0.5}

                                    MDBoxLayout:
                                        orientation: 'vertical'
                                        adaptive_height: True
                                        MDLabel:
                                            text: "0"
                                            bold: True
                                            halign: "center"
                                        MDLabel:
                                            text: "Подписки"
                                            font_style: "Caption"
                                            halign: "center"

                                    MDBoxLayout:
                                        orientation: 'vertical'
                                        adaptive_height: True
                                        MDLabel:
                                            text: "0"
                                            bold: True
                                            halign: "center"
                                        MDLabel:
                                            text: "Подписчики"
                                            font_style: "Caption"
                                            halign: "center"

                                    MDBoxLayout:
                                        orientation: 'vertical'
                                        adaptive_height: True
                                        MDLabel:
                                            text: "0"
                                            bold: True
                                            halign: "center"
                                        MDLabel:
                                            text: "Лайки"
                                            font_style: "Caption"
                                            halign: "center"

                            MDBoxLayout:
                                orientation: 'vertical'
                                adaptive_height: True
                                spacing: "4dp"
                                MDLabel:
                                    text: "Даня"
                                    bold: True
                                    adaptive_height: True
                                MDLabel:
                                    text: "Я даун"
                                    font_style: "Caption"
                                    adaptive_height: True

                            MDRaisedButton:
                                text: "Редактировать профиль"
                                md_bg_color: 0.2, 0.2, 0.2, 1
                                size_hint_x: 1
                                elevation: 0

    MDBoxLayout:
        size_hint_y: None
        height: "55dp"
        pos_hint: {"bottom": 1}
        md_bg_color: 0, 0, 0, 1
        MDIconButton:
            icon: "home-variant"
            size_hint_x: 0.5
            on_release: screen_manager.current = 'feed_screen'; app.resume_current_video()
        MDIconButton:
            icon: "account"
            size_hint_x: 0.5
            on_release: screen_manager.current = 'profile_screen'; app.stop_all_videos()
'''

class TikTokApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.root_widget = Builder.load_string(KV)
        self.posts_list = []
        self.current_idx = 0

        carousel = self.root_widget.ids.slide_container
        base_path = os.path.dirname(os.path.abspath(__file__))

        posts_data = [
            {"u": "@Даня", "d": "Looky Beta запущен! ✅", "v": "1.mp4"},
            {"u": "@Даня", "d": "Разработка Kivy #python", "v": "2.mp4"},
        ]

        for data in posts_data:
            v_path = os.path.join(base_path, 'videos', data["v"])
            post = VideoPost(username=data["u"], description=data["d"], video_source=v_path)
            carousel.add_widget(post)
            self.posts_list.append(post)

        if self.posts_list:
            self.posts_list[0].is_playing = True
        return self.root_widget

    def open_comments(self):
        self.panel = CommentsPanel(pos_hint={"top": 0})
        self.root_widget.add_widget(self.panel)
        anim = Animation(pos_hint={"top": 0.75}, duration=0.25, t='out_quad')
        anim.start(self.panel)

    def add_comment(self, field):
        if field.text.strip():
            new_item = OneLineAvatarListItem(text=field.text, theme_text_color="Custom", text_color=[1, 1, 1, 1])
            new_item.add_widget(IconLeftWidget(icon="account-circle"))
            self.panel.ids.comments_list.add_widget(new_item)
            field.text = ""

    def stop_all_videos(self):
        for post in self.posts_list:
            post.is_playing = False

    def resume_current_video(self):
        if self.posts_list:
            self.posts_list[self.current_idx].is_playing = True

    def manage_video_playback(self, index):
        self.current_idx = index
        for i, post in enumerate(self.posts_list):
            post.is_playing = (i == index)

if __name__ == "__main__":
    TikTokApp().run()
