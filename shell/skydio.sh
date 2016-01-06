# add aircam home
export AIRCAM=~/aircam

# add aircam tools
# legacy
export PATH=$PATH:$AIRCAM/build/bin
export PATH=$PATH:$AIRCAM/build/third_party/bin
# new
export PATH=$PATH:$AIRCAM/build/host_aircam/bin
export PATH=$PATH:$AIRCAM/build/host_third_party/bin
