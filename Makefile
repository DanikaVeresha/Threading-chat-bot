install:
	pip install poetry && \
	poetry install

start:
	poetry run python trading_chatBot/tradingBot.py


