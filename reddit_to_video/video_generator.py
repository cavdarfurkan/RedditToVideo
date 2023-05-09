'''
Video generator script out of SubmissionModel
'''

import os
from random import choice

from moviepy.editor import ImageClip, VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips

from PIL import Image
import numpy as np

from models.submission_model import SubmissionModel


BACKGROUND_VIDEOS_DIR: str = './background_videos'

PATH_TO_ASSETS: str = './temp_assets'
TEMPL_IMG = PATH_TO_ASSETS + "/{sub_id}/{com_id}.png"
TEMPL_AUDIO = PATH_TO_ASSETS + "/{sub_id}/{sub_id}_{com_id}.wav"

OUTPUT_DIR: str = './outputs'


def generate_video(model: SubmissionModel):
    '''
    Generate final video out of submission.

    @param model: Submission model to generate video.
    @type model: SubmissionModel
    '''
    background_video = __random_background_video()

    clips = []

    # First generate title clip
    title_img_dir = TEMPL_IMG.format(
        sub_id=model.submission_id, com_id='title')
    title_audio_dir = PATH_TO_ASSETS + f"/{model.submission_id}/title.wav"

    title_audio = AudioFileClip(title_audio_dir)
    title_image = __make_resized_image(
        title_img_dir, background_video, h_padding=100).set_duration(title_audio.duration)
    title_image_with_audio = title_image.set_audio(title_audio)
    clips.append(title_image_with_audio)

    # Generate comment clips
    for comment_id in model.comments:
        img_dir = TEMPL_IMG.format(
            sub_id=model.submission_id, com_id=comment_id)
        audio_dir = TEMPL_AUDIO.format(
            sub_id=model.submission_id, com_id=comment_id)

        title_audio = AudioFileClip(audio_dir)
        title_image = __make_resized_image(
            img_dir, background_video, h_padding=100).set_duration(title_audio.duration)
        title_image_with_audio = title_image.set_audio(title_audio)
        clips.append(title_image_with_audio)

    concatenated_clips = concatenate_videoclips(
        clips=clips, method="compose", bg_color=None)
    final_clip = CompositeVideoClip(
        [background_video, concatenated_clips.set_position(("center", "center"))], use_bgclip=True, size=background_video.size)

    final_clip.write_videofile(OUTPUT_DIR + (f'/{model.submission_id}.mp4'))


def __random_background_video() -> VideoFileClip:
    '''
    Selects a random background video from the background_videos directory 
    and returns it as VideoFileClip
    '''

    background_videos = [s for s in os.listdir(
        BACKGROUND_VIDEOS_DIR) if s.endswith('.mp4')]
    selected_background_video = choice(background_videos)
    return VideoFileClip(f'{BACKGROUND_VIDEOS_DIR}/{selected_background_video}')
    # return VideoFileClip(BACKGROUND_VIDEOS_DIR.joinpath(selected_background_video))


def __make_resized_image(image_dir: str, background_video: VideoFileClip, h_padding: int = 0) -> ImageClip:
    '''
    Resize the image to fit the background video while keeping the ratio same.

    @param image: Path of the image to resize.
    @type image: str

    @param background_video: Background video.
    @type background_video: VideoFileClip

    @param h_padding: Horizontal padding. Image is centered.
    @type h_padding: int
    '''

    img = Image.open(image_dir)

    width, height = img.size
    target_width = background_video.w - h_padding
    target_height = int(height * target_width / width)

    img = img.resize((target_width, target_height))

    arr = np.array(img)
    return ImageClip(arr)


__random_background_video()
