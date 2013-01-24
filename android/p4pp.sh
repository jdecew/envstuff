## in the pocketgems repo
cd ~/marmalade/pcove/pocketgems
# pull p4 to local master
git p4 sync
git co p4master
git rebase

# pull to android_p4 and push to origin
git co android_p4
git rebase p4/master
git push origin android_p4
git co p4master


#don't run the rest of the script
exit 0
echo "ERROR: Execution should have stopped!"

#### 

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
git fetch shared
# pull p4 to local master
git p4 sync
git co master
git rebase
# pull to pocketgems_master and push to shared
git co pocketgems_master
git rebase p4/master
git push shared pocketgems_master
git co master


