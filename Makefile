test:
		coverage run tests.py

verify:
		pyflakes src/sic_assembler
		pep8 --ignore=E501, E225 src/sic_assembler

install:
		python setup.py install

clean:
		find . -name *.pyc -delete
		rm build -rf
		rm dist -rf
		rm src/sic_assembler.egg-info -rf
