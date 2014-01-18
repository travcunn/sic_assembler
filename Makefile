test:
		coverage run tests.py

verify:
		pyflakes sic_assembler

install:
		python setup.py install

clean:
		find . -name *.pyc -delete
