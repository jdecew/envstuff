cd /Developer/Marmalade/6.1/modules/third_party/cocotron/
cp cocotron.mkf cocotron.mkf.bak
sed 's/{{ 1 }}/{{ 0 }}/' <cocotron.mkf.bak >cocotron.mkf
