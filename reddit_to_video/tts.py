'''
This is where text is converted to speech then saved.
'''

import os
from pathlib import Path
from random import choice

import edge_tts
import soundfile


PATH_TO_ASSETS: Path = Path('./temp_assets')


VOICES = ['en-US-AriaNeural', 'en-US-ChristopherNeural', 'en-US-EricNeural', 'en-US-GuyNeural',
          'en-US-JennyNeural', 'en-US-MichelleNeural', 'en-US-RogerNeural', 'en-US-SteffanNeural']


async def save_audio(text: str, subdir: str, file_name: str) -> bool:
    '''
    Save the text as .wav audio.

    @param text: Text to save as audio
    @type text: str

    @param subdir: Subdir name. Usually it's same as submission id. /temp_assets/{subdir}
    @type subdir: str

    @param file_name: File name.wav
    @type file_name: str
    '''

    path: Path = PATH_TO_ASSETS.joinpath(subdir)
    is_saved: bool = False

    try:
        path.mkdir(parents=True)
    except FileExistsError:
        print("File Exists Error")

    try:
        # asyncio.run(tts_to_speech(text, str(path), file_name))
        output = edge_tts.Communicate(text, choice(VOICES))
        await output.save(f'{path}/{file_name}.wav')
        is_saved = True
    except Exception:
        is_saved = False
        print('Synthesizer failed.')

    return is_saved


def delete_audio(subdir: str, audio_file: str) -> None:
    '''
    Delete audio /temp_assets/{subdir}/{file_name}.wav

    @param subdir: Path of subdir. Usually it's same as submisison id.
    @type subdir: str

    @param audio_file: Path of the audio file.
    @type audio_file: str
    '''

    try:
        path: Path = PATH_TO_ASSETS.joinpath(
            subdir).joinpath(f'{audio_file}.wav')
        os.remove(path)
    except FileNotFoundError:
        print("File Not Found Error")


def audio_length(subdir: str, audio_file: str) -> float:
    '''
    Audio length of the saved audio asset.

    @param subdir: Path of subdir. Usually it's same as submisison id.
    @type subdir: str

    @param audio_file: Path of the audio file.
    @type audio_file: str
    '''

    path: Path = PATH_TO_ASSETS.joinpath(subdir).joinpath(f'{audio_file}.wav')
    return soundfile.info(path).duration
