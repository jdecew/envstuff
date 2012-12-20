echo $1 | grep -E -q '^(on|off)$' || { echo 'Argument must be "on" or "off", "'$1'" provided' ; exit 1; }
if [ $1 == 'on' ] ; then
   sed -i '.bak' 's/^P4PORT=.*$/P4PORT=localhost:1666/' ~/marmalade/pcove/.p4config
fi
if [ $1 == 'off' ] ; then
   sed -i '.bak' 's/^P4PORT=.*$/P4PORT=inbound.iw3d.co.uk:1666/' ~/marmalade/pcove/.p4config
fi