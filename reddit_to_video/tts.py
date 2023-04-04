'''
This is where text is converted to speech than saved.
'''

import os
import random

from pathlib import Path
import pyttsx3 as tts


PATH_TO_AUDIO: Path = Path('./tts_audio')


engine = tts.init()
engine.setProperty('rate', 150)
vs = engine.getProperty('voices')


def save_audio(text: str, file_name: str) -> None:
    '''
    Save the text as audio to the ./tts_audio directory.

    @param text: Text to save as audio
    @type text: str

    @param file_name: File name after the temp_ prefix and before the .mp3 suffix
    @type file_name: str
    '''

    if not PATH_TO_AUDIO.exists():
        try:
            PATH_TO_AUDIO.mkdir()
        except FileExistsError:
            print("File Exists Error")

    _set_random_voice()
    engine.save_to_file(text, f"{PATH_TO_AUDIO}/temp_{file_name}.mp3")
    engine.runAndWait()


def delete_all_audios() -> None:
    '''
    Delete temp audio files in ./tts_audio directory.
    '''
    try:
        for file in PATH_TO_AUDIO.glob("temp_*.mp3"):
            os.remove(file)
    except FileNotFoundError:
        print("File Not Found Error")


def _set_random_voice() -> None:
    '''
    Sets a random voice from voices list.
    '''
    engine.setProperty('voice', random.choice(vs).id)
