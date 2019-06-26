# add aircam tools
export PATH=$PATH:./build/host_aircam/bin
export PATH=$PATH:./build/host_third_party/bin
export PATH=$PATH:./build/host_aircam/bin/tests

# add python site packages to path (mac specific)
export PYTHON_SITE=~/Library/Python/2.7/bin
export PATH=$PATH:$PYTHON_SITE

# renderworld fix
export OSG_LIBRARY_PATH=/home/skydio/aircam/build/host_third_party/lib

# performance
export DISABLE_MOBILE_PTREE_CHECKING=1

# fix username mismatch
export SKYREV_REMOTE_USER=jeff

alias ca="cd ~/aircam"
