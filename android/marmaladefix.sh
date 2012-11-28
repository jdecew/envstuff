cd /Developer/Marmalade/6.2/modules/third_party/cocotron/
cp cocotron.mkf cocotron.mkf.bak
echo $1 | grep -E -q '^[01]$' || { echo 'Argument must 1 (Sim-preferred) or 0 (ARM-safe), "'$1'" provided' ; exit 1; }
sed 's/{{ .* }}/{{ '$1' }}/' <cocotron.mkf.bak >cocotron.mkf
