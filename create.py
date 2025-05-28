import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import os
import threading

# ---------- API処理 ----------
def get_paper_versions():
    try:
        res = requests.get("https://api.papermc.io/v2/projects/paper")
        res.raise_for_status()
        return res.json()["versions"]
    except Exception as e:
        print("バージョン取得失敗:", e)
        return ["取得失敗"]

def get_latest_build(version):
    try:
        url = f"https://api.papermc.io/v2/projects/paper/versions/{version}"
        res = requests.get(url)
        res.raise_for_status()
        builds = res.json()["builds"]
        return builds[-1]
    except Exception as e:
        print("ビルド取得失敗:", e)
        return None

# ---------- GUIイベント ----------
def select_directory():
    folder = filedialog.askdirectory()
    if folder:
        selected_directory.set(folder)

def create_eula_and_start_bat(save_dir, jar_name):
    try:
        with open(os.path.join(save_dir, "eula.txt"), "w", encoding="utf-8") as f:
            f.write("eula=true\n")
        with open(os.path.join(save_dir, "start.bat"), "w", encoding="utf-8") as f:
            f.write(f"@echo off\n")
            f.write(f"java -Xms{memory_xms.get()}G -Xmx{memory_xmx.get()}G -jar {jar_name} nogui\n")
            f.write("pause\n")
    except Exception as e:
        messagebox.showerror("エラー", f"ファイル作成失敗: {e}")

def download_paper_jar():
    version = selected_version.get()
    build = get_latest_build(version)

    if not build:
        messagebox.showerror("エラー", "ビルドの取得に失敗しました")
        return

    folder = selected_directory.get()
    folder_name = server_folder_name.get()
    xms = memory_xms.get()
    xmx = memory_xmx.get()

    if not folder or not folder_name or not xms or not xmx:
        messagebox.showerror("エラー", "全ての項目を入力してください")
        return
    if not xms.isdigit() or not xmx.isdigit():
        messagebox.showerror("エラー", "メモリ値は数字で入力してください")
        return

    jar_name = f"paper-{version}-{build}.jar"
    target_dir = os.path.join(folder, folder_name)
    save_path = os.path.join(target_dir, jar_name)

    def download_thread():
        try:
            os.makedirs(target_dir, exist_ok=True)
            url = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build}/downloads/{jar_name}"
            res = requests.get(url, stream=True)
            res.raise_for_status()

            with open(save_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)

            create_eula_and_start_bat(target_dir, jar_name)
            messagebox.showinfo("成功", "サーバーを構築しました")
        except Exception as e:
            messagebox.showerror("エラー", f"ダウンロード失敗: {e}")

    threading.Thread(target=download_thread).start()

# ---------- GUI構築 ----------
root = tk.Tk()
root.title("PaperMCサーバーダウンローダー")
root.resizable(False, False)

# 変数定義
selected_version = tk.StringVar()
selected_directory = tk.StringVar()
server_folder_name = tk.StringVar()
memory_xms = tk.StringVar()
memory_xmx = tk.StringVar()

# バリデーション関数と登録
def validate_number(new_value):
    return new_value.isdigit() or new_value == ""

vcmd = (root.register(validate_number), "%P")

# バージョン選択
tk.Label(root, text="PaperMCのバージョンを選択").pack(pady=(10, 0))
version_combobox = ttk.Combobox(root, textvariable=selected_version, values=get_paper_versions(), state="readonly")
version_combobox.current(0)
version_combobox.pack(pady=5)

# フォルダ名
tk.Label(root, text="サーバーフォルダ名").pack(pady=(10, 0))
tk.Entry(root, textvariable=server_folder_name, width=30).pack(pady=5)

# 保存先ディレクトリ
tk.Label(root, text="ディレクトリ").pack(pady=(10, 0))
dir_frame = tk.Frame(root)
dir_frame.pack(pady=5)
tk.Entry(dir_frame, textvariable=selected_directory, state="readonly", width=40).pack(side="left", padx=(0, 5))
tk.Button(dir_frame, text="参照", command=select_directory).pack(side="left")

# メモリ設定
tk.Label(root, text="Xms（最小メモリ）").pack()
tk.Entry(root, textvariable=memory_xms, validate="key", validatecommand=vcmd, width=10).pack()
tk.Label(root, text="Xmx（最大メモリ）").pack()
tk.Entry(root, textvariable=memory_xmx, validate="key", validatecommand=vcmd, width=10).pack()

# 実行ボタン
tk.Button(root, text="サーバーを構築", command=download_paper_jar).pack(pady=15)

# 実行
root.mainloop()
