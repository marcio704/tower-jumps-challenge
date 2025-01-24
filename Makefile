.PHONY: install
install:
	pipenv install --dev

.PHONY: path
export PYTHONPATH=.
path: 

.PHONY: run-simple-solution
run-simple-solution: path
	pipenv run python src/simple_solution/towerjumps.py

.PHONY: run-accurate-solution
run-accurate-solution: path
	pipenv run python src/accurate_solution/towerjumps.py

.PHONY: run-duration-based-solution
run-duration-based-solution: path
	pipenv run python src/duration_based_solution/towerjumps.py $(START_DATE) $(END_DATE)


.PHONY: generate-heatmap
generate-heatmap: path
	pipenv run python src/generate-heatmap.py $(START_DATE) $(END_DATE)

.PHONY: tests
tests: path install
	pipenv run python3 -m pytest src/tests/tests.py
