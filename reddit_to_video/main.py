'''Main Script'''

import shutil
import os

from reddit_scraper import take_submissions
from image_scraper import take_screenshot
from video_generator import generate_video

TEMP_ASSETS_PATH = './temp_assets'
OUTPUTS_PATH = './outputs'

delete_temp_assets = True
delete_outputs = False

# Create necessary directories
if not os.path.exists(OUTPUTS_PATH):
    print(f'Make dir {OUTPUTS_PATH}')
    os.makedirs(OUTPUTS_PATH)


submissions = take_submissions("askreddit", ratio=0, score=200)

for sub in submissions:
    take_screenshot(sub)

for sub in submissions:
    generate_video(sub)


if delete_temp_assets:
    shutil.rmtree(TEMP_ASSETS_PATH)

if delete_outputs:
    shutil.rmtree(OUTPUTS_PATH)
