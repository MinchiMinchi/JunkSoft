import tkinter as tk
import math

def koch_curve(p1, p2, depth):
    """ p1→p2 のコッホ曲線を depth 再帰で返す """
    if depth == 0:
        return [p1, p2]
    x1, y1 = p1; x5, y5 = p2
    # 分割点
    x2, y2 = (2*x1 + x5)/3, (2*y1 + y5)/3
    x4, y4 = (x1 + 2*x5)/3, (y1 + 2*y5)/3
    # とがった頂点（60° 回転）
    ux, uy = x4-x2, y4-y2
    ang = math.radians(60)
    x3 = x2 + ux*math.cos(ang) - uy*math.sin(ang)
    y3 = y2 + ux*math.sin(ang) + uy*math.cos(ang)

    pts = []
    segments = [
        (p1,   (x2, y2)),
        ((x2, y2), (x3, y3)),
        ((x3, y3), (x4, y4)),
        ((x4, y4), p2),
    ]
    for a, b in segments:
        seg = koch_curve(a, b, depth-1)
        if pts:
            seg = seg[1:]  # 重複点を除く
        pts += seg
    return pts

class KochZoomApp:
    def __init__(self, depth=5, size=800, max_depth=10):
        self.size = size
        # 表示領域（x_min, x_max, y_min, y_max）
        self.view_rect = [0, size, 0, size]
        # 再帰深さ
        self.depth = depth

        # 元データは depth に応じて毎回再計算
        self.base_pts = koch_curve((0, size/2), (size, size/2), self.depth)
        # 現在表示中の点列
        self.current_pts = list(self.base_pts)

        # TK ウィンドウ
        self.root = tk.Tk()
        self.root.title("Koch Curve Zoom (Depth 可変)")

        # 深さスライダー
        self.depth_slider = tk.Scale(
            self.root,
            from_=0,
            to=max_depth,
            orient=tk.HORIZONTAL,
            label="Depth",
            command=self.on_depth_change
        )
        self.depth_slider.set(self.depth)
        self.depth_slider.pack(fill='x', padx=10, pady=5)

        # 正方形 Canvas
        self.canvas = tk.Canvas(self.root, width=size, height=size, bg='white')
        self.canvas.pack()

        # 描画＆ズーム用イベント
        self._draw(self.current_pts)
        self.center = None
        self.zoom_rect = None

        self.canvas.bind("<ButtonPress-1>",    self.on_press)
        self.canvas.bind("<B1-Motion>",       self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        tk.Button(self.root, text="リセット", command=self.reset_view).pack(pady=5)

    def _draw(self, pts):
        self.canvas.delete("all")
        coords = []
        for x, y in pts:
            coords.extend((x, y))
        self.canvas.create_line(coords, fill='blue', width=1)

    def on_depth_change(self, val):
        # スライダーで depth が変わったとき
        self.depth = int(val)
        # 元データ再計算
        self.base_pts = koch_curve((0, self.size/2), (self.size, self.size/2), self.depth)
        # 現在の view_rect に合わせて再マッピング
        xmin, xmax, ymin, ymax = self.view_rect
        new_pts = []
        for x, y in self.base_pts:
            nx = (x - xmin) * self.size / (xmax - xmin)
            ny = (y - ymin) * self.size / (ymax - ymin)
            new_pts.append((nx, ny))
        self.current_pts = new_pts
        self._draw(self.current_pts)

    def on_press(self, e):
        self.center = (e.x, e.y)
        if self.zoom_rect:
            self.canvas.delete(self.zoom_rect)
            self.zoom_rect = None

    def on_drag(self, e):
        x0, y0 = self.center
        dx, dy = e.x - x0, e.y - y0
        half = max(abs(dx), abs(dy))
        x1, y1 = x0-half, y0-half
        x2, y2 = x0+half, y0+half
        if self.zoom_rect:
            self.canvas.coords(self.zoom_rect, x1, y1, x2, y2)
        else:
            self.zoom_rect = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline='red', dash=(4,4)
            )

    def on_release(self, e):
        x0, y0 = self.center
        dx, dy = e.x - x0, e.y - y0
        half = max(abs(dx), abs(dy))
        if half < 5:
            if self.zoom_rect:
                self.canvas.delete(self.zoom_rect)
                self.zoom_rect = None
            return

        xmin, ymin = x0-half, y0-half
        xmax, ymax = x0+half, y0+half
        # view_rect 更新
        self.view_rect = [xmin, xmax, ymin, ymax]

        # 現在表示中の点列を変換
        new_pts = []
        for x, y in self.current_pts:
            nx = (x0 - half <= x <= x0 + half) and (x - xmin) * self.size / (xmax - xmin) or None
            ny = (y0 - half <= y <= y0 + half) and (y - ymin) * self.size / (ymax - ymin) or None
            if nx is not None and ny is not None:
                new_pts.append((nx, ny))
        # フィルタ：正方形領域内の点のみ変換
        self.current_pts = new_pts
        self._draw(self.current_pts)

        if self.zoom_rect:
            self.canvas.delete(self.zoom_rect)
            self.zoom_rect = None

    def reset_view(self):
        self.view_rect = [0, self.size, 0, self.size]
        self.base_pts = koch_curve((0, self.size/2), (self.size, self.size/2), self.depth)
        self.current_pts = list(self.base_pts)
        self._draw(self.current_pts)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KochZoomApp(depth=5, size=600)
    app.run()
