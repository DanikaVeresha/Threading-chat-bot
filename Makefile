install:
	pip install poetry && \
	poetry install

start:
	poetry run python Serverbot/tradingBot.py


