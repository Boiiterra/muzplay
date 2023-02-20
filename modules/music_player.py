from tkinter import filedialog, Tk, Button, Label, Frame, Scale, IntVar
from tkinter.messagebox import showinfo
from os import listdir, path as o_path
from fleep import get as f_get
from mutagen.mp3 import MP3

# Custom imports
from .music import (
    initialize,
    start,
    pause,
    unpause,
    stop,
    skip_to,
    go_back,
    set_volume,
    gpos,
    continue_,
)
from .tooltip import create_tool_tip

FILE_TYPES = [("Music files", "*.mp3"), ("Other", "*")]
FONT = ("Arial", 25)
INIT_DIR = "~/Music"

initialize()


class MusicPlayer(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Music Player")
        # self.iconbitmap("path to icon") # Need to draw icon
        self.minsize(300, 200)

        files = []
        self.current = ""
        vol = IntVar()
        vol.set(40)
        playing = 0

        def start_playing():
            if files:
                start(files[playing])
            else:
                print("No files were chosen to play!")

        set_volume(0.4)

        add_c = Frame(self)
        add_c.pack()

        add_i = Label(add_c, text="Add:", font=FONT)
        add_i.grid(row=0, column=0, padx=(0, 5), sticky="snew")
        add_file = Button(add_c, font=FONT, text="file", command=lambda: add())
        add_file.grid(row=0, column=1, sticky="snew")
        add_dir = Button(add_c, font=FONT, text="dir", command=lambda: add(True))
        add_dir.grid(row=0, column=2, sticky="snew", padx=1)
        add_files = Button(add_c, font=FONT, text="files", command=lambda: add(False))
        add_files.grid(row=0, column=3, sticky="snew")
        play = Button(self, text="Play", font=FONT, command=start_playing)
        play.pack()
        song_info = Label(self, font=FONT)
        song_info.pack()
        volume = Scale(
            self,
            label="Volume:",
            font=FONT,
            from_=0,
            to=100,
            variable=vol,
            orient="horizontal",
            command=lambda _volume: set_volume(int(_volume) / 100),
        )
        volume.pack(fill="x", padx=25, pady=(0, 10))

        create_tool_tip(song_info, "Current song")

        def current_song(new: str):
            song_info.config(text=new)

        current_song("None song is present. 0:0")

        def add(folder: bool = None):
            """folder == None then add one file\n
            folder == False -> multiple files\n
            folder == True -> folder"""

            if folder is None:
                get_prompt = filedialog.askopenfile(
                    initialdir=INIT_DIR, title="Selecting file", filetypes=FILE_TYPES
                )
                if get_prompt is None:
                    showinfo(
                        "Nothing selected",
                        "No file is selected.\nPlease select something next time.",
                    )
                    return

                with open(get_prompt.name, "rb") as _file:
                    info = f_get(_file.read(128))

                if (
                    info.extension[0] == "mp3"
                    and info.type[0] == "audio"
                    and get_prompt.name not in files
                ):
                    files.append(get_prompt.name)

            elif folder:
                get_prompt = filedialog.askdirectory(
                    initialdir=INIT_DIR, title="Selecting directory"
                )

                if get_prompt:
                    fid = list(filter(lambda a: ".mp3" in a, listdir(get_prompt)))
                    if fid:
                        for file in fid:
                            file_path = o_path.join(get_prompt, file)

                            with open(file_path, "rb") as _file:
                                info = f_get(_file.read(128))

                            if (
                                info.extension[0] == "mp3"
                                and info.type[0] == "audio"
                                and file_path not in files
                            ):
                                files.append(file_path)
                    else:
                        showinfo(
                            "Nothing found",
                            f'There are no ".mp3" files found in "{get_prompt}"',
                        )
                else:
                    showinfo(
                        "Nothing selected",
                        "No folder is selected.\nPlease select something next time.",
                    )

            else:
                get_prompt = filedialog.askopenfiles(
                    initialdir=INIT_DIR, title="Selecting file", filetypes=FILE_TYPES
                )

                if get_prompt:
                    for file in get_prompt:
                        with open(file.name, "rb") as _file:
                            info = f_get(_file.read(128))

                        if (
                            info.extension[0] == "mp3"
                            and info.type[0] == "audio"
                            and file.name not in files
                        ):
                            files.append(file.name)
                else:
                    showinfo(
                        "Nothing selected",
                        "No files are selected.\nPlease select something next time.",
                    )

            files.sort()
            if not self.current and files:
                self.current = files[0].split("/")[-1]
                duration = MP3(files[0]).info.length  # seconds
                minutes = int(duration // 60)
                seconds = round(duration - minutes * 60)
                current_song(f"{self.current} {minutes}:{seconds}")
            print(files)
