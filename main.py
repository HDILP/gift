from PyQt5 import uic, QtWidgets, QtGui, QtCore
import json
import requests

class ProfileApp(QtWidgets.QMainWindow):
    def __init__(self, json_data):
        super().__init__()
        # Load UI file
        uic.loadUi("profile.ui", self)  # 替换为实际路径
        
        # Parse JSON data
        self.json_data = json_data
        
        # UI Elements
        self.name_label = self.findChild(QtWidgets.QLabel, "nameLabel")
        self.article_list = self.findChild(QtWidgets.QListWidget, "articleListWidget")
        self.article_content = self.findChild(QtWidgets.QTextBrowser, "contentBrowser")
        self.image_label = self.findChild(QtWidgets.QLabel, "imageLabel")
        
        # Populate UI
        self.populate_user_info()
        self.populate_articles()
        
        # Connect signals
        self.article_list.itemClicked.connect(self.display_article_details)
    
    def populate_user_info(self):
        """Populate user information from JSON."""
        if 'notes' in self.json_data and self.json_data['notes']:
            # Assume the first note contains user information
            user_info = self.json_data['notes'][0]
            self.name_label.setText(user_info.get('nick_name', '未知用户'))
    
    def populate_articles(self):
        """Populate article titles into the list widget."""
        for note in self.json_data.get('notes', []):
            title = note.get('title', '无标题')
            item = QtWidgets.QListWidgetItem(title)
            item.setData(QtCore.Qt.UserRole, note)  # Store full note data in the item
            self.article_list.addItem(item)
    
    def display_article_details(self, item):
        """Display selected article details."""
        note = item.data(QtCore.Qt.UserRole)
        content = json.loads(note.get('content', '{}')).get('text', '')
        urls = json.loads(note.get('urls', '[]'))
        
        # Update content and image
        self.article_content.setText(content or "暂无内容")
        if urls:
            # Load first image URL as an example
            image_path = urls[0]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(self.download_image(image_path))
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.clear()
    
    def download_image(self, url):
        """Download an image from the given URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"Failed to download image: {e}")
            return b''

url = "https://api.yaerxing.com/GetSTUserNotes2"

payload = {
  'unionid': "otJFa09hMXKizNDdufEyjjTEKkAw",
  'api_sig': "0F9677B8D2505C04B51E8A0779FABD69",
  'openid': "okvxLv2YTrsRnrp7JdtAZXtdzi60",
  'channel': "none",
  'type': "0",
  'app_c': "143",
  'call_id': "1733500304586",
  'os_v': "32",
  'um_token': "",
  'rom': "HUAWEI",
  'app_v': "1.14.3",
  'api_key': "9608ebc12b0dcfac257dd071357e3c2c",
  'appid': "wx2bd42ba7f4c547f5",
  'device_token': "",
  'platform_id': "2",
  'model': "NCO-AL00",
  'home_id': "15641558",
  'page': "0",
  'brand': "HUAWEI"
}

headers = {
  'User-Agent': "android",
  'Connection': "Keep-Alive",
  'Accept': "application/json",
  'Accept-Encoding': "gzip"
}

response = requests.post(url, data=payload, headers=headers)

json_data = response.json()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ProfileApp(json_data)
    window.show()
    sys.exit(app.exec_())
