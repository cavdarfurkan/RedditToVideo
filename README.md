# Reddit to Video Bot

## Build

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

If ```make``` is succesfully completed:

* Make sure playwright browsers are installed.
* Install ImageMagick. Required for watermark.
* Edit the watermark text.
* Add background videos.
* Edit the configuration for subreddits.

## Run

Run from the project's root folder.

```shell
python reddit_to_video/main.py
```

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

## Playwright

To install browsers run in the terminal.

```shell
playwright install
```

Or run '```make venv```' in the terminal.

## ImageMagick

ImageMagick is required to be able to add watermark to videos.

If you are getting security policy error, go to ```/etc/ImageMagick-6/policy.xml``` and comment out the following line:

```<policy domain="path" rights="none" pattern="@*"/>```

### Windows

You can install it from the offical website.
You may also need to set the path.

### Linux

You can install it with your package manager.

## Subreddits

You can add, remove or change the configuration for subreddits from [subreddits.json](./data/subreddits.json)

## Background Videos

You can find and download the background videos from the releases or you can use your own custom videos.

After downloading background videos, place them inside _background_videos_ folder which is located at the root of the project.

Videos should be 60 seconds long as the script will collect texts up to 60 seconds. Or maximum video duration should also be changed from the script.
