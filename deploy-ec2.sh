#!/bin/bash

rm ~/shear.zip
rm ~/shear/shear.zip
zip -r ~/shear.zip *
cd ~/shearvenv/lib/python3.6/site-packages
zip -ur ~/shear.zip *
cd ~
mv ~/shear.zip ~/shear/shear.zip

