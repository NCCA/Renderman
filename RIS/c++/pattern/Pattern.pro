CONFIG-=qt
CONFIG-=app_bundle
QMAKE_CXXFLAGS=-Wno-deprecated -fPIC
INCLUDEPATH+=$(RMANTREE)/include
QMAKE_LFLAGS+=-shared
SOURCES+=PxrFractal.cpp
TARGET=PxrMyFractal.so
macx:QMAKE_MAC_SDK = macosx10.12
CONFIG+=c++11
macx:QMAKE_LFLAGS-= -stdlib=libc++
OTHER_FILES+=pattern.py
