# My first BASH script!
# This script toggles the OSX Dashboard feature.

if [ -z "$1" ]; then
  echo "execute this script with either 'on' or 'off' as the only argument"
  exit 1
fi

if [ $1 == "off" ]; then
  echo "TURNING DASHBOARD OFF"
  defaults write com.apple.dashboard mcx-disabled -boolean YES
  killall Dock
  echo "OK"
elif [ $1 == "on" ]; then
  echo "TURNING DASHBOARD ON"
  defaults write com.apple.dashboard mcx-disabled -boolean NO
  killall Dock
  echo "OK"
else
  echo "Invalid options: execute with either 'on' or 'off' as the only argument"
  exit 1
fi