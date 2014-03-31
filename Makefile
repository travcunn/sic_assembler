test:
		coverage run tests.py

verify:
		pyflakes sic_assembler
		pep8 --ignore=E501, E225 sic_assembler

install:
		python setup.py install

clean:
		find . -name *.pyc -delete
		rm build -rf
		rm dist -rf
		rm sic_assembler.egg-info -rf
