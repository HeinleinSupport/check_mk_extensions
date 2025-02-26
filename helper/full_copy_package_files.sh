#!/bin/bash

# copy the files from a package to the CWD

if [ -n "$1" ]; then
  package="$1"
else
  package=$(basename $(pwd))
fi

if ! mkp show "$package" > /dev/null; then
  echo Package "$package" does not exist
  exit 1
fi

mkp files "$package" | while read file; do

  lfile=${file#$OMD_ROOT}
  ldir=.$(dirname "$lfile")
  mkdir -pv "$ldir"
  cp -av "$file" "$ldir"

done

cp -av $OMD_ROOT/var/check_mk/packages/"$package" .
