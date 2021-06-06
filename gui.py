import json
import os
import shutil
import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
import main
import logging


class Application(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.master = root
        self.pack()
        self.source = tk.StringVar(value="E:/音声分类")
        self.alpha = tk.StringVar(value="E:/音声abc")
        self.num = tk.StringVar(value="E:/音声123")
        self.kana = tk.StringVar(value="E:/音声假名")
        self.kanji = tk.StringVar(value="E:/音声汉字")
        self.unknown = tk.StringVar(value="E:/音声其它")
        self.file_name_group = {}
        self.int_wind()

    def scan(self):
        self.file_name_group = main.scan_files(self.source.get())
        showinfo(title='扫描完成', message=self.pretty(self.file_name_group))

    def pretty(self, d):
        return json.dumps(d, indent=4, ensure_ascii=False)

    def cut_move(self):
        logging.info("开始文件传输")
        for key in self.file_name_group:
            logging.info("--开始移动类别：" + key)
            for file_list in self.file_name_group[key]:
                file_name = file_list[0]
                group_name = file_list[1]
                if key == 'alpha':
                    target_base_path = self.alpha.get()
                elif key == 'num':
                    target_base_path = self.num.get()
                elif key == 'kana':
                    target_base_path = self.kana.get()
                elif key == 'kanji':
                    target_base_path = self.kanji.get()
                elif key == 'unknown':
                    target_base_path = self.unknown.get()
                target_path = target_base_path + "/" + group_name
                if not os.path.isdir(target_path):
                    os.mkdir(target_path)
                logging.info("----开始移动" + file_name)
                try:
                    if not os.path.exists(target_path + "/" + file_name):
                        # os.makedirs(target_path + "/" + file_name)
                        shutil.move(self.source.get() + "/" + file_name, target_path + "/" + file_name)
                        logging.info("----移动完毕")
                    else:
                        logging.info("文件已存在，取消传输")
                except BaseException as e:
                    logging.info(e)
                    logging.info("文件传输异常")
        showinfo(title='移动完毕', message="移动完毕")

    def int_wind(self):
        frame1 = Frame(self, width=50)
        Label(frame1, text='源').grid(row=0, column=0)
        Entry(frame1, textvariable=self.source).grid(row=0, column=1)

        frame2 = Frame(self)
        Label(frame2, text='英文').grid(row=1, column=0)
        Entry(frame2, textvariable=self.alpha).grid(row=1, column=1)

        frame3 = Frame(self)
        Label(frame3, text='数字').grid(row=2, column=0)
        Entry(frame3, textvariable=self.num).grid(row=2, column=1)

        frame4 = Frame(self)
        Label(frame4, text='假名').grid(row=3, column=0)
        Entry(frame4, textvariable=self.kana).grid(row=3, column=1)

        frame5 = Frame(self)
        Label(frame5, text='汉字').grid(row=4, column=0)
        Entry(frame5, textvariable=self.kanji).grid(row=4, column=1)

        frame6 = Frame(self)
        Label(frame6, text='未知').grid(row=5, column=0)
        Entry(frame6, textvariable=self.unknown).grid(row=5, column=1)

        # 间距
        frame1.grid(pady=20)
        frame2.grid(pady=20)
        frame3.grid(pady=20)
        frame4.grid(pady=20)
        frame5.grid(pady=20)
        frame6.grid(pady=20)

        Button(self, text='扫描文档', width=10, command=self.scan).grid()
        Button(self, text='移动文件', width=10, command=self.cut_move).grid()


if __name__ == '__main__':
    logging.basicConfig(filename='./log.log', level=logging.INFO)
    root = tk.Tk()
    root.geometry("720x480")
    application = Application(root)
    root.mainloop()
