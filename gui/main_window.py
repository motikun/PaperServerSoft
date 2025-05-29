import tkinter as tk
from create import open_create_window  # create.py 側で関数として定義しておく

def launch_app():
    root = tk.Tk()
    root.state('zoomed')
    root.title("ランチャー")

    tk.Button(root, text="PaperMCサーバー作成", command=open_create_window).pack(pady=20)

    root.mainloop()