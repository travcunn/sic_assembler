clean:
	find . -name *.pyc -delete
	rm build -rf
	rm dist -rf
	rm sic_assembler.egg-info -rf

develop:
	python setup.py develop

install:
	python setup.py install

test:
	coverage run tests.py

uninstall:
	pip uninstall sic_assembler
