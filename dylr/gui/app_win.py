# coding=utf-8
"""
:author: Lyzen
:date: 2023.01.17
:brief: 主窗口
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog, messagebox

from dylr.gui import grip_frame
from dylr.core import version, record_manager, app


class ApplicationWin(ttk.Frame):
    def __init__(self):
        app.win = self
        ttk.Frame.__init__(self, None, border=2)
        self.pack(fill=tk.BOTH, expand=True)
        self.init_win()
        self.reload_all()
        self.mainloop()

    def init_win(self):
        """ 初始化窗口 """
        self.topwin = self.winfo_toplevel()
        self.topwin.title(f'[吾爱破解论坛]抖音直播自动录制工具 v{version} by Lyzen')
        self.topwin.protocol('WM_DELETE_WINDOW', self.on_close)
        self.rootpane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.rootpane.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # 底部按钮
        footer_frame = tk.Frame(self)
        # add_room_btn = tk.Button(footer_frame, text='添加主播', font=('微软雅黑', 14), command=self._request_add_room)
        # add_room_btn.grid(row=0, column=0, padx=25, pady=5)
        info_label = tk.Label(footer_frame, text='修改监测直播、录制弹幕、重要主播，直接双击[是]或[否]即可')
        info_label.grid(row=0, column=1, padx=10, pady=5)
        self.rootpane.add(footer_frame)

        # 可滚动布局容器
        canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        room_list_frame = tk.Frame(canvas, background="#ffffff")
        vsb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4, 4), window=room_list_frame, anchor="nw")
        canvas.config(height=480)
        room_list_frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        self.grip_frame = grip_frame.GripFrame(room_list_frame)
        self.grip_frame.pack()
        self.grip_frame.bind('<Configure>', self._on_canvas_adjust)

    def reload_all(self):
        self.grip_frame.remove_all()
        for room in record_manager.get_rooms():
            self.grip_frame.append(room.room_id, room.room_name, '未直播' if room.auto_record else '未监测',
                                   room.auto_record, room.record_danmu, room.important)

    def set_state(self, room, text, color='#000000'):
        self.grip_frame.set(room.room_id, text, color)

    def add_room(self, room):
        self.grip_frame.append(room.room_id, room.room_name, '未直播' if room.auto_record else '未监测',
                               room.auto_record, room.record_danmu, room.important)

    def remove_room(self, web_rid):
        self.grip_frame.remove(web_rid)

    def _request_add_room(self):
        res = simpledialog.askstring(title='添加主播', prompt='请输入房间地址，支持Web_Sid、直播间地址、短链、(正在直播的)主播主页，如\n'
                                                          '123456\n'
                                                          'https://live.douyin.com/123456?xxx=\n'
                                                          'https://v.douyin.com/AbCDef\n'
                                                          'https://www.douyin.com/user/MS4wLjABAAAA2G3...')
        # add_room_manager.try_add_room(res)


    def _on_canvas_adjust(self, event):
        self.topwin.minsize(event.width + 20, 480)

    def on_close(self):
        if messagebox.askokcancel("关闭", "是否关闭软件？"):
            self.quit()
