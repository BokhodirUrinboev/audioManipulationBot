import matplotlib.pyplot as plt
import datetime
from random import randint
from pydub import AudioSegment


PATH_PICTURES = "C:\\Users\\Bokhodir\\PycharmProjects\\audio_manipulation\\data\\pictures\\"

PATH_RESULT = "C:\\Users\\Bokhodir\\PycharmProjects\\audio_manipulation\data\\result\\"


def reverse_sound(song, lebel_name = "sound"):
    rev = song.reverse()
    sound_plot = song.get_array_of_samples()

    basename_p = PATH_PICTURES + "plot_sound"
    suffix_p = datetime.datetime.now().strftime("%y%m%d_%H%M%S" + ".png")
    img_path = "_".join([basename_p, suffix_p])

    plt.figure(randint(1, 999))
    plt.title(lebel_name)
    plt.plot(sound_plot)
    plt.savefig(img_path)

    basename_s = PATH_RESULT + "result_sound"
    suffix_s = datetime.datetime.now().strftime("%y%m%d_%H%M%S" + ".mp3")
    sound_path = "_".join([basename_s, suffix_s])

    rev.export(sound_path, format="mp3")

    return sound_path, img_path

def speed_change(sound, speed=1.0, lebel_name="sound"):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    result_sound = sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)
    sound_plot = sound.get_array_of_samples()

    basename_p = PATH_PICTURES + "plot_sound"
    suffix_p = datetime.datetime.now().strftime("%y%m%d_%H%M%S" + ".png")
    img_path = "_".join([basename_p, suffix_p])

    plt.figure(randint(1, 999))
    plt.title(lebel_name)
    plt.plot(sound_plot)
    plt.savefig(img_path)

    basename_s = PATH_RESULT + "result_sound"
    suffix_s = datetime.datetime.now().strftime("%y%m%d_%H%M%S" + ".mp3")
    sound_path = "_".join([basename_s, suffix_s])

    result_sound.export(sound_path, format="mp3")

    return sound_path, img_path

def background_effect(sound, background, vol_dec= 5, lebel_name="sound"):
    result_sound = sound.overlay(background -vol_dec)
    sound_plot = sound.get_array_of_samples()

    basename_p = PATH_PICTURES + "plot_sound"
    suffix_p = datetime.datetime.now().strftime("%y%m%d_%H%M%S" + ".png")
    img_path = "_".join([basename_p, suffix_p])

    plt.figure(randint(1, 999))
    plt.title(lebel_name)
    plt.plot(sound_plot)
    plt.savefig(img_path)

    basename_s = PATH_RESULT + "result_sound"
    suffix_s = datetime.datetime.now().strftime("%y%m%d_%H%M%S" + ".mp3")
    sound_path = "_".join([basename_s, suffix_s])

    result_sound.export(sound_path, format="mp3")

    return sound_path, img_path


# sound = AudioSegment.from_ogg(PATH_TEMP + "putin.ogg")
# background = AudioSegment.from_mp3(PATH_SOUND_EFFECT + SOUND_EFFECT[2])

#  sound_path, image_path = reverse_sound(sound,"ali xoja ")
# sound_path, image_path = background_effect(sound, background, 7, "user_ali")
# sound_path, image_path = speed_change(sound,0.8, "user ali")


