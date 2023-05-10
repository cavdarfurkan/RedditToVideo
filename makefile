VENV := myenv
PYTHON := ${VENV}/bin/python3
PIP := ${VENV}/bin/pip
BROWSER := ${VENV}/bin/playwright

all: ${VENV}/bin/activate praw.ini

${VENV}/bin/activate: requirements.txt
	python3 -m venv ${VENV}
	./${PIP} install -r requirements.txt
	${BROWSER} install

praw.ini: ${VENV}/bin/activate
	@echo "Enter your Reddit API credentials:"; \
	read -p "Client ID: " client_id; \
	read -p "Client secret: " client_secret; \
	read -p "User agent name: " user_agent; \
	echo "[VideoMakerBot]" > praw.ini; \
	echo "client_id=$$client_id" >> praw.ini; \
	echo "client_secret=$$client_secret" >> praw.ini; \
	echo "user_agent=$$user_agent" >> praw.ini
	
run: praw.ini
	./${PYTHON} reddit_to_video/main.py
	
clean:
	rm -rf ${VENV}
	find . -type f -name '*.pyc' -delete
	
.PHONY: all run clean
