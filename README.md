# Reddit to Video Bot

## Build

---

> Run the command below where **makefile** is located to build the project.
>
> ```shell
> make
> ```
>
> If you run ```make``` sucessfully, then no need to do the other steps.

> Run the command below where **makefile** is located to build the **venv** and install required dependencies.
>
> ```shell
> make venv
> ```

> Run the command below where **makefile** is located to build the **praw.ini**.
>
> ```shell
> make praw.ini
> ```
>
> You wil be asked to enter credentials for **praw.ini**.

> Run the command below where **makefile** is located to delete the **venv** and **praw.ini**.
>
> ```shell
> make clean
> ```

If ```make``` is succesfully completed, you don't need to do anything else except background videos.

---

## Praw

_praw.ini_ is required at the root directory of the project.

Can be built with '```make praw.ini```'.

Example:

```ini
[bot1]
client_id=yourClientId
client_secret=yourSecretId
user_agent=userAgentName
```

---

## Playwright

To install browsers run in the terminal.

```shell
playwright install
```

Or run '```make venv```' in the terminal.

---

## Subreddits

You can add, remove or change the configuration for subreddits from [subreddits.json](./data/subreddits.json)

---

## Background Videos

You can find and download the background videos from the releases or you can use your own custom videos.

After downloading background videos, place them inside _background_videos_ folder which is located at the root of the project.

Videos should be 60 seconds long as the script will collect texts up to 60 seconds. Or maximum video duration should also be changed from the script.
