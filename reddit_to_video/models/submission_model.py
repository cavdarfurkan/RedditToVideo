'''Model for creating submission objects.'''


class SubmissionModel:
    '''
    @param submission_id: Unique identifier of submission.

    @param title: Title of the submission. ['Author', 'Title']
    @type title: tuple

    @param comments: Comments of the sumbission. list[['Author', 'Comment']]
    @type comments: list[tuple]
    '''

    def __init__(self, submission_id, title: tuple, comments: list[tuple]) -> None:
        self.submission_id = submission_id
        self.title = title
        self.comments = comments
