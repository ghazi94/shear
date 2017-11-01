#!/bin/bash

rm ~/Desktop/VMShare/shear/shear.zip
rm ~/Desktop/VMShare/shear.zip
zip -r ~/Desktop/VMShare/shear.zip *
cd /home/ghazi/Desktop/virtualEnvs/shear/lib/python3.6/site-packages
zip -ur ~/Desktop/VMShare/shear.zip *
cd ~/Desktop/VMShare/shear
mv ~/Desktop/VMShare/shear.zip shear.zip

