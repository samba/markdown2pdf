
.PHONY: package install clean

package: 
	git submodule update
	sudo python setup.py bdist_egg
	sudo python setup.py sdist

install:
	git submodule update
	sudo python setup.py install


clean: 
	sudo python setup.py clean
	@sudo rm -rf build/ dist/
	@sudo rm -rf *.egg-info
