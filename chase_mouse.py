import tkinter as tk
import pyautogui
import math

class MouseSprite:
    def __init__(self, canvas, x, y, size=40):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        s = size
        # 体
        self.body = canvas.create_oval(
            x - s*0.4, y - s*0.2, x + s*0.4, y + s*0.2,
            fill='gray', outline='black'
        )
        # 頭
        self.head = canvas.create_oval(
            x + s*0.3, y - s*0.25, x + s*0.6, y + s*0.05,
            fill='gray', outline='black'
        )
        # 耳
        self.ear1 = canvas.create_oval(
            x + s*0.35, y - s*0.35, x + s*0.45, y - s*0.25,
            fill='gray', outline='black'
        )
        self.ear2 = canvas.create_oval(
            x + s*0.45, y - s*0.35, x + s*0.55, y - s*0.25,
            fill='gray', outline='black'
        )
        # しっぽ
        self.tail = canvas.create_line(
            x - s*0.4, y + s*0.1,
            x - s*0.7, y + s*0.2,
            x - s*0.8, y + s*0.0,
            smooth=True, width=3, fill='pink'
        )
        self.parts = [self.body, self.head, self.ear1, self.ear2, self.tail]

    def move_towards(self, tx, ty, step=30):
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)
        if dist < 1:
            return
        # 一度に動く距離を step ピクセルに制限
        factor = min(step / dist, 1)
        move_x = dx * factor
        move_y = dy * factor
        # パーツ全体を移動
        for part in self.parts:
            self.canvas.move(part, move_x, move_y)
        # 中心座標を更新
        self.x += move_x
        self.y += move_y

class MouseChaseApp:
    def __init__(self, width=600, height=400, interval=50):
        self.root = tk.Tk()
        self.root.title("ネズミがマウスを追いかける")
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg='white')
        self.canvas.pack()
        # 初期位置は画面中央
        cx, cy = width/2, height/2
        self.mouse = MouseSprite(self.canvas, cx, cy, size=60)
        self.interval = interval
        self._poll()

    def _poll(self):
        # グローバルなマウス座標取得
        gx, gy = pyautogui.position()
        # ウィンドウ左上のスクリーン座標
        wx = self.root.winfo_rootx()
        wy = self.root.winfo_rooty()
        # キャンバス内の相対座標に変換
        rx = gx - wx
        ry = gy - wy
        # ネズミを更新
        self.mouse.move_towards(rx, ry)
        # 繰り返し
        self.root.after(self.interval, self._poll)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    # pyautogui の警告を抑制（必要なら）
    pyautogui.FAILSAFE = False
    app = MouseChaseApp()
    app.run()
