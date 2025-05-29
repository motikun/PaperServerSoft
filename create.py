from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QCheckBox, QHBoxLayout, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import requests
import os
import json

class DownloadThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, version, build, jar_name, target_dir, memory_xms, memory_xmx, folder_name_input):
        super().__init__()
        self.version = version
        self.build = build
        self.jar_name = jar_name
        self.target_dir = target_dir
        self.memory_xms = memory_xms
        self.memory_xmx = memory_xmx
        self.folder_name = folder_name_input

    def run(self):
        try:
            os.makedirs(self.target_dir, exist_ok=True)
            url = f"https://api.papermc.io/v2/projects/paper/versions/{self.version}/builds/{self.build}/downloads/{self.jar_name}"
            res = requests.get(url, stream=True)
            res.raise_for_status()
            save_path = os.path.join(self.target_dir, self.jar_name)

            with open(save_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)

            with open(os.path.join(self.target_dir, "eula.txt"), "w", encoding="utf-8") as f:
                f.write("eula=true\n")

            with open(os.path.join(self.target_dir, "start.bat"), "w", encoding="utf-8") as f:
                f.write(f"@echo off\n")
                f.write(f"java -Xms{self.memory_xms}G -Xmx{self.memory_xmx}G -jar {self.jar_name} nogui\n")
                f.write("pause\n")

            info_path = os.path.join(os.path.dirname(__file__), "servers.json")

            # 既にファイルがあれば読み込む、なければ空のリストを使う
            if os.path.exists(info_path):
                with open(info_path, "r", encoding="utf-8") as f:
                    try:
                        server_list = json.load(f)
                    except json.JSONDecodeError:
                        server_list = []
            else:
                server_list = []

            # 新しいサーバー情報を追加
            server_list.append({
                "name": self.folder_name,
                "dir": self.target_dir
            })

            # ファイルに書き戻す
            with open(info_path, "w", encoding="utf-8") as f:
                json.dump(server_list, f, indent=4, ensure_ascii=False)

            self.finished.emit("サーバーを構築しました")
        except Exception as e:
            self.error.emit(str(e))


class CreateServerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PaperMCサーバーダウンローダー")
        self.setFixedSize(400, 450)

        self.version_combo = QComboBox()
        self.folder_name_input = QLineEdit()
        self.directory_input = QLineEdit()
        self.xms_input = QLineEdit()
        self.xmx_input = QLineEdit()
        self.eula_checkbox = QCheckBox("EULAに同意します")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("PaperMCのバージョンを選択"))
        layout.addWidget(self.version_combo)

        layout.addWidget(QLabel("サーバーフォルダ名"))
        layout.addWidget(self.folder_name_input)

        layout.addWidget(QLabel("ディレクトリ"))
        dir_layout = QHBoxLayout()
        self.directory_input.setReadOnly(True)
        browse_button = QPushButton("参照")
        browse_button.clicked.connect(self.select_directory)
        dir_layout.addWidget(self.directory_input)
        dir_layout.addWidget(browse_button)
        layout.addLayout(dir_layout)

        layout.addWidget(QLabel("Xms（最小メモリ）"))
        layout.addWidget(self.xms_input)
        layout.addWidget(QLabel("Xmx（最大メモリ）"))
        layout.addWidget(self.xmx_input)

        layout.addWidget(self.eula_checkbox)

        self.start_button = QPushButton("サーバーを構築")
        self.start_button.clicked.connect(self.download_paper_jar)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        self.load_versions()

    def load_versions(self):
        try:
            res = requests.get("https://api.papermc.io/v2/projects/paper")
            res.raise_for_status()
            versions = res.json()["versions"]
            self.version_combo.addItems(versions)
        except Exception as e:
            self.version_combo.addItem("取得失敗")

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "ディレクトリ選択")
        if directory:
            self.directory_input.setText(directory)

    def download_paper_jar(self):
        version = self.version_combo.currentText()
        folder_name = self.folder_name_input.text()
        directory = self.directory_input.text()
        xms = self.xms_input.text()
        xmx = self.xmx_input.text()
        eula = self.eula_checkbox.isChecked()

        if not all([folder_name, directory, xms, xmx]):
            QMessageBox.critical(self, "エラー", "全ての項目を入力してください")
            return

        if not (xms.isdigit() and xmx.isdigit()):
            QMessageBox.critical(self, "エラー", "メモリ値は数字で入力してください")
            return

        if not eula:
            QMessageBox.critical(self, "エラー", "EULAに同意してください")
            return

        build = self.get_latest_build(version)
        if not build:
            QMessageBox.critical(self, "エラー", "ビルドの取得に失敗しました")
            return

        jar_name = f"paper-{version}-{build}.jar"
        target_dir = os.path.join(directory, folder_name)

        self.thread = DownloadThread(version, build, jar_name, target_dir, xms, xmx, folder_name)
        self.thread.finished.connect(lambda msg: QMessageBox.information(self, "成功", msg))
        self.thread.error.connect(lambda msg: QMessageBox.critical(self, "エラー", f"ダウンロード失敗: {msg}"))
        self.thread.start()

    def get_latest_build(self, version):
        try:
            url = f"https://api.papermc.io/v2/projects/paper/versions/{version}"
            res = requests.get(url)
            res.raise_for_status()
            return res.json()["builds"][-1]
        except Exception:
            return None
