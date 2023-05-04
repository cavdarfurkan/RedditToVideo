'''Main Script'''


from reddit_scraper import take_submissions
import image_scraper

submissions = take_submissions("askreddit", ratio=0, score=1500)

for sub in submissions:
    image_scraper.take_screenshot(sub)

# if submissions:
#     # List is not empty
#     for submission in submissions:
#         tts.save_audio(submission.title[1], 'title')
#         for comment in submission.comments:
#             tts.save_audio(comment[1], comment[0])
# else:
#     # List is empty
#     pass

# if submissions:
#     print("list is not empty")
#     for x in submissions:
#         print(x.title[1])
#         print(len(x.comments))
#         for c in x.comments:
#             print(f"-----{c[0]}-----")
#             print(c[1])
#             print("----------")
# if not submissions:
#     print("list is empty")
