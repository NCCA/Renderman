TARGET=d_sdldisplaydriver.so
QMAKE_LFLAGS += -shared
CONFIG -= app_bundle
CONFIG += console
QT+=opengl
CONFIG+=c++11
#LIBS+= -L $(RMANTREE)/lib -lrix
SOURCES+=$$PWD/src/driver.cpp \
         $$PWD/src/SDLOpenGL.cpp

HEADERS+=$$PWD/include/SDLOpenGL.h

INCLUDEPATH+=$$PWD/include
OTHER_FILES+=$$PWD/rgb.rib
INCLUDEPATH+=$(RMANTREE)/include
# this demo uses SDL so add the paths using the sdl2-config tool
QMAKE_CXXFLAGS+=$$system(sdl2-config  --cflags)
message(output from sdl2-config --cflags added to CXXFLAGS= $$QMAKE_CXXFLAGS)

LIBS+=$$system(sdl2-config  --libs)
message(output from sdl2-config --libs added to LIB=$$LIBS)
