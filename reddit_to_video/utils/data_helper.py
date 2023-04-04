'''Visitor pattern for JSON data operations'''

from pathlib import Path
import json

# PATH_TO_DATA: str = "./reddit_to_video/data"
PATH_TO_DATA: Path = Path("./reddit_to_video/data")


#TODO: check submissions.json and subreddits.json if exists


# Element
class DataElement:
    '''Abstract-like class for Data Elements(Visitee).'''

    def accept(self, visitor: 'DataOperationVisitor') -> None:
        '''
        Accept an operation and visit that operation.

        @param visitor: Data Operation to visit.
        @type visitor: DataOperationVisitor
        '''
        visitor.visit(self)


# Visitor
class DataOperationVisitor:
    '''Abstract-like class for visitiors(operations).'''

    def visit(self, element: 'DataElement') -> None:
        '''Abstract method for visiting Data Element.'''


# Elements
class SubredditsData(DataElement):
    '''Element for `subreddits.json`.\n
    Data operations visits here.'''

    def read_json(self) -> None:
        '''Read data inside `subreddits.json`'''
        try:
            with open(PATH_TO_DATA.joinpath("subreddits.json"), 'r', encoding="utf-8") as f:
                # with open(PATH_TO_DATA + "/subreddits.json", 'r', encoding="utf-8") as f:
                data = json.load(f)
            print(data)
        except Exception as exc:
            print(f"Error reading file: {str(exc)}")

    def write_json(self, json_data: str) -> None:
        '''
        Write data to `subreddits.json`

        @param json_data: Data to write in JSON format.
        @type json_data: str
        '''
        try:
            with open(PATH_TO_DATA.joinpath("subreddits.json"), 'w', encoding="utf-8") as f:
                json.dump(json_data, f)
        except Exception as exc:
            print(f"Error writing file: {str(exc)}")


class SubmissionsData(DataElement):
    '''Element for `submissions.json`.\n
    Data operations visits here.'''

    def read_json(self) -> None:
        '''Read data inside `submissions.json`'''
        try:
            with open(PATH_TO_DATA.joinpath("submissions.json"), 'r', encoding="utf-8") as f:
                data = json.load(f)
            print(data)
        except Exception as exc:
            print(f"Error reading file: {str(exc)}")

    def write_json(self, json_data: str) -> None:
        '''
        Write data to `submissions.json`

        @param json_data: Data to write in JSON format.
        @type json_data: str
        '''
        try:
            with open(PATH_TO_DATA.joinpath("submissions.json"), 'w', encoding="utf-8") as f:
                json.dump(json_data, f)
        except Exception as exc:
            print(f"Error writing file: {str(exc)}")


# Visitors
class ReadJsonVisitor(DataOperationVisitor):
    '''Read Operation that will visit based on the element type'''

    def visit(self, element: 'DataElement') -> None:
        if isinstance(element, SubredditsData):
            element.read_json()
        elif isinstance(element, SubmissionsData):
            element.read_json()


class WriteJsonVisitor(DataOperationVisitor):
    '''
    Write Operation that will visit based on the element type

    @param json_data: Data to write in JSON format.
    @type json_data: str
    '''

    def __init__(self, json_data: str) -> None:
        self.json_data = json_data

    #TODO: Validate the JSON before writing, if not valid: raise exception

    def visit(self, element: 'DataElement'):
        if isinstance(element, SubredditsData):
            element.write_json(self.json_data)
        elif isinstance(element, SubmissionsData):
            element.write_json(self.json_data)
