# add aircam home
export AIRCAM=~/aircam

# add aircam tools
export PATH=$PATH:$AIRCAM/build/host_aircam/bin
export PATH=$PATH:$AIRCAM/build/host_third_party/bin

# add python site packages to path (mac specific)
export PYTHON_SITE=~/Library/Python/2.7/bin
export PATH=$PATH:$PYTHON_SITE

# renderworld fix
export OSG_LIBRARY_PATH=/home/skydio/aircam/build/host_third_party/lib

# fix username mismatch
export SKYREV_REMOTE_USERNAME=jeff
