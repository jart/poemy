test:
	py.test --doctest-modules

upgrade-static:
	rm -rf static/bootstrap
	git clone https://github.com/twitter/bootstrap.git static/bootstrap
	rm -rf static/bootstrap/.git
	make -C static/bootstrap bootstrap
	cp static/bootstrap/bootstrap/js/bootstrap.min.js static/js
