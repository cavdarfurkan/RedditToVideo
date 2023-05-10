# Reddit to Video Bot

> You can download the background videos from the releases.

Run the below command where makefile is located to build in a venv.

```
make
```

Run the below command where makefile is located to build in a venv and then run.

```
make run
```

You wil be asked to enter credentials for 'praw.ini'.

If make is succesfully completed, you can skip the steps below.

---

## Praw

*praw.ini* is required at the root directory of the project.

Example:

```ini
[bot1]
client_id=yourClientId
client_secret=yourSecretId
user_agent=userAgentName
```

---

## Coqui

~/.local/share/tts has the tts models

---

## Playwright

To install browsers

```
playwright install
```

---
