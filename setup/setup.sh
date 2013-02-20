ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
source $ROOT_DIR/confirm.sh

confirm "This will overwrite your ~/.bash_profile!!  Do you want to continue?"
if [ $? -eq 0 ]
then
    echo source "$ROOT_DIR/bash_profile" > ~/.bash_profile
    echo "Overwrote ~/.bash_profile!"
else
    echo "No changes made!"
fi

confirm "This will overwrite your ~/Library/KeyBindings/!!  Do you want to continue?"
if [ $? -eq 0 ]
then
cp -r KeyBindings ~/Library
echo "Overwrote ~/Library/KeyBindings/!"
else
echo "No changes made!"
fi

