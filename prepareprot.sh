#!/usr/bin/env bash
mkdir ./receptor/rawpdbs
mv ./receptor/$1.pdb ./receptor/rawpdbs/$1_raw.pdb
grep ATOM ./receptor/rawpdbs/$1_raw.pdb > ./receptor/$1.pdb