import argparse
import os
import random
import re
import subprocess
import sys

class BC:
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[30m'
    RED = '\033[31m'
    RED_BOLD = '\033[1;31m'
    GREEN = '\033[32m'
    GREEN_BOLD = '\033[1;32m'
    YELLOW = '\033[33m'
    YELLOW_BOLD = '\033[1;33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    ENDC = '\033[0m'

    def disable(self):
        self.RED = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.BLUE = ''
        self.PURPLE = ''
        self.CYAN = ''
        self.ENDC = ''

def main():
    if len(sys.argv)==1:
        print "Which util? -- [git_branch_status]"
        return 1
    if sys.argv[1] == "git_branch_status":
        return git_branch_status(sys.argv[2:])
    if sys.argv[1] == "git_branch_pull_upstream":
        return git_branch_pull_upstream(sys.argv[2:])
    if sys.argv[1] == "test":
        return test(sys.argv[2:])
    print "Unknown util: "+sys.argv[1]
    return 1

def git_branch_pull_upstream(rawargs):
    parser = argparse.ArgumentParser(prog='git_branch_pull_upstream')
    parser.add_argument('localbranch', help='local branch')
    parser.add_argument('--dryrun', '-n', action='store_true', help='dry run')
    parser.add_argument('--force', '-f', action='store_true', help='force')
    parser.add_argument('--quiet', '-q', action='store_true', help='quiet')
    args = parser.parse_args(rawargs)

    dryrun = not not args.dryrun
    force = not not args.force
    loud = not args.quiet
    branch = args.localbranch
    localbranches = bash_output("git branch --no-color --list '%s'" % branch)
    if localbranches is None:
        # not a git repo; user already warned via stdout
        return 1
    if localbranches not in ("  "+branch+"\n", "* "+branch+"\n"):
        print localbranches
        print "error: '%s' is not a local branch" % branch
        return 1
    upstream = bash_output("git for-each-ref --format='%%(upstream:short)' -- 'refs/heads/%s'" % branch).strip()
    if not upstream:
        print "error: '%s' has no upstream" % branch
        return 1
    branch_sha = git_merge_base(branch)
    upstream_sha = git_merge_base(upstream)
    if branch_sha == upstream_sha:
        print "Already up to date."
        return 1
    mergebase = git_merge_base(branch_sha, upstream_sha)
    ahead = git_diff_count(mergebase, branch_sha)
    behind = git_diff_count(mergebase, upstream_sha)
    plus = colored("+%d" % ahead, BC.GREEN_BOLD) if ahead else ""
    minus = colored("-%d" % behind, BC.RED_BOLD) if behind else ""
    plusminus = "<%s>" % ("%s %s" % (plus, minus)).strip()
    if ahead and not force:
        print "error: can't pull %s upstream to %s <+%s -%s> (%s..%s) (Forced update required)" % (branch, upstream, ahead, behind, branch_sha[:7], upstream_sha[:7])
        return 1
    verb = "would pull" if dryrun else "pulling"
    print "%s %s upstream to %s %s (%s..%s)" % colored_l((verb, branch, upstream, plusminus, branch_sha[:7], upstream_sha[:7]), (None, BC.GREEN, BC.CYAN, None, None, None))
    if dryrun:
        return 0
    gitfolder = get_git_folder()
    reffile = os.path.join(gitfolder, "refs", "heads", branch)
    if os.path.isfile(reffile):
        with open(reffile) as f:
            if f.read() != branch_sha + "\n":
                print "fatal: reffile contents not as expected"
                return 1
    elif os.path.exists(reffile):
        print "fatal: reffile exists but not a file: %s" % reffile
        return 1
    else:
        print "warning: creating nonexistent reffile (did you run 'git remote prune'?)"
    with open(reffile,'w') as f:
        f.write(upstream_sha+"\n")
    return 0
    
def git_branch_status(rawargs):
    parser = argparse.ArgumentParser(prog='git_branch_status')
    parser.add_argument('--verbose', '-v', action='store_true', help='include commit message')
    args = parser.parse_args(rawargs)

    verbose = not not args.verbose
    output = bash_output('git branch --no-color -v -v')
    if not output:
        return 1
    lines = output.splitlines()
    rows = []
    lm = re.compile("(?P<current>[*]?)\s*(?P<local>(\S|no branch|detached from [^ )]+)+)(?P<localpad>\s+?)(?P<sha>[0-9a-f]+)\s+(?P<fullmessage>(\[(?P<remote>[^]]+)\])? ?(?P<message>.*))$")
    rm = re.compile("(?P<branch>\S+)(:|$)\s*(ahead (?P<ahead>\d+))?,?\s*(behind (?P<behind>\d+))?") #origin/foo: ahead 5, behind 5
    for line in lines:
        line = line.strip()
        row = {"padding":"#  "}
        rows.append(row)
        match = lm.match(line)
        if not match: print repr(line)
        remote = match.group("remote") if match.group("remote") else ""
        row["sha"] = BC.LIGHT_GRAY+match.group("sha")+BC.ENDC
        row["message"] = BC.LIGHT_GRAY+match.group("message")+BC.ENDC
        row["current"] = BC.YELLOW+u"\u2713"+BC.ENDC if match.group("current") else ""
        color = BC.GREEN if match.group("current") else ""
        row["branch"] = color+match.group("local")+BC.ENDC+" "
        if remote:
            rmatch = rm.match(remote)
            if rmatch:
                row["ahead"] = BC.GREEN_BOLD+"+"+rmatch.group("ahead")+BC.ENDC if rmatch.group("ahead") else ""
                row["behind"] = BC.RED_BOLD+"-"+rmatch.group("behind")+BC.ENDC if rmatch.group("behind") else ""
                row["remoteBranch"] = BC.CYAN+rmatch.group("branch")+BC.ENDC
            else:
                row["message"] = BC.LIGHT_GRAY+match.group("fullmessage")+BC.ENDC
        if not remote or not rmatch:
            row["ahead"] = ""
            row["behind"] = ""
            row["remoteBranch"] = BC.PURPLE+"<local>"+BC.ENDC
    cols = ["padding","branch","current","ahead","behind","remoteBranch","sha"]
    if verbose: cols += ["message"]
    counts={}
    for col in cols: 
        counts[col] = 0
    for row in rows:
        for col in cols: 
            counts[col] = max(counts[col], vislen(row[col]))
    for col, count in counts.items():
        if count == 0:
            cols.remove(col)
    for row in rows:
        for col in cols:
            print visljust(row[col], counts[col]),
        print ""
    return 0

def get_git_folder():
    path = os.path.abspath(".")
    while path != "/" and ".git" not in os.listdir(path):
        path = os.path.dirname(path)
    path = os.path.join(path, ".git")
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        relpath = re.match(r"gitdir:\s*(?P<path>.*)\s*", open(path).read()).group("path")
        return os.path.normpath(os.path.join(path, "..", relpath))
    else:
        return None        

def colored(value, color):
    if color:
        return color + str(value) + BC.ENDC
    return str(value)
def colored_l(values, colors):
    return tuple(colored(value, color) for value, color in zip(values, colors))

def git_diff_count(fromRef, toRef):
    return int(bash_output("git rev-list %s..%s | wc -l" % (fromRef, toRef)).strip())

def git_merge_base(refname, alt=None):
    if not alt:
        alt = refname
    sha = bash_output("git merge-base '%s' '%s'" % (refname, alt))
    if sha and len(sha.strip()) == 40:
        return sha.strip()

def bash_output(command, raiseError=False):
    try:
        return subprocess.check_output(command, shell=True)
    except:
        if raiseError:
            raise

def visljust(string, width):
    len = vislen(string)
    return string + "".ljust(width-len)

def vislen(string):
    return len(re.sub("\x1b\[(\d+;)?\d+m","",string))

def test(args):
    foo = BC.GREEN+"foo"+BC.ENDC
    foolen=vislen(foo)
    if not foolen==3: raise AssertionError("vislen("+repr(foo)+") should be 3 - was "+str(foolen))
    print "All tests passed"

if __name__ == "__main__":
    sys.exit(main())
