# -*- coding: utf-8 -*-
import io
import re
import json
from urllib.request import urlopen
from tkinter import (
    Label,
    Button,
    Tk,
    NW,
    LEFT,
    IntVar,
    Radiobutton,
)
from tkinter.font import Font
from tkinter.messagebox import showwarning
from PIL import (
    Image,
    ImageTk,
)

tk_image = None
emoji_pattern = re.compile('['
        '\U0001F300-\U0001F64F'
        '\U0001F680-\U0001F6FF'
        '\u2600-\u2B55]+',
        re.UNICODE)


class FireEye(object):
    def __init__(self, master):
        self.master = master
        self.offset = 0
        with open('videos1.txt', 'r') as v_file:
            self.videos = json.load(v_file)

        with open('result.txt', 'r') as r_file:
            self.result = json.load(r_file)

        self.current = self.videos[0]
        self.title_label = Label(
            self.master, text=emoji_pattern.sub("", self.current['title']), font=Font(size=15, weight='bold'),
            wraplength=580, justify=LEFT)
        self.title_label.place(anchor=NW, x=10, y=10)

        self._get_poster()
        self.poster_label = Label(self.master, image=tk_image)
        self.poster_label.place(anchor=NW, x=10, y=100)

        tags = ', '.join(self.current['tag'])
        self.tag_label = Label(self.master, text=emoji_pattern.sub("", tags), wraplength=580, justify=LEFT)
        self.tag_label.place(anchor=NW, x=10, y=350)

        self.sexy_value = IntVar()
        self.sexy_value.set(self.result.get(self.current['id'], -1))
        sexy_radio = Radiobutton(
            master, text="sexy", variable=self.sexy_value, value=1, command=self.set_sexy)
        not_sexy_radio = Radiobutton(
            master, text="not sexy", variable=self.sexy_value, value=0, command=self.set_not_sexy)
        sexy_radio.place(anchor=NW, x=200, y=600)
        not_sexy_radio.place(anchor=NW, x=300, y=600)

        self.save_button = Button(self.master, text="save", command=self.handle_save)
        self.save_button.place(anchor=NW, x=400, y=600)

        self.previous_button = Button(self.master, text="previous", command=self.handle_previous)
        self.previous_button.place(anchor=NW, x=10, y=650)
        self.page_label = Label(self.master, text=str(self.offset))
        self.page_label.place(anchor=NW, x=290, y=650)
        self.next_button = Button(self.master, text="next", command=self.handle_next)
        self.next_button.place(anchor=NW, x=550, y=650)

    def _get_poster(self):
        global tk_image
        poster = self.current['poster']
        poster = poster.replace('maxresdefault', 'mqdefault')
        poster = poster.replace('hqdefault', 'mqdefault')
        image_bytes = urlopen(poster).read()
        data_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        tk_image = ImageTk.PhotoImage(pil_image)

    def render_video(self):
        """render single video"""
        if self.offset < 0:
            showwarning("error", "already the first video")
            return

        if self.offset >= len(self.videos):
            showwarning("error", "already the last video")
            return

        self.current = self.videos[self.offset]
        self.title_label['text'] = emoji_pattern.sub("", self.current['title'])
        self.page_label['text'] = str(self.offset)

        self._get_poster()
        self.poster_label['image'] = tk_image

        tags = ', '.join(self.current['tag'])
        self.tag_label['text'] = emoji_pattern.sub("", tags)

        self.sexy_value.set(self.result.get(self.current['id'], -1))

    def handle_previous(self):
        """goto previous video"""
        self.offset -= 1
        self.render_video()

    def handle_next(self):
        """goto next video"""
        self.offset += 1
        self.render_video()

    def set_sexy(self):
        """set video sexy"""
        self.result[self.current['id']] = 1

    def set_not_sexy(self):
        """set video not sexy"""
        self.result[self.current['id']] = 0

    def handle_save(self):
        with open('result.txt', 'w') as w_file:
            json.dump(self.result, w_file, indent=4)


if __name__ == '__main__':
    root = Tk()
    root.title("FireEye")
    root.wm_geometry("600x700")
    root.wm_resizable(width=False, height=False)
    display = FireEye(root)
    root.mainloop()
