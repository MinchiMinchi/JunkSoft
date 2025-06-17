import tkinter as tk
import math
import pyautogui

class Eye:
    def __init__(self, canvas, x, y, radius=50, pupil_radius=15):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = radius
        self.pr = pupil_radius
        # 白目
        self.eye_id = canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill='white', outline='black', width=2
        )
        # 瞳
        self.pupil_id = canvas.create_oval(
            x - pupil_radius, y - pupil_radius,
            x + pupil_radius, y + pupil_radius,
            fill='black'
        )

    def look_at(self, mouse_x, mouse_y):
        # 目の中心からマウス位置へのベクトル
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        # 瞳が白目の外に出ないように最大移動距離を設定
        max_dist = self.r - self.pr - 2
        factor = min(max_dist / dist, 1)
        # 新しい瞳の中心座標
        nx = self.x + dx * factor
        ny = self.y + dy * factor
        # キャンバス上の瞳を移動
        self.canvas.coords(
            self.pupil_id,
            nx - self.pr, ny - self.pr,
            nx + self.pr, ny + self.pr
        )

class XEyesApp:
    def __init__(self, width=400, height=200, poll_interval=50):
        self.root = tk.Tk()
        self.root.title("Global xeyes Toy (pyautogui)")
        # キャンバスを作成
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg='lightblue')
        self.canvas.pack()
        # 左右の目を作成
        self.eyes = [
            Eye(self.canvas, width * 0.3, height * 0.5),
            Eye(self.canvas, width * 0.7, height * 0.5)
        ]
        # ポーリング間隔（ミリ秒）
        self.poll_interval = poll_interval
        # ポーリング開始
        self._poll_mouse()

    def _poll_mouse(self):
        # 画面全体のマウス座標を取得
        gx, gy = pyautogui.position()
        # ウィンドウ左上のスクリーン座標を取得
        wx = self.root.winfo_rootx()
        wy = self.root.winfo_rooty()
        # キャンバス上の相対座標に変換
        rx = gx - wx
        ry = gy - wy
        # 各目を更新
        for eye in self.eyes:
            eye.look_at(rx, ry)
        # 指定間隔で繰り返し
        self.root.after(self.poll_interval, self._poll_mouse)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = XEyesApp()
    app.run()
