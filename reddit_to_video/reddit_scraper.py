'''Take subreddits'''

import itertools

import praw
from praw.models import MoreComments

from tts import est_audio_length

from models.submission_model import SubmissionModel

reddit = praw.Reddit(site_name="bot1")

MAX_VIDEO_DURATION: float = 60
PAUSE_DURATION: float = 0.5


def take_submissions(subreddit: str, t_filter="day", ratio=0.85, score=3000, min_num_comments=10) -> list[SubmissionModel]:
    '''
    Get the top submissions of the day.

    `subreddit`: Name of the subreddit.
    `t_filter`: Filter submissions by time.
    `ratio`: Up vote ratio of submission.
    `score`: Up votes minus down votes.
    `min_num_comments`: Minimum number of comments must exists in the submission

    ```python
    take_submission("askreddit")
    take_submission("askreddit", t_filter="now", ratio=0.90, score=5000, min_num_comments=5)
    take_submission("askreddit", t_filter="day", ratio=0.85, score=0, min_num_comments=10)
    ```

    To disable the `score` and `ratio` filters, simply set their values to 0.
    '''

    submission_models_list: list[SubmissionModel] = []

    for submission in reddit.subreddit(subreddit).top(time_filter=t_filter):
        if submission.is_robot_indexable is False:
            continue
        if submission.num_comments < min_num_comments:
            continue

        if (submission.upvote_ratio >= ratio and submission.score >= score):
            video_length: float = MAX_VIDEO_DURATION
            video_length -= (est_audio_length(submission.title) +
                             PAUSE_DURATION)
            comments = __take_comments(submission.id, video_length)
            if comments:
                submission_models_list.append(SubmissionModel(
                    submission.id, (submission.author, submission.title), comments))

    return submission_models_list


def __take_comments(submission_id: str, video_length: float, sort_filter: str = "top") -> list[tuple]:
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
    comments_list = []
    for comment in all_comments_list:
        if isinstance(comment, MoreComments):
            continue
        if comment.author is None:
            # Comment is removed
            continue
        if comment.author.is_mod:
            # Comment submitted by moderator. Including AutoModerator
            continue
        comments_list.append(comment)
        if len(comments_list) >= 10:
            break

    # Selecting the most optimal comments considering the video duration
    max_sum: float = 0
    max_tuple: tuple = tuple()
    for i in range(3, 8):
        for combination in itertools.combinations(comments_list, i):
            length_combination: tuple[float, ...] = tuple(
                est_audio_length(comment.body) for comment in combination)
            current_sum: float = sum(length_combination)
            if current_sum > video_length:
                continue
            if (current_sum <= video_length - (i*PAUSE_DURATION)) and (current_sum > max_sum):
                max_sum = current_sum
                max_tuple = combination

    if not max_tuple:
        for combination in itertools.combinations(comments_list, 2):
            length_combination: tuple[float, ...] = tuple(
                est_audio_length(comment.body) for comment in combination)
            current_sum: float = sum(length_combination)
            if current_sum > video_length:
                continue
            if (current_sum <= video_length - (2*PAUSE_DURATION)) and (current_sum > max_sum):
                max_sum = current_sum
                max_tuple = combination

    return list((comment.author, comment.body) for comment in max_tuple)
    # comment.id -> unique id for the comment
