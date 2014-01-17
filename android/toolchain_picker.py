#! /usr/bin/env python

import collections
import os
import subprocess
import sys

TOOLCHAINS_DIR = os.path.expanduser("~/apportable")
TOOLCHAIN_PATH = os.path.join(TOOLCHAINS_DIR, "apportable_sdk/toolchain")
TOOLCHAIN_PREFIX = "toolchain_"

def toolchain_options():
    options = {}
    for name in os.listdir(TOOLCHAINS_DIR):
        if name.startswith(TOOLCHAIN_PREFIX):
            options[name] = os.path.join(TOOLCHAINS_DIR, name)
    return options

def current_toolchain():
    if os.path.exists(TOOLCHAIN_PATH):
        return os.path.basename(subprocess.check_output(['readlink', '-n', TOOLCHAIN_PATH]))
    return None

def set_toolchain(path):
    os.remove(TOOLCHAIN_PATH)
    subprocess.check_call(['ln', '-sv', path, TOOLCHAIN_PATH])

def main():
    print "Current Toolchain: %s" % current_toolchain()
    i = 0
    options_dict = toolchain_options()
    options_list = sorted(options_dict.items())
    for name, path in options_list:
        i += 1
        print "%d: %s" % (i, name)
    choice = raw_input("Pick a toolchain: ").strip()
    
    if choice in options_dict:
        set_toolchain(options_dict[choice])
        return 0
    try:
        set_toolchain(options_list[int(choice)-1][1])
        return 0
    except:
        pass
    if TOOLCHAIN_PREFIX+choice in options_dict:
        set_toolchain(options_dict[TOOLCHAIN_PREFIX+choice])
        return 0
    print "Unrecognized choice: '%s'" % choice
    return 1

if __name__ == "__main__":
    sys.exit(main())
