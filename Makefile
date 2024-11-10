dist:
	python setup.py build sdist bdist_wheel

.PHONY: build
build:
	python setup.py build_ext --inplace

test:
	pytest tests.py

.PHONY: suitesparse
suitesparse:
	rm -rf suitesparse
	git clone --depth 1 --branch v7.2.0 https://github.com/DrTimothyAldenDavis/SuiteSparse suitesparse || true
	cd suitesparse && rm -rf .git

.PHONY: xla
xla:
	rm -rf xla
	git clone --depth 1 --branch main https://github.com/openxla/xla
	cd xla && rm -rf .git

clean:
	find . -not -path "./suitesparse*"  -not -path "./xla*" -name "dist" | xargs rm -rf
	find . -not -path "./suitesparse*"  -not -path "./xla*" -name "build" | xargs rm -rf
	find . -not -path "./suitesparse*"  -not -path "./xla*" -name "builds" | xargs rm -rf
	find . -not -path "./suitesparse*"  -not -path "./xla*" -name "__pycache__" | xargs rm -rf
	find . -not -path "./suitesparse*"  -not -path "./xla*" -name "*.so" | xargs rm -rf
	find . -not -path "./suitesparse*"  -not -path "./xla*" -name "*.egg-info" | xargs rm -rf
	find . -not -path "./suitesparse*"  -not -path "./xla*" -name ".ipynb_checkpoints" | xargs rm -rf
	find . -not -path "./suitesparse*"  -not -path "./xla*" -name ".pytest_cache" | xargs rm -rf

