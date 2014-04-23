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
            toolchain = os.path.join(TOOLCHAINS_DIR, name)
            xcode_select = os.path.join(toolchain, 'xcode-select.path')
            xcode = None
            if os.path.isfile(xcode_select):
                with open(xcode_select) as f:
                    xcode = f.read().strip()
            if xcode and not os.path.isdir(xcode):
                print "===WARNING=== Could not find Xcode at: "+xcode
            options[name] = {'path':toolchain, 'xcode':xcode}
    return options

def current_toolchain():
    if os.path.exists(TOOLCHAIN_PATH):
        return os.path.basename(subprocess.check_output(['readlink', '-n', TOOLCHAIN_PATH]))
    return None

def set_toolchain(toolchain):
    path = toolchain['path']
    os.remove(TOOLCHAIN_PATH)
    subprocess.check_call(['ln', '-sv', path, TOOLCHAIN_PATH])
    if toolchain['xcode']:
        subprocess.check_call(['sudo', 'xcode-select', '--switch', toolchain['xcode']])
        subprocess.check_call(['xcode-select', '--print-path'])

def main():
    print "Current Toolchain: %s" % current_toolchain()
    i = 0
    options_dict = toolchain_options()
    options_list = sorted(options_dict.items())
    for name, toolchain in options_list:
        path = toolchain['path']
        xcode = ""
        if toolchain['xcode']:
            xcode = " (%s)" % toolchain['xcode'].replace("/Applications/","").replace("/Contents/Developer","")
        i += 1
        print "%d: %s%s" % (i, name, xcode)
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
