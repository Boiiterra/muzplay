from tkinter import filedialog, Tk, Button
from tkinter.messagebox import showinfo
from os import listdir, path as o_path
from fleep import get as f_get

FILE_TYPES = [("Music files", "*.mp3")]


class MusicPlayer(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Title")
        # self.iconbitmap("path to icon") # Need to draw icon
        self.minsize(300, 200)

        files = []

        add_file = Button(self, text="Add file", command=lambda: add())
        add_file.pack()
        add_dir = Button(self, text="Add dir", command=lambda: add(True))
        add_dir.pack()
        add_files = Button(self, text="Add files", command=lambda: add(False))
        add_files.pack()

        def add(folder:bool=None):
            """folder == None then add one file\n
            folder == False -> multiple files\n
            folder == True -> folder"""

            if folder is None:
                get_prompt = filedialog.askopenfile(initialdir="~", title="Selecting file", filetypes=FILE_TYPES)
                if get_prompt is None:
                    showinfo("Nothing selected", "No file is selected.\nPlease select something next time.")
                    return

                with open(get_prompt.name, "rb") as _file:
                    info = f_get(_file.read(128))

                if info.extension[0] == "mp3" and info.type[0] == "audio":
                    files.append(get_prompt.name)

            elif folder:
                get_prompt = filedialog.askdirectory(initialdir="~", title="Selecting directory")

                if get_prompt:
                    fid = list(filter(lambda a: ".mp3" in a, listdir(get_prompt)))
                    if fid:
                        for file in fid:
                            file_path = o_path.join(get_prompt,file)

                            with open(file_path, "rb") as _file:
                                info = f_get(_file.read(128))

                            if info.extension[0] == "mp3" and info.type[0] == "audio":
                                files.append(file_path)
                    else:
                        showinfo("Nothing found", f'There are no ".mp3" files found in "{get_prompt}"')
                else:
                    showinfo("Nothing selected", "No folder is selected.\nPlease select something next time.")

            else:
                get_prompt = filedialog.askopenfiles(initialdir="~", title="Selecting file", filetypes=FILE_TYPES)

                if get_prompt:
                    for file in get_prompt:
                        with open(file.name, "rb") as _file:
                            info = f_get(_file.read(128))

                        if info.extension[0] == "mp3" and info.type[0] == "audio":
                            files.append(file.name)
                else:
                    showinfo("Nothing selected", "No files are selected.\nPlease select something next time.")
