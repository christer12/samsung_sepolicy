#!/bin/bash

for f in `ls *.te`
do
	sed -i "/mmcblk/d" $f
done
