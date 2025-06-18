import tkinter as tk

class DrawApp:
    def __init__(self, master):
        self.master = master
        master.title("Simple Draw App")

        # 現在のツール: "rect", "oval", "line", "triangle"
        self.current_tool = "line"
        self.start_x = None
        self.start_y = None
        self.temp_item = None
        self.triangle_points = []
        self.triangle_previews = []

        # ツールボタンフレーム
        tool_frame = tk.Frame(master)
        tool_frame.pack(side=tk.TOP, fill=tk.X)

        for tool, text in [
            ("line", "線"),
            ("rect", "四角形"),
            ("oval", "円／楕円"),
            ("triangle", "三角形")
        ]:
            btn = tk.Button(tool_frame, text=text,
                            command=lambda t=tool: self.select_tool(t))
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        clear_btn = tk.Button(tool_frame, text="クリア", command=self.clear_canvas)
        clear_btn.pack(side=tk.RIGHT, padx=2, pady=2)

        # 描画キャンバス
        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # マウスイベントバインド
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def select_tool(self, tool):
        self.current_tool = tool
        self.triangle_points.clear()
        for preview in self.triangle_previews:
            self.canvas.delete(preview)
        self.triangle_previews.clear()

    def clear_canvas(self):
        self.canvas.delete("all")
        self.triangle_points.clear()
        self.triangle_previews.clear()

    def on_button_press(self, event):
        if self.current_tool == "triangle":
            # 三角形はクリック3回で描画
            self.triangle_points.append((event.x, event.y))
            n = len(self.triangle_points)
            # プレビュー点を小さく表示
            dot = self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3,
                                          fill="red")
            self.triangle_previews.append(dot)
            if n > 1:
                # 前の点から線を引く
                x0, y0 = self.triangle_points[-2]
                line = self.canvas.create_line(x0, y0, event.x, event.y, dash=(2,2))
                self.triangle_previews.append(line)
            if n == 3:
                # 3点目でポリゴンを描画
                pts = [coord for point in self.triangle_points for coord in point]
                self.canvas.create_polygon(*pts, outline="black", fill="", width=2)
                # プレビューを削除
                for item in self.triangle_previews:
                    self.canvas.delete(item)
                self.triangle_points.clear()
                self.triangle_previews.clear()
        else:
            # 他のツールはドラッグで描画
            self.start_x = event.x
            self.start_y = event.y
            if self.current_tool == "rect":
                self.temp_item = self.canvas.create_rectangle(event.x, event.y, event.x, event.y,
                                                              outline="black")
            elif self.current_tool == "oval":
                self.temp_item = self.canvas.create_oval(event.x, event.y, event.x, event.y,
                                                         outline="black")
            elif self.current_tool == "line":
                self.temp_item = self.canvas.create_line(event.x, event.y, event.x, event.y,
                                                         fill="black")

    def on_mouse_drag(self, event):
        if self.current_tool in ("rect", "oval", "line") and self.temp_item:
            # プレビューを更新
            if self.current_tool == "line":
                self.canvas.coords(self.temp_item, self.start_x, self.start_y, event.x, event.y)
            else:
                self.canvas.coords(self.temp_item, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        if self.current_tool in ("rect", "oval", "line"):
            # 描画確定（temp_itemは残す）
            self.temp_item = None
            self.start_x = None
            self.start_y = None

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawApp(root)
    root.mainloop()
