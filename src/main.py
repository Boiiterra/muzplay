from tkinter import filedialog, Tk, Button
from platform import system

base = "~"


class MusicPlayer(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Title")
        # self.iconbitmap("path to icon") # Need to draw icon

        add_file = Button(self, text="Add file")

MusicPlayer().mainloop()
# files = filedialog.askopenfile(initialdir="~", title="Selecting file", filetypes=[("Music files", "*.mp3"), ("Any files", "*.*")])
# print(files.name)
