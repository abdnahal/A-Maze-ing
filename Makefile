.PHONY: install run debug clean lint lint-strict

install:
	pip install --break-system-packages mypy flake8

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ mazegen/__pycache__ .mypy_cache
	rm -f maze.txt

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

package:
    pip install --break-system-packages build
    python3 -m build
    cp dist/mazegen-*.tar.gz ./mazegen.tar.gz
    @echo "Package built: mazegen.tar.gz"
