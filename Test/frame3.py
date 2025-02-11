import tkinter as tk

class TransparentRectangleSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("透明矩形框选择器")

        self.canvas = tk.Canvas(root, width=800, height=600, bg='red')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 添加清除按钮
        self.clear_button = tk.Button(root, text="清除", command=self.clear_canvas)
        self.clear_button.pack(pady=10)

        self.rect_id = None
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

        # 鼠标点击次数
        self.clickNum = 0

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Motion>", self.on_move)

    def on_button_press(self, event):
        if self.clickNum <= 1:
            self.on_rect_click(event)
            self.clickNum += 1
            return

        self.clickNum = 0
        self.start_x = event.x
        self.start_y = event.y

        if self.rect_id:
            self.canvas.delete(self.rect_id)

        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='black', width=3
        )

    def on_move_press(self, event):
        if not self.rect_id:
            return
        self.clickNum = 0
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_button_release(self, event):
        pass

    def on_move(self, event):
        self.clickNum = 0

    def on_rect_click(self, event):
        if not self.rect_id:
            return
        x_percent, y_percent = self.get_percentage_coordinates(event.x, event.y)
        print(f"点击百分比坐标: {x_percent}, {y_percent}")

    def get_percentage_coordinates(self, click_x, click_y):
        x1, y1, x2, y2 = self.canvas.coords(self.rect_id)
        width = x2 - x1
        height = y2 - y1

        if width == 0 or height == 0:
            return (0, 0)

        x_percent = (click_x - x1) / width
        y_percent = (click_y - y1) / height

        return (x_percent, y_percent)

    def clear_canvas(self):
        # 清除所有图形
        self.canvas.delete("all")
        self.rect_id = None
        self.clickNum = 0  # 重置鼠标点击次数

def main():
    root = tk.Tk()
    app = TransparentRectangleSelector(root)
    root.mainloop()

if __name__ == "__main__":
    main()