
# highlight different files
export CLICOLOR=1
export LSCOLORS=ExFxCxDxBxegedabagacad

# Erase duplicates
export HISTCONTROL=erasedups
#export PS1="\[\033[0;31m\]\W\[\033[0m\]$ "
export FIGNORE=$FIGNORE:.pyc:.DS_Store

export HTTP_HOST='localhost'
export ANDROID_HOME=~/android
export ANDROID_ROOT=$ANDROID_HOME
export NDK_ROOT=~/android-ndk-r8
export ENVSTUFF=~/personal/envstuff
export P4CONFIG=.p4config
export P4EDITOR=nano

export DCF_ROOT=~/apportable/apportable_sdk
export APPORTABLE_ANDROID_HOME=/Users/jeffreydecew/apportable/apportable_sdk/toolchain/macosx/android-sdk

export XCODE_BIN=/Applications/Xcode.app/Contents/Developer/usr/bin/

export ANDROID_PATH=$APPORTABLE_ANDROID_HOME/tools:$APPORTABLE_ANDROID_HOME/platform-tools
export PATH=$ANDROID_PATH:$PATH:/Developer/Marmalade/6.2/s3e/bin/:$DCF_ROOT/bin:$XCODE_BIN

source /usr/local/etc/bash_completion.d/git-completion.bash

c_cyan=`tput setaf 6`
c_red=`tput setaf 1`
c_green=`tput setaf 2`
c_sgr0=`tput sgr0`

parse_git_branch ()
{
  if git rev-parse --git-dir --no-color >/dev/null 2>&1
  then
          gitver="$(git branch --no-color 2>/dev/null| sed -n '/^\*/s/^\* //p')"
  else
          return 0
  fi
  echo -e $gitver
}

branch_color ()
{
        if git rev-parse --git-dir >/dev/null 2>&1
        then
                color=""
                if git diff --quiet 2>/dev/null >&2
                then
                        color="${c_green}"
                else
                        color="${c_red}"
                fi
        else
                return 0
        fi
        echo -ne $color
}

gl () {
    if [ -z "$1" ]
    then
        git log $(git merge-base origin/master HEAD)^.. --oneline
    else
	git log $(git merge-base origin/$1 HEAD)^.. --oneline
    fi
}

#PS1='\[${c_cyan}\]\W\[${c_sgr0}\] (\[$(branch_color)\]$(parse_git_branch)\[${c_sgr0}\])$ '
PS1='\[$(branch_color)\]$(parse_git_branch)\[${c_sgr0}\]:\[${c_cyan}\]\W\[${c_sgr0}\]$ '

# bash aliases
alias .="pwd"
alias la="ls -a"
alias lsla="ls -la"
alias where="pwd"

# git alias
alias gs="git status"
alias gd="git diff"
alias gld='gl dragonwithassets'
#alias jgpp="git pull && ant clean test && git push"
#alias cops="git co ~/workspace/tapzooandroid/*/project.properties"
alias gb="python ~/personal/envstuff/bash_utils.py git_branch_status"
alias gf="git fetch && gb"
alias pt="adb pull /mnt/sdcard/IwTrace.txt"
alias gu="git submodule update --init --recursive"
alias svnpp="cd ~/openpath/svn/ && git svn fetch && git co svn-tracker && git rebase && git co master && git rebase svn-tracker && git push github master && git co working && git rebase master"
alias gitrmdeleted='git status --porcelain | grep "^ D " | sed "s/^ D //" | xargs git rm'

# marmalade aliases
alias mkb60="/Developer/Marmalade/6.0/s3e/bin/mkb"
alias mkb61="/Developer/Marmalade/6.1/s3e/bin/mkb"
alias mkb62="/Developer/Marmalade/6.2/s3e/bin/mkb"
alias p4login="p4 login < $ENVSTUFF/secret/.iw3d-p4.pass"
alias p4pp="cd ~/marmalade/pcove/pocketgems && p4login && $ENVSTUFF/android/p4pp.sh"
alias p4tunnel="$ENVSTUFF/secret/p4tunnel.sh"
alias tunnelfix="$ENVSTUFF/android/tunnelfix.sh"
alias marmaladefix="$ENVSTUFF/android/marmaladefix.sh"
alias apksign="~/workspace/androidsigning/tools/apksign.py"
alias apkmod="~/workspace/androidsigning/tools/apkmod.py"
alias keygen="~/workspace/androidsigning/tools/keygen.py"
