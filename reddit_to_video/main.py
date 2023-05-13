'''Main Script'''

import shutil
import os
import json

from reddit_scraper import take_submissions
from image_scraper import take_screenshot
from video_generator import generate_video

TEMP_ASSETS_PATH = './temp_assets'
OUTPUTS_PATH = './outputs'
DATA_PATH = './data/{file}.json'

delete_temp_assets = True
delete_outputs = False

# Create necessary directories
if not os.path.exists(OUTPUTS_PATH):
    print(f'Make dir {OUTPUTS_PATH}')
    os.makedirs(OUTPUTS_PATH)

with open(DATA_PATH.format(file='subreddits'), encoding='utf-8') as f:
    datas = json.load(f)
    for item in datas:

        print(f'Taking submissions: {item["name"]}')

        submissions = take_submissions(subreddit=item['name'], t_filter=item['time_filter'],
                                       ratio=item['ratio'], score=item['score'], min_num_comments=item['min_comments'])

        for sub in submissions:
            take_screenshot(sub)

        for sub in submissions:
            generate_video(sub)


if delete_temp_assets:
    print(f'Deleting {TEMP_ASSETS_PATH}')
    shutil.rmtree(TEMP_ASSETS_PATH)

if delete_outputs:
    print(f'Deleting {OUTPUTS_PATH}')
    shutil.rmtree(OUTPUTS_PATH)
