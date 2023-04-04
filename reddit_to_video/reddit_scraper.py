'''Take subreddtis'''

import praw

reddit = praw.Reddit(site_name="bot1")


def take_submission(subreddit: str, t_filter="day", ratio=0.85, score=3000, min_num_comments=3):
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
    take_submission("askreddit", t_filter="day", ratio=0.85, score=0, min_num_comments=3)
    ```

    To disable the `score` and `ratio` filters, simply set their values to 0.
    '''

    for submission in reddit.subreddit(subreddit).top(time_filter=t_filter):
        if submission.is_robot_indexable is False:
            continue
        if not submission.media == 'Null':
            continue
        if submission.num_comments < min_num_comments:
            continue

        if (submission.upvote_ratio >= ratio and submission.score >= score):
            print("*************************")
            print(f"---{submission.title}---")
            take_comments(submission.id)
            print("*************************")

# print(len(submissionsList))
#     print(submission.author)
#     print(submission.is_robot_indexable)
#     print(submission.ups)
#     print(submission.upvote_ratio)
#     print(submission.score)
#     print(submission.over_18)
#     print(submission.num_comments)
#     print(submission.media) -> 'None'
#     print(submission.is_video) -> False
#
#     print(submission.subreddit_id)
#     print(submission.id)
#
#     print(submission.title)


def take_comments(submission_id: str, sort_filter="best"):
    '''
    Get the top 3 comments from the selected submission

    `submission_id`: Unique ID representation of submission
    `sort_filter`: Filter type for sorting comments of submission

    ```python
    take_comments("111aaa")
    take_comments("111aaa", sort_filter="top")
    ```
    '''

    submission = reddit.submission(submission_id)
    submission.comment_sort = sort_filter
    # filtered_comments = list(submission.comments)

    for e in list(submission.comments)[:3]:
        print("-----")
        print(e.author)
        print()
        print(e.body)
        print("-----")


# sub = reddit.submission('128ukfw')
# sub.comment_sort = "best"
# tlc = list(sub.comments)
# print(tlc[0].author)
# print(tlc[0].body)
# for c in tlc:
# Take the top 3 comments
# top_comments = c


# Coqui TTS

take_submission("askreddit", ratio=0.80)
# take_submission("askscience", ratio=0.80, score=0)
# take_submission("ProgrammerHumor", ratio=0.80, score=0)
