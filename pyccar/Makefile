ifneq ("$(wildcard /usr/include/linux/input.h)","")
LINUX_INPUT=1
else
LINUX_INPUT=0
endif

CFLAGS=$(shell python3-config --cflags) -DHAVE_LINUX_INPUT_H=$(LINUX_INPUT)
LDFLAGS=$(shell python3-config --ldflags)

all:	pyccar

runcar:	pyccar
	PYTHONPATH=`pwd` ./pyccar --fb-touch

runX:	pyccar
	PYTHONPATH=`pwd` ./pyccar --timeout

runfb0:	pyccar
	PYTHONPATH=`pwd` ./pyccar --fb-touch --timeout

runfb1:	pyccar
	PYTHONPATH=`pwd` ./pyccar --fb-touch --fb-device=/dev/fb1 --timeout

clean:
	rm -f *~ *.o

ALL_OBJECTS=\
	pyccar.o \
	TouchInput.o \
	Window.o \
	PyCCarUI.o

ALL_SOURCES=\
	pyccar.cc \
	TouchInput.cc \
	Window.cc \
	PyCCarUI.cc

ALL_HEADERS=\
	BBox.hh \
	TouchInput.hh \
	Window.hh \
	pyccar.hh

OTHER_FILES=\
	Makefile \
	pyccarui.py

pyccar:		$(ALL_OBJECTS)
		c++ -o pyccar $(ALL_OBJECTS) $(LDFLAGS)

%.o:	%.cc $(ALL_HEADERS)
	c++ -c $< -o $@ $(CFLAGS)
