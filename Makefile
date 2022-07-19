venv:
	python3 -m virtualenv venv

test-rate:
	python main.py --coinmetro --exchangerate

test-historic:
	python main.py --coinmetro --historicdata

test-historic-write:
	python main.py --coinmetro --historicdata --savedata