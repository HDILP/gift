import sys, json
import requests
from math import ceil
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPainterPath, QColor, QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QFrame, QGraphicsDropShadowEffect, QHBoxLayout, QGridLayout, QSizePolicy, QGraphicsBlurEffect


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Profile')
        self.setGeometry(100, 100, 1920, 1080)
    
        # 设置背景图片
        self.set_background_image("bg2.png")
    
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
    QScrollArea {
        background: rgba(254, 223, 225, 0); /* 半透明白色背景 */
        border-radius: 15px;
        border: 1px solid rgba(0, 0, 0, 0);
    }
    QScrollBar:vertical {
        width: 12px;
        background: transparent;
    }
    QScrollBar::handle:vertical {
        background: #3498db;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background: #2980b9;
    }
""")


        self.layout.addWidget(self.post_area)
    
        # 创建文章内容部件，并使其背景透明
        self.scroll_widget = QWidget(self)
        self.scroll_widget.setStyleSheet("background: transparent;")  # 保持透明
        self.post_area.setWidget(self.scroll_widget)
        self.post_area.setWidgetResizable(True)
    
        # 文章内容显示区域的布局
        self.posts_layout = QVBoxLayout(self.scroll_widget)
    
        # 加载用户信息和文章
        self.load_user_data()
        self.load_posts()

        # 页面底部分割线
        footer_divider = QFrame(self)
        footer_divider.setFrameShape(QFrame.HLine)
        footer_divider.setStyleSheet("""
            background: qlineargradient(
                spread: pad, x1:0, y1:0, x2:1, y2:0,
                stop: 0 rgba(255, 170, 178, 0),
                stop: 0.5 rgba(255, 170, 178, 0.8),
                stop: 1 rgba(255, 170, 178, 0)
            );
            height: 2px;
            border: none;
        """)
        self.layout.addWidget(footer_divider)

    def add_shadow(self, widget, blur_radius=15, offset=(0, 5), color=QColor(0, 0, 0, 100)):
        """
        为指定控件添加阴影效果。
        :param widget: 需要添加阴影的控件
        :param blur_radius: 阴影模糊半径
        :param offset: 阴影的偏移量 (x, y)
        :param color: 阴影的颜色
        """
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur_radius)
        shadow.setOffset(*offset)
        shadow.setColor(color)
        widget.setGraphicsEffect(shadow)
        
    def add_shadows_to_labels(self, parent_widget):
        """
        为父控件内的所有 QLabel 添加阴影效果。
        :param parent_widget: 父控件
        """
        for child in parent_widget.findChildren(QLabel):
            self.add_shadow(child, blur_radius=10, offset=(0, 2), color=QColor(0, 0, 0, 120))


    def set_background_image(self, image_path):
        """
        设置主窗口的背景图片。
        """
        self.setStyleSheet(f"""
            QMainWindow {{
                background-image: url({image_path});
                background-position: center;
                background-repeat: no-repeat;
            }}
        """)

    def create_profile_info(self):
        # 主框架
        profile_frame = QFrame(self)
        profile_frame.setStyleSheet("""
            background-color: rgba(254, 223, 225, 0.3); /* 半透明白色 */
            border-radius: 20px;
            padding: 15px;
            border: 1px solid rgba(0, 0, 0, 0);
        """)
    
        # 添加阴影
        self.add_shadow(profile_frame, blur_radius=20, offset=(0, 8), color=QColor(0, 0, 0, 100))
    
        # 栅格布局
        profile_layout = QGridLayout(profile_frame)
    
        # 头像部分
        self.avatar_label = QLabel(self)
        self.avatar_label.setStyleSheet("""
            border-radius: 50%; /* 圆形头像 */
            background-color: #f0f0f0; /* 默认背景 */
        """)
        self.avatar_label.setFixedSize(150, 150)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.add_shadow(self.avatar_label, blur_radius=15, offset=(0, 5), color=QColor(0, 0, 0, 80))
        profile_layout.addWidget(self.avatar_label, 0, 0, 2, 1, Qt.AlignCenter)
    
        # 文本部分
        text_layout = QVBoxLayout()
    
        # 用户名
        self.username_label = QLabel('@YourUsername', self)
        self.username_label.setStyleSheet("""
            font-size: 22px;
            color: #F596AA;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        self.username_label.setAlignment(Qt.AlignLeft)
        self.add_shadow(self.username_label, blur_radius=10, offset=(0, 2), color=QColor(0, 0, 0, 120))
        text_layout.addWidget(self.username_label)
    
        # 简介
        self.bio_label = QLabel('This is your bio. Add something interesting here!', self)
        self.bio_label.setStyleSheet("""
            font-size: 16px;
            color: #B19693;
        """)
        self.bio_label.setWordWrap(True)
        self.bio_label.setAlignment(Qt.AlignLeft)
        self.add_shadow(self.bio_label, blur_radius=10, offset=(0, 2), color=QColor(0, 0, 0, 100))
        text_layout.addWidget(self.bio_label)
    
        profile_layout.addLayout(text_layout, 0, 1, 1, 2)
    
        # 添加分割线
        divider = QFrame(self)
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("""
            background: qlineargradient(
                spread: pad, x1:0, y1:0, x2:1, y2:0,
                stop: 0 rgba(255, 170, 178, 0),
                stop: 0.5 rgba(255, 170, 178, 0.8),
                stop: 1 rgba(255, 170, 178, 0)
            );
            height: 2px;
            border: none;
        """)
        self.layout.addWidget(profile_frame)
        self.layout.addWidget(divider)


    def create_post_card(self, post):
        """
        创建一张优化后的文章卡片，增加卡片高度。
        """
        # 创建卡片框架
        card = QFrame(self)
        card.setStyleSheet("""
            background-color: rgba(254, 223, 225, 0.1);  /* 提高透明度 */
            border-radius: 12px;
            padding: 15px;
            border: 1px solid rgba(0, 0, 0, 0);
        """)
        self.add_shadow(card, blur_radius=30, offset=(0, 8), color=QColor(0, 0, 0, 100))
        
        # 设置卡片最小高度
        card.setMinimumHeight(250)  # 调整高度
    
        # 卡片主布局
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_layout.setSpacing(10)
    
        # 上半部分布局（图片和标题+内容）
        top_layout = QHBoxLayout()
    
        # 图片部分
        if "thumb" in post and post["thumb"]:
            image_label = QLabel(card)
            image_pixmap = QPixmap()
            image_pixmap.loadFromData(requests.get(post["thumb"]).content)
    
            # 使用原逻辑动态调整图片高度
            fixed_width = 200
            scaled_pixmap = image_pixmap.scaledToWidth(fixed_width, Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setStyleSheet("border-radius: 10px;")  # 圆角图片
            top_layout.addWidget(image_label)
    
        # 文本部分
        text_layout = QVBoxLayout()
    
        # 标题
        title_label = QLabel(post.get("title", "Untitled"), card)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #F8C3CD;
            margin-bottom: 5px;
            background: transparent;
        """)
        title_label.setWordWrap(True)
        # self.add_shadow(title_label, blur_radius=10, offset=(0, 3), color=QColor(0, 0, 0, 120))
        text_layout.addWidget(title_label)
    
        # 内容
        content_label = QLabel(json.loads(post.get("content", "")).get('text'), card)
        content_label.setStyleSheet("""
            font-size: 14px;
            color: #FEDFE1;
            background: transparent;
        """)
        content_label.setWordWrap(True)
        text_layout.addWidget(content_label)
    
        # 将文本部分添加到上半部分
        top_layout.addLayout(text_layout)
        card_layout.addLayout(top_layout)

        return card

        
    def get_api(self, types):
        url1 = "https://api.yaerxing.com/GetSTUserData"
        url2 = "https://api.yaerxing.com/GetSTUserNotes2"

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
            data = requests.post(url1, data=payload1, headers=headers).json()
            return data
        
        elif types == 'notes': 
            notes = requests.post(url2, data=payload2, headers=headers).json()
            return notes

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
            print("Starting load_posts...")
    
            # 强制重置 scroll_widget
            self.scroll_widget.deleteLater()  # 删除旧的 widget
            self.scroll_widget = QWidget(self)
            self.scroll_widget.setStyleSheet("background: transparent;")  # 保持透明
            self.post_area.setWidget(self.scroll_widget)
    
            # 创建新的布局
            main_layout = QHBoxLayout()
            left_column = QVBoxLayout()
            right_column = QVBoxLayout()
            main_layout.addLayout(left_column, 1)
            main_layout.addLayout(right_column, 1)
    
            for index, post in enumerate(posts):
                card = self.create_post_card(post)
                if index % 2 == 0:
                    left_column.addWidget(card)
                else:
                    right_column.addWidget(card)
    
            left_column.addStretch()
            right_column.addStretch()
    
            # 设置布局
            print("Setting new layout...")
            self.scroll_widget.setLayout(main_layout)
            print("New layout set successfully.")
    
        except Exception as e:
            print(f"Error in load_posts: {e}")
    
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font_id = QFontDatabase.addApplicationFont("./GenJyuuGothicX-Regular.ttf")
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

    font = QFont(font_family, 12)
    app.setFont(font)
    app.setStyle('Fusion')  # 使用 Fusion 样式

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

