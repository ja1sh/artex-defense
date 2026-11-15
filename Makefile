.PHONY: test demo
test:
	python -m pytest -q
demo:
	PYTHONPATH=src python -m artex_defense.engine fixtures/positive.jsonl
