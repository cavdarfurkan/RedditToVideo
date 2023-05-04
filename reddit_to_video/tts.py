'''
This is where text is converted to speech then saved.
'''

import os
import site
from pathlib import Path

from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

import soundfile

PATH_TO_ASSETS: Path = Path('./temp_assets')

SITE_LOCATION = site.getsitepackages()[0]
TTS_PATH = SITE_LOCATION+"/TTS/.models.json"

model_manager = ModelManager(TTS_PATH)
model_path, config_path, model_item = model_manager.download_model(
    "tts_models/en/ljspeech/glow-tts")
# model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")
voc_path, voc_config_path, _ = model_manager.download_model(
    model_item["default_vocoder"])

synthesizer = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path
)


def save_audio(text: str, subdir: str, file_name: str) -> None:
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

    try:
        path.mkdir(parents=True)
    except FileExistsError:
        print("File Exists Error")

    outputs = synthesizer.tts(text)
    synthesizer.save_wav(outputs, f'{path}/{file_name}.wav')


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
