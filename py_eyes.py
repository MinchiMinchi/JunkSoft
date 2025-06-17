import tkinter as tk
import math

class Eye:
    def __init__(self, canvas, x, y, radius=50, pupil_radius=15):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = radius
        self.pr = pupil_radius
        # 目玉（白目）
        self.eye_id = canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill='white', outline='black', width=2
        )
        # 瞳（黒目）
        self.pupil_id = canvas.create_oval(
            x - pupil_radius, y - pupil_radius,
            x + pupil_radius, y + pupil_radius,
            fill='black'
        )

    def look_at(self, mouse_x, mouse_y):
        # 目の中心からマウス位置へのベクトル
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        # 距離
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        # 瞳を白目の内側に収めるための係数
        max_dist = self.r - self.pr - 2
        factor = min(max_dist / dist, 1)
        # 瞳の新しい中心位置
        nx = self.x + dx * factor
        ny = self.y + dy * factor
        # 瞳を移動
        self.canvas.coords(
            self.pupil_id,
            nx - self.pr, ny - self.pr,
            nx + self.pr, ny + self.pr
        )

class XEyesApp:
    def __init__(self, width=400, height=200):
        self.root = tk.Tk()
        self.root.title("Python xeyes Toy")
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg='lightblue')
        self.canvas.pack()
        # 左右の目を配置
        self.eyes = [
            Eye(self.canvas, width*0.3, height*0.5),
            Eye(self.canvas, width*0.7, height*0.5)
        ]
        # マウス移動イベントをバインド
        self.canvas.bind('<Motion>', self.on_mouse_move)

    def on_mouse_move(self, event):
        for eye in self.eyes:
            eye.look_at(event.x, event.y)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = XEyesApp()
    app.run()
