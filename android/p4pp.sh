## in the i3d repo
cd ~/marmalade/pcove/i3d
git fetch
# pull p4 to local master
git p4 sync
git co master
git rebase
# pull to i3d_master and push to shared
git co i3d_master
git rebase p4/master
git push shared i3d_master

## in the pocketgems repo
cd ~/marmalade/pcove/pocketgems
git fetch
# pull p4 to local master
git p4 sync
git co master
git rebase
# pull to pocketgems_master and push to shared
git co pocketgems_master
git rebase p4/master
git push shared pocketgems_master



