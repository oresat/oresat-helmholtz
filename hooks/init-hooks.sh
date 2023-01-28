#!/bin/sh

GIT_HOOKS_PATH=$PWD/.git/hooks
SH_NAME=$(echo $0 | rev | cut -d'/' -f1 | rev)
SH_PATH="$(dirname $0)"

for file in $(ls $SH_PATH); do
    if [[ "$file" == "$SH_NAME" ]]; then continue; fi
    strp_name="${file/\.sh/}"
    SRC="$SH_PATH/$file"
    DST="$GIT_HOOKS_PATH/$strp_name"
    echo -e "$SRC -> $DST"
    cp $SRC $DST
done