all:
	python setup.py build
	cp build/lib.*/*.so .

test:
	py.test --doctest-modules

install:
	python setup.py install

clean:
	rm -f db.marshal *.so
	rm -rf build
	find . -name \*.pyc | xargs rm -f

apt-get-stuff-you-need:
	apt-get install build-essential python-dev libboost-python-dev

upgrade-static:
	rm -rf static/bootstrap
	git clone https://github.com/twitter/bootstrap.git static/bootstrap
	rm -rf static/bootstrap/.git
	make -C static/bootstrap bootstrap
	cp static/bootstrap/bootstrap/js/bootstrap.min.js static/js
