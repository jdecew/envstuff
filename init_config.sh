# Turn off the dashboard pane of OSX
./dashboard.sh off

# Change the default behavior of "git push" to only push the current branch
# http://stackoverflow.com/questions/948354/git-push-current-branch
git config --global --add push.default upstream

# Add the breadcrumbs to the bottom of finder
# http://knoopx.net/2011/10/28/os-x-lion-tweaks
defaults write com.apple.finder ShowPathbar -bool true

# terminal keybindings (MANUAL)
# http://fplanque.com/dev/mac/mac-osx-terminal-page-up-down-home-end-of-line