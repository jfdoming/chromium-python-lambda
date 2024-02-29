#!/bin/bash
# For certain websites to work properly we need to modify the chromedriver
# executable as per this link:
# https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver

filename="${1:-/opt/chrome/chrome}"
sed_cmd="sed -i"
if [ "$(uname)" == "Darwin" ]; then
    sed_cmd="sed -i ''"
fi
export LC_ALL=C

$sed_cmd -e 's/cdc_/dog_/g' "$filename"
$sed_cmd -e 's/wdc_/cat_/g' "$filename"
$sed_cmd -e 's/selenium/chocolat/g' "$filename"
