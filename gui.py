import tkinter as tk
import subprocess

# 解析网址
def parse_url(url):
    x, y, z = url.split("@")[1].split(",")
    x = int(x)
    y = int(y)
    z = float(z[:-1])
    return x, y, z

# 运行测试脚本
def run_test():
    url = url_entry.get()
    params = parse_url(url)
    result = subprocess.run(["python", "test.py", params], capture_output=True, text=True)
    info_text.config(state=tk.NORMAL)
    info_text.delete("1.0", tk.END)
    info_text.insert(tk.END, result.stdout)
    info_text.config(state=tk.DISABLED)

# 运行下载脚本
def download_file():
    result = subprocess.run(["python", "download.py"], capture_output=True, text=True)
    info_text.config(state=tk.NORMAL)
    info_text.delete("1.0", tk.END)
    info_text.insert(tk.END, result.stdout)
    info_text.config(state=tk.DISABLED)

# 创建主窗口
root = tk.Tk()
root.title("地图下载器")

# 添加标签和文本框
url_label = tk.Label(root, text="请输入待解析网址:")
url_label.pack()

url_entry = tk.Entry(root)
url_entry.pack()

# 添加信息展示区
info_text = tk.Text(root, height=10, width=50)
info_text.pack()
info_text.config(state=tk.DISABLED)  # 设置为只读

# 添加按钮
test_button = tk.Button(root, text="测试", command=run_test)
test_button.pack()

download_button = tk.Button(root, text="下载", command=download_file)
download_button.pack()

quit_button = tk.Button(root, text="退出", command=root.quit)
quit_button.pack()

# 启动主循环
root.mainloop()
