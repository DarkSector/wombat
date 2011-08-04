inst_HEADERS= BaseApplication.h TutorialApplication.h
instdir= "/home/darksector/gamecode/ogre3d"
ACLOCAL_AMFLAGS = -I m4
bin_PROGRAMS= OgreApp
OgreApp_CPPFLAGS= -I$(top_srcdir)
OgreApp_SOURCES= BaseApplication.cpp TutorialApplication.cpp
OgreApp_CXXFLAGS= $(OGRE_CFLAGS) $(OIS_CFLAGS)
OgreApp_LDADD= $(OGRE_LIBS) $(OIS_LIBS) -lGL

EXTRA_DIST = bootstrap
AUTOMAKE_OPTIONS = foreign
