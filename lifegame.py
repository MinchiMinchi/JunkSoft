import tkinter as tk
import numpy as np

class GameOfLife:
    def __init__(self, master, rows=50, cols=50, cell_size=10, interval=100):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.interval = interval  # ミリ秒
        self.running = False

        # グリッド (0: 死, 1: 生)
        self.grid = np.zeros((rows, cols), dtype=int)

        # Canvas の準備
        width = cols * cell_size
        height = rows * cell_size
        self.canvas = tk.Canvas(master, width=width, height=height, bg='white')
        self.canvas.pack()

        # ボタン
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="ランダム初期化", command=self.randomize).pack(side='left', padx=5)
        self.start_btn = tk.Button(btn_frame, text="開始", command=self.toggle_running)
        self.start_btn.pack(side='left', padx=5)
        tk.Button(btn_frame, text="ステップ", command=self.step).pack(side='left', padx=5)
        tk.Button(btn_frame, text="クリア", command=self.clear).pack(side='left', padx=5)

        # クリックでセルのオン・オフ切り替え
        self.canvas.bind("<Button-1>", self.on_click)

        # 描画用セル ID 配列
        self.rects = [
            [None]*cols
            for _ in range(rows)
        ]
        for r in range(rows):
            for c in range(cols):
                x0 = c * cell_size
                y0 = r * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                rect = self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill='white', outline='lightgray'
                )
                self.rects[r][c] = rect

    def randomize(self):
        self.grid = np.random.randint(2, size=(self.rows, self.cols))
        self.draw()

    def clear(self):
        self.grid.fill(0)
        self.draw()

    def toggle_running(self):
        self.running = not self.running
        self.start_btn.config(text="停止" if self.running else "開始")
        if self.running:
            self.run()

    def run(self):
        if not self.running:
            return
        self.step()
        self.master.after(self.interval, self.run)

    def step(self):
        new = np.zeros_like(self.grid)
        for r in range(self.rows):
            for c in range(self.cols):
                # 8 近傍の合計
                total = (
                    self.grid[(r-1)%self.rows, (c-1)%self.cols] +
                    self.grid[(r-1)%self.rows, c] +
                    self.grid[(r-1)%self.rows, (c+1)%self.cols] +
                    self.grid[r, (c-1)%self.cols] +
                    self.grid[r, (c+1)%self.cols] +
                    self.grid[(r+1)%self.rows, (c-1)%self.cols] +
                    self.grid[(r+1)%self.rows, c] +
                    self.grid[(r+1)%self.rows, (c+1)%self.cols]
                )
                if self.grid[r, c] == 1 and total in (2, 3):
                    new[r, c] = 1
                elif self.grid[r, c] == 0 and total == 3:
                    new[r, c] = 1
        self.grid = new
        self.draw()

    def draw(self):
        for r in range(self.rows):
            for c in range(self.cols):
                color = 'black' if self.grid[r, c] else 'white'
                self.canvas.itemconfig(self.rects[r][c], fill=color)

    def on_click(self, event):
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r, c] = 1 - self.grid[r, c]
            self.draw()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Conway's Game of Life")
    app = GameOfLife(root, rows=60, cols=80, cell_size=8, interval=180)
    root.mainloop()
