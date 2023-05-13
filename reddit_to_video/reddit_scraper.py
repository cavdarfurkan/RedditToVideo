'''Take subreddits'''


from typing import List
from itertools import combinations
import asyncio

import praw
from praw.models import MoreComments

import tts

from models.submission_model import SubmissionModel

reddit = praw.Reddit(site_name="VideoMakerBot")

MAX_VIDEO_DURATION: float = 60
PAUSE_DURATION: float = 0.5


def take_submissions(subreddit: str, t_filter="day", ratio=0.85, score=3000, min_num_comments=10) -> List[SubmissionModel]:
    '''
    Get the top submissions of the day.

    `subreddit`: Name of the subreddit.
    `t_filter`: Filter submissions by time.
    `ratio`: Up vote ratio of submission.
    `score`: Up votes minus down votes.
    `min_num_comments`: Minimum number of comments that must exists in the submission

    ```python
    take_submission("askreddit")
    take_submission("askreddit", t_filter="now", ratio=0.90, score=5000, min_num_comments=5)
    take_submission("askreddit", t_filter="day", ratio=0.85, score=0, min_num_comments=10)
    ```

    To disable the `score` and `ratio` filters, simply set their values to 0.
    '''

    submission_models_list: List[SubmissionModel] = []

    for submission in reddit.subreddit(subreddit).top(time_filter=t_filter):
        if submission.is_robot_indexable is False:
            continue
        if submission.over_18:
            continue
        if submission.num_comments < min_num_comments:
            continue

        if (submission.upvote_ratio >= ratio and submission.score >= score):
            print(f'submission_id: {submission.id}')
            video_length: float = MAX_VIDEO_DURATION
            asyncio.run(tts.save_audio(
                submission.title, submission.id, 'title'))
            video_length -= (tts.audio_length(submission.id,
                             'title') + PAUSE_DURATION)
            comments = __take_comments(submission.id, video_length)
            if comments:
                submission_models_list.append(
                    SubmissionModel(submission.id, comments))

    return submission_models_list


def __take_comments(submission_id: str, video_length: float, sort_filter: str = "top") -> List[str]:
    '''
    Get the top 10 comments from the selected submission.

    `submission_id`: Unique ID representation of submission
    `video_length`: Sets maximum video duration for comment selection based on tts durations.
    `sort_filter`: Filter type for sorting comments of submission

    ```python
    take_comments("111aaa", 60)
    take_comments("111aaa", 55, sort_filter="best")
    ```
    '''

    submission = reddit.submission(submission_id)
    submission.comment_sort = sort_filter
    all_comments_list = submission.comments.list()
    comments_list: List[tuple] = []
    for comment in all_comments_list:
        if isinstance(comment, MoreComments):
            continue
        if comment.author is None:
            # Comment is removed
            continue
        if comment.author.is_mod:
            # Comment submitted by moderator. Including AutoModerator
            continue
        file_name = f'{submission_id}_{comment.id}'

        is_saved: bool = asyncio.run(tts.save_audio(
            comment.body, submission_id, file_name))
        if is_saved:
            duration: float = tts.audio_length(submission_id, file_name)
            comments_list.append(
                (comment.body, file_name, duration, comment.id))
            if len(comments_list) >= 10:
                break

    # Selecting the most optimal comments considering the video duration
    max_sum: float = 0
    max_tuple: tuple = tuple()

    for i in range(3, 8):
        for combination in combinations(comments_list, i):

            length_combination = [comment[2] for comment in combination]
            current_sum: float = sum(length_combination)

            if current_sum > video_length:
                continue
            if (current_sum <= video_length - (i*PAUSE_DURATION)) and (current_sum > max_sum):
                max_sum = current_sum
                max_tuple = combination

    # If max_tuple is empty, retry with combination of 2
    if not max_tuple:
        for combination in combinations(comments_list, 2):

            length_combination = [comment[2] for comment in combination]
            current_sum: float = sum(length_combination)

            if current_sum > video_length:
                continue
            if (current_sum <= video_length - (2*PAUSE_DURATION)) and (current_sum > max_sum):
                max_sum = current_sum
                max_tuple = combination

    selected_items = list((comment_id[3] for comment_id in max_tuple))

    # Delete unselected audios by file_name
    for item in comments_list:
        is_selected = False
        for selected_item in max_tuple:
            if item[1] == selected_item[1]:
                is_selected = True
                break
        if not is_selected:
            tts.delete_audio(submission_id, item[1])

    return selected_items
