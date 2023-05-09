'''
Runs headless browser, locates some elements on the webpage and combine them into single screenshot.
'''

from pathlib import Path

from playwright.sync_api import sync_playwright, FloatRect

from PIL import Image

from models.submission_model import SubmissionModel

# "https://www.reddit.com/comments/{submission_id}/comment/{comment_id}"
TITLE_URL = "https://www.reddit.com/comments/{}"
URL = "https://www.reddit.com/comments/{}/comment/{}"

PATH_TO_ASSETS: Path = Path('./temp_assets')


def take_screenshot(model: SubmissionModel) -> None:
    '''
    Take screenshot of the title and comments by submission_id and comment_id

    @param model: Submission model to take screenshots.
    @type model: SubmissionModel
    '''

    with sync_playwright() as p:
        path = PATH_TO_ASSETS.joinpath(model.submission_id)

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Take screenshot of title.
        page.goto(TITLE_URL.format(model.submission_id))
        title_element = page.locator(f"#t3_{model.submission_id}")
        title_element.screenshot(path=f'{path}/title.png')
        __reduce_transparency(path, 'title.png')

        # Take screenshot of each comment.
        for comment_id in model.comments:
            page.goto(URL.format(model.submission_id, comment_id))

            box_header = page.locator('.summary-flex').first.bounding_box()
            box_body = page.locator(
                'xpath=/html/body/shreddit-app/div/div[2]/shreddit-comment-tree/shreddit-comment/div[2]/div').bounding_box()
            box_footer = page.locator(
                'xpath=/html/body/shreddit-app/div/div[2]/shreddit-comment-tree/shreddit-comment/shreddit-comment-action-row').bounding_box()

            if box_header and box_body and box_footer:
                combined_box: FloatRect = {
                    'x': min(box_header['x'], box_body['x'], box_footer['x']),
                    'y': min(box_header['y'], box_body['y'], box_footer['y']),
                    'width': max(box_header['x'] + box_header['width'], box_body['x'] + box_body['width'], box_footer['x'] + box_footer['width']) - min(box_header['x'], box_body['x'], box_footer['x']),
                    'height': max(box_header['y'] + box_header['height'], box_body['y'] + box_body['height'], box_footer['y'] + box_footer['height']) - min(box_header['y'], box_body['y'], box_footer['y'])
                }
                page.screenshot(
                    path=f'{path}/{comment_id}.png', clip=combined_box)
                __reduce_transparency(path, f'{comment_id}.png')
            else:
                print("One or more elements not found on page.")

        browser.close()


def __reduce_transparency(path: Path, img_name: str) -> None:
    '''
    Reduce the transparency of the the image to 80%

    @param path: Directory path of the image
    @type path: Path

    @param img_name: Name of the image file
    @type img_name: str
    '''

    # alpha = 204  # 80% transparency
    alpha = 230  # 90% transparency

    img = Image.open(f'{path}/{img_name}')
    img.putalpha(alpha)

    img.save(f'{path}/{img_name}')
