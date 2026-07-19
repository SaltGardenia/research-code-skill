.PHONY: train test test-full format clean sync

train:
	python src/train.py

test:
	pytest

test-full:
	pytest -m slow

format:
	pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

sync:
	git pull
