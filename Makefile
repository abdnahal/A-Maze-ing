.PHONY: install run debug clean lint lint-strict package

install:
	pip install --break-system-packages mypy flake8

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf pycache mazegen/pycache .mypy_cache dist build mazegen.egg-info
	rm -f maze.txt

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

package:
	pip install --break-system-packages build
	python3 -m build --outdir .
	rm -f mazegen-*.whl
	@echo "Package built: mazegen-1.0.0.tar.gz"
