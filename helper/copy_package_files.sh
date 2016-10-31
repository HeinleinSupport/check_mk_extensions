#!/bin/bash

# copy the files from a package to the CWD

mkp list dovereplstat | while read file; do

  lfile=${file#$OMD_ROOT/local/share/check_mk}
  ldir=.$(dirname $lfile)
  mkdir -pv $ldir
  cp -av $file $ldir

done
