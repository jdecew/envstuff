# add aircam home
export AIRCAM=~/aircam

# add aircam tools
# new paths
export PATH=$PATH:$AIRCAM/build/host_aircam/bin
export PATH=$PATH:$AIRCAM/build/host_third_party/bin
export PATH=/usr/local/ccache:$PATH
# legacy paths
export PATH=$PATH:$AIRCAM/build/bin
export PATH=$PATH:$AIRCAM/build/third_party/bin
