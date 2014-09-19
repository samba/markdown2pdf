
.PHONY: package install clean submodules


# sudo easy_install pip

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	CPPFLAGS += -I/opt/X11/include 
endif

submodules:
	git submodule init
	git submodule update --recursive


package: submodules
	sudo python setup.py bdist_egg
	sudo python setup.py sdist

# On a Mac, installing Pillow will crash when it can't find "X11/Xlib.h"
# Workaround: add the X11 source context
install: submodules
	which pip || sudo easy_install pip
	CPPFLAGS="$(CPPFLAGS)" sudo -E pip install pillow xhtml2pdf
	sudo python setup.py install


clean: 
	sudo python setup.py clean
	@sudo rm -rf build/ dist/
	@sudo rm -rf *.egg-info
