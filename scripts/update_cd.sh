#!/bin/bash
# For certain websites to work properly we need to modify the chromedriver
# executable as per this link:
# https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver

filename="${1:-/opt/chrome/chrome}"
export LC_ALL=C
sed -i '' -e 's/cdc_/dog_/g' "$filename"
sed -i '' -e 's/wdc_/cat_/g' "$filename"
sed -i '' -e 's/selenium/chocolat/g' "$filename"
