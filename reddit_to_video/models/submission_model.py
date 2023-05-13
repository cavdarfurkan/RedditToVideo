'''Model for creating submission objects.'''

from typing import List


class SubmissionModel:
    '''
    @param submission_id: Unique identifier of submission.
    @type submission_id: str

    @param comments: Selected comments of the submission. Consist of comment_ids
    @type comments: list[str]
    '''

    def __init__(self, submission_id: str, comments: List[str]) -> None:
        self.submission_id = submission_id
        self.comments = comments
