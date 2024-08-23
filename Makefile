.PHONY: format

format:
	poetry run isort .
	poetry run black .
