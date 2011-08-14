#!/bin/bash

cd ~/Ogre3D
make
cp OgreApp dist/bin/OgreApp
cd ~/Ogre3D/dist/bin/
rm *.png -f
./OgreApp $1 $2
