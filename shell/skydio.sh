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
alias ca2="cd ~/aircam2"


# Alias for Yubikey pin prompt
alias yubact="ssh-add -e /usr/local/lib/opensc-pkcs11.so; ssh-add -s /usr/local/lib/opensc-pkcs11.so"

# # Auto finds ssh-agent
# . ~/yubikey_scripts/ssh-find-agent/ssh-find-agent.sh
# ssh_find_agent -a
# if [ -z "$SSH_AUTH_SOCK" ]
# then
#     eval $(ssh-agent) > /dev/null
#     ssh-add -l >/dev/null || alias ssh='ssh-add -l >/dev/null || ssh-add && unalias ssh; ssh'
# fi

# Auto prompt yubikey on new terminal
ioreg -p IOUSB | grep -i yubikey >/dev/null
YUBIKEY_STATUS=$?
ssh-add -L >/dev/null
ACTIVE_STATUS=$?
if [ $YUBIKEY_STATUS -eq 0 ] && [ $ACTIVE_STATUS -eq 1 ]; then
    yubact
fi
