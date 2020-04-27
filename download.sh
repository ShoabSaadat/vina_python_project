#!/usr/bin/env bash
wget https://de.cyverse.org/dl/d/6FE1A5C4-4140-420E-8F32-4EC6250E16D5/vina_prep.zip
unzip vina_prep.zip
mv ./vina_prep ./Vina_Project
rm vina_prep.zip 
cd Vina_Project
