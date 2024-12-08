import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPainterPath, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QFrame, QGraphicsDropShadowEffect, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Profile')
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet("background-color: #f5f7fa;")  # 设置整体背景色

        # 创建主窗口内容
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # 创建布局
        self.layout = QVBoxLayout(self.main_widget)

        # 创建头像、用户名、简介
        self.create_profile_info()

        # 创建文章显示区域
        self.post_area = QScrollArea(self)
        self.post_area.setStyleSheet("""
            QScrollArea { border: none; }
            QScrollBar:vertical {
                width: 10px;
                background: #f5f7fa;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                border-radius: 5px;
            }
        """)
        self.layout.addWidget(self.post_area)

        self.scroll_widget = QWidget()
        self.post_area.setWidget(self.scroll_widget)
        self.post_area.setWidgetResizable(True)

        # 文章内容显示区域的布局
        self.posts_layout = QVBoxLayout(self.scroll_widget)

        # 加载用户信息和文章
        self.load_user_data()
        self.load_posts()
    def get_api(self, types):
        url = "https://api.yaerxing.com/GetSTUserData"

        payload1 = {
        'unionid': "otJFa09hMXKizNDdufEyjjTEKkAw",
        'api_sig': "F1C2697129FB85A425DA7C4EE459F424",
        'openid': "okvxLv2YTrsRnrp7JdtAZXtdzi60",
        'channel': "none",
        'app_c': "143",
        'call_id': "1733638404230",
        'os_v': "32",
        'um_token': "",
        'rom': "HUAWEI",
        'app_v': "1.14.3",
        'api_key': "9608ebc12b0dcfac257dd071357e3c2c",
        'appid': "wx2bd42ba7f4c547f5",
        'device_token': "",
        'platform_id': "2",
        'model': "NCO-AL00",
        'home_id': "otJFa09hMXKizNDdufEyjjTEKkAw",
        'brand': "HUAWEI"
        }

        payload2 = {
        'unionid': "otJFa09hMXKizNDdufEyjjTEKkAw",
        'api_sig': "33BCE58DE343A6F2EF4803C5B586E66A",
        'openid': "okvxLv2YTrsRnrp7JdtAZXtdzi60",
        'channel': "none",
        'type': "0",
        'app_c': "143",
        'call_id': "1733638404500",
        'os_v': "32",
        'um_token': "",
        'rom': "HUAWEI",
        'app_v': "1.14.3",
        'api_key': "9608ebc12b0dcfac257dd071357e3c2c",
        'appid': "wx2bd42ba7f4c547f5",
        'device_token': "",
        'platform_id': "2",
        'model': "NCO-AL00",
        'home_id': "otJFa09hMXKizNDdufEyjjTEKkAw",
        'page': "0",
        'brand': "HUAWEI"
        }
        
        headers = {
        'User-Agent': "android",
        'Connection': "Keep-Alive",
        'Accept': "application/json",
        'Accept-Encoding': "gzip"
        }

        if types == 'data':
            data = requests.post(url, data=payload1, headers=headers).json()
            return data
        
        elif types == 'notes': 
            notes = requests.post(url, data=payload2, headers=headers).json()
            return notes
    def create_profile_info(self):
        profile_frame = QFrame(self)
        profile_frame.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #ddd;
        """)
        profile_layout = QHBoxLayout(profile_frame)

        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(5, 5)
        shadow.setColor(QColor(0, 0, 0, 80))
        profile_frame.setGraphicsEffect(shadow)

        # 头像
        self.avatar_label = QLabel(self)
        self.avatar_label.setStyleSheet("border-radius: 75px; background-color: transparent;")
        self.avatar_label.setFixedSize(150, 150)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        profile_layout.addWidget(self.avatar_label)

        # 用户名与简介
        text_layout = QVBoxLayout()
        self.username_label = QLabel('@YourUsername', self)
        self.username_label.setStyleSheet("font-size: 24px; color: #2c3e50; font-weight: bold;")
        text_layout.addWidget(self.username_label)

        self.bio_label = QLabel('This is your bio. Add something interesting here!', self)
        self.bio_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        text_layout.addWidget(self.bio_label)

        profile_layout.addLayout(text_layout)
        self.layout.addWidget(profile_frame)

    def load_user_data(self):
        try:
            user_data = self.get_api('data').get("info", {})

            # 加载头像
            avatar_url = user_data.get("logo")
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(avatar_url).content)

            # 调用裁剪函数，将头像裁剪为圆形
            circular_avatar = self.get_circular_pixmap(pixmap, 100)
            self.avatar_label.setPixmap(circular_avatar)

            # 加载用户名和简介
            self.username_label.setText(f"@ {user_data.get('nick_name')}")
            self.bio_label.setText('Power By HDILP')

        except requests.exceptions.RequestException as e:
            print(f"Error fetching user data: {e}")
            error_message = QLabel("Failed to load user data.", self)
            error_message.setStyleSheet("font-size: 14px; color: red;")
            self.layout.addWidget(error_message)

    def load_posts(self):
        try:
            posts = self.get_api('notes').get("notes", [])
            print(posts)
            # 遍历返回的文章数据并动态生成卡片
            for post in posts:
                card = self.create_post_card(post)
                self.posts_layout.addWidget(card)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            error_message = QLabel("Failed to load articles.", self)
            error_message.setStyleSheet("font-size: 14px; color: red;")
            self.posts_layout.addWidget(error_message)
    def get_circular_pixmap(self, pixmap, size):
        """
        将头像裁剪为圆形，并确保头像内容完整覆盖圆形区域。
        :param pixmap: 原始 QPixmap
        :param size: 圆形图像的直径
        :return: 裁剪后的圆形 QPixmap
        """
        # 缩放图片使其完全覆盖圆形区域
        scaled_pixmap = pixmap.scaled(size, size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # 创建一个与目标大小匹配的透明背景 QPixmap
        circular_pixmap = QPixmap(size, size)
        circular_pixmap.fill(Qt.transparent)

        # 使用 QPainter 绘制圆形遮罩
        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置圆形剪裁区域
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)

        # 将头像绘制到圆形区域
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()

        return circular_pixmap

    def create_post_card(self, post):
        # 创建卡片
        card = QFrame(self)
        card.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 10px;
            border: 1px solid #ddd;
            margin: 15px;
            padding: 15px;
        """)

        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setOffset(5, 5)
        shadow.setColor(QColor(0, 0, 0, 50))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)

        # 标题
        title = QLabel(post["title"], card)
        title.setStyleSheet("font-size: 20px; color: #2c3e50; font-weight: bold; margin-bottom: 10px;")
        card_layout.addWidget(title)

        # 内容
        content = QLabel(post["content"], card)
        content.setStyleSheet("font-size: 16px; color: #7f8c8d; margin-bottom: 10px;")
        content.setWordWrap(True)  # 自动换行
        card_layout.addWidget(content)

        return card


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用 Fusion 样式
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
