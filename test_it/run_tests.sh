#!/usr/bin/env bash

for f in *.blend
do
  echo "Exporting ${f}"
  blender --background "${f}" --python run_export.py
done