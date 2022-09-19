from pygame import mixer

melody = "path here" # !!! WONT WORK WITHOUT PATH TO MUSIC FILE HERE
melody1 = "path here" # !!! WONT WORK WITHOUT PATH TO MUSIC FILE HERE

def pause():
    mixer.music.pause()

def unpause():
    mixer.music.unpause()

def stop():
    mixer.music.stop()

def skip_to(to) -> int:
    mixer.music.pause()
    prev_pos = mixer.music.get_pos()
    mixer.music.stop()
    mixer.music.load(to)
    mixer.music.play()
    return prev_pos

def go_back(to):
    mixer.music.pause()
    prev_pos = mixer.music.get_pos()
    mixer.music.stop()
    mixer.music.load(to)
    mixer.music.play()
    return prev_pos

mixer.pre_init(44100, -16, 1, 512)
mixer.init()

mixer.music.load(melody)
mixer.music.set_volume(0.01)
mixer.music.play()
while mixer.music.get_busy():  # wait for music to finish playing
    inp = input()

    if inp == "next":
        skip_to(melody1)
    elif inp == "back":
        go_back(melody)