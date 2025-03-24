import time
import tkinter as tk
from tkinter import messagebox
from spyder import Spyder
from judgment import ContentSafetyChecker


class TextQueryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("文本处理工具")
        self.geometry('600x400')
        self._setup_ui()
        self._style_config()
        self.query = ""
        self.data_list = []

    def _setup_ui(self):
        """构建界面元素"""
        # 输入控件容器
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10, padx=5, fill=tk.X)

        # 查询输入框（在查询按钮左侧）
        self.query_entry = tk.Entry(control_frame, width=25, font=("微软雅黑", 10))
        self.query_entry.pack(side=tk.LEFT, padx=(0, 5))

        # 操作按钮组
        self.btn_query = tk.Button(
            control_frame,
            text="查询(请按照2024年3月23日格式搜索)",
            command=self.execute_query,
            width=30
        )
        self.btn_query.pack(side=tk.LEFT)

        self.btn_clear = tk.Button(
            control_frame,
            text="清除内容",
            command=self.clear_content,
            width=10
        )
        self.btn_clear.pack(side=tk.LEFT, padx=(5, 0))

        self.btn_check = tk.Button(
            control_frame,
            text="查询违规文本",
            command=self.check_data,
            width=20
        )
        self.btn_check.pack(side=tk.LEFT)

        # 文本显示区域
        self.text_area = tk.Text(self, wrap=tk.WORD, font=("宋体", 11))
        self.text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def _style_config(self):
        """样式配置"""
        self.configure(bg="#F0F0F0")
        # 输入框样式
        self.query_entry.configure(
            bg="white",
            relief=tk.GROOVE,
            borderwidth=1
        )
        # 按钮样式
        self.btn_query.configure(
            bg="#4CAF50",  # 绿色按钮
            fg="white",
            activebackground="#45a049"
        )
        self.btn_clear.configure(
            bg="#f44336",  # 红色按钮
            fg="white",
            activebackground="#d32f2f"
        )
        self.btn_check.configure(
            bg="#f44336",
            fg="white",
            activebackground="#d32f2f"
        )

    def check_data(self):
        """此方法用来查询是否有违规或具有安全，隐患的文本"""
        if self.text_area.get("1.0", tk.END).strip():
            # 实例化查询对象
            messagebox.showwarning("查询程序", "确认是否查询")
            time.sleep(1)
            checker = ContentSafetyChecker()
            result = checker.insert_text(self.text_area.get("1.0", tk.END).strip())
            messagebox.showinfo("查询结果", result)
        else:
            messagebox.showwarning("提示消息", "请先查询当日的公众号文章")

    def execute_query(self):
        """执行查询操作"""
        self.query = self.query_entry.get().strip()
        spyder_pro = Spyder(self.query)  # 接入爬虫的接口
        self.data_list = spyder_pro.run()  # 返回爬虫数据
        if not self.query:
            messagebox.showwarning("输入提示", "请输入查询内容")
            return

        # 示例处理逻辑：显示查询内容
        self.text_area.insert(tk.END, f"执行查询{self.query}的公众号数据\n")
        for index, data in enumerate(self.data_list):
            self.text_area.insert(tk.END, "{}  ".format(index))
            for data_detail in data:
                self.text_area.insert(tk.END, "  {}".format(data_detail))
            self.text_area.insert(tk.END, "\n")
        self.query_entry.delete(0, tk.END)

    def clear_content(self):
        """清空文本区域"""
        self.text_area.delete(1.0, tk.END)


if __name__ == "__main__":
    app = TextQueryApp()
    app.mainloop()
