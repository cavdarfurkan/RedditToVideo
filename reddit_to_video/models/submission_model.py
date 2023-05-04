'''Model for creating submission objects.'''

from typing import List
from pathlib import Path


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
        # self.generate_assets()

    def generate_assets(self):
        '''Make new directory named with submission_id and generate assets for the submission'''

        dir_path: Path = Path(self.submission_id)

        if not dir_path.exists():
            try:
                dir_path.mkdir()
                # tts.
            except FileExistsError:
                print("File Exists Error")
