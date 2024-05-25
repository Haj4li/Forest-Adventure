from pygame import mixer
#Instantiate mixer
mixer.init()


def play_audio(file_path, loop=False,volume=1):
    mixer.music.load(file_path)
    #Set preferred volume
    mixer.music.set_volume(volume)
    mixer.music.play(-1)
