
# highlight different files
export CLICOLOR=1
export LSCOLORS=ExFxCxDxBxegedabagacad

# Erase duplicates
export HISTCONTROL=erasedups
#export PS1="\[\033[0;31m\]\W\[\033[0m\]$ "
export FIGNORE=$FIGNORE:.pyc:.DS_Store

export HTTP_HOST='localhost'
export ANDROID_HOME=~/android

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

# git alias
alias gs="git status"
alias gd="git diff"
alias gld='gl dragon'
alias jgpp="git pull && ant clean test && git push"
alias la="ls -a"
alias lsla="ls -la"
alias where=pwd
alias cops="git co ~/workspace/tapzooandroid/*/project.properties"
alias gb="python ~/personal/envstuff/bash_utils.py git_branch_status"
