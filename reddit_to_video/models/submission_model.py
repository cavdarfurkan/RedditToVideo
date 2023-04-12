'''Model for creating submission objects.'''


class SubmissionModel:
    '''
    @param title: Title of the submission. ['Author', 'Title']
    @type title: tuple

    @param comments: Comments of the sumbission. list[['Author', 'Comment']]
    @type comments: list[tuple]
    '''

    def __init__(self, title: tuple, comments: list[tuple]) -> None:
        self.title = title
        self.comments = comments
