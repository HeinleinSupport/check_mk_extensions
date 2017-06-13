#!/bin/bash

# copy the files from a package to the CWD

mkp list "$1" | while read file; do

  lfile=${file#$OMD_ROOT/local/share/check_mk}
  lfile=${lfile#$OMD_ROOT/local}
  ldir=.$(dirname $lfile)
  mkdir -pv $ldir
  cp -av $file $ldir

done
