#! /usr/bin/env python

import collections
import json
import os
import re
import subprocess
import sys

HELP_STRING = """
This tool manages your Apportable toolchain folders by symlinking to them.

* Toolchain folders are folders which start with 'toolchain_' in the '$DCF_ROOT/..' directory.
* Feel free to modify toolchain folders manually - the tool reads from the file system every time it runs.
* Toolchains are often linked to a version of xcode.
    Change the version by editing the pg_config.json file inside the toolchain directory.
* Select an option using its number, full directory name, or directory suffix.
"""

DCF_ROOT = os.path.abspath(os.path.expanduser(os.getenv('DCF_ROOT', '~/apportable/apportable_sdk')))
TOOLCHAIN_PATH = os.path.join(DCF_ROOT, "toolchain")
TOOLCHAINS_DIR = os.path.dirname(DCF_ROOT)
TOOLCHAIN_PREFIX = "toolchain_"
DEFAULT_CONFIG = {'XCODE_SELECT_PATH':None,'VALID_PGX_VERSIONS':None}

#print "TOOLCHAIN_PATH = " + TOOLCHAIN_PATH
#print "TOOLCHAINS_DIR = " + TOOLCHAINS_DIR

def toolchain_options():
    options = {}
    for name in os.listdir(TOOLCHAINS_DIR):
        if name.startswith(TOOLCHAIN_PREFIX):
            toolchain = os.path.join(TOOLCHAINS_DIR, name)
            cfg = load_config(name)
            xcode = cfg.get('XCODE_SELECT_PATH', None)
            pgxs = cfg.get('VALID_PGX_VERSIONS', None)
            if xcode and not os.path.isdir(xcode):
                print "===WARNING=== Could not find Xcode at: "+xcode
            options[name] = {'path':toolchain, 'xcode':xcode, 'pgxs':pgxs}
    return options

def current_toolchain():
    if os.path.islink(TOOLCHAIN_PATH):
        return os.path.basename(subprocess.check_output(['readlink', '-n', TOOLCHAIN_PATH]).strip())
    return None

def current_xcode_path():
    return subprocess.check_output(['xcode-select', '--print-path']).strip()

def save_config(toolchain_name, config_dict):
    toolchain = os.path.join(TOOLCHAINS_DIR, toolchain_name)
    pg_config = os.path.join(toolchain, 'pg_config.json')
    with open(pg_config, 'w') as f:
        json.dump(config_dict, f, sort_keys=True, indent=4)

def check_migrate_config(toolchain_name):
    toolchain = os.path.join(TOOLCHAINS_DIR, toolchain_name)
    xcode_select = os.path.join(toolchain, 'xcode-select.path')
    new_config = {}
    if os.path.isfile(xcode_select):
        with open(xcode_select) as f:
            xcode = f.read().strip()
            if xcode:
                new_config['XCODE_SELECT_PATH'] = xcode
        os.remove(xcode_select)
        # now that this file is deleted, we can call load_config without recursing infinitely
    config = dict(DEFAULT_CONFIG)
    config.update(load_config(toolchain_name, migrate=False))
    config.update(new_config)
    save_config(toolchain_name, config)
    return config

def load_config(toolchain_name, migrate=True):
    if migrate:
        return check_migrate_config(toolchain_name)
    toolchain = os.path.join(TOOLCHAINS_DIR, toolchain_name)
    pg_config = os.path.join(toolchain, 'pg_config.json')
    if os.path.isfile(pg_config):
        with open(pg_config, 'r') as f:
            try:
                return json.load(f)
            except:
                print "ERROR: Failed to read JSON in file: " + pg_config
                raise
    else:
        return {}

def save_xcode_path(toolchain_name, xcode_path):
    cfg = load_config(toolchain_name)
    cfg['XCODE_SELECT_PATH'] = xcode_path
    save_config(toolchain_name, cfg)

def set_toolchain(toolchain):
    path = toolchain['path']
    if os.path.exists(TOOLCHAIN_PATH):
        os.remove(TOOLCHAIN_PATH)
    print "Linking:"
    subprocess.check_call(['ln', '-sv', path, TOOLCHAIN_PATH])
    if toolchain['xcode'] and current_xcode_path() != toolchain['xcode']:
        print "** if prompted, enter your mac password **"
        subprocess.check_call(['sudo', 'xcode-select', '--switch', toolchain['xcode']])
    print "Xcode CLI path: "+current_xcode_path()

def setup_toolchain_management():
    if not os.path.exists(DCF_ROOT):
        print "ERROR: DCF_ROOT (%s) does not exist!" % DCF_ROOT
        return False
    if not os.path.exists(TOOLCHAIN_PATH):
        print "TOOLCHAIN_PATH (%s) does not exist.  OK." % TOOLCHAIN_PATH
        return True
    elif os.path.isfile(TOOLCHAIN_PATH):
        print "ERROR: TOOLCHAIN_PATH (%s) is a file!" % TOOLCHAIN_PATH
        return False
    new_name = TOOLCHAIN_PREFIX+"_original"
    toolchain_new = os.path.join(TOOLCHAINS_DIR, new_name)
    if os.path.exists(toolchain_new):
        print "ERROR: %s already exists!" % toolchain_new
        return False
    print "Moving %s to %s" % (TOOLCHAIN_PATH, toolchain_new)
    os.rename(TOOLCHAIN_PATH, toolchain_new)
    xcode_path = current_xcode_path()
    print "Setting Xcode path to %s" % xcode_path
    save_xcode_path(new_name, xcode_path)
    return True

def create_new_toolchain():
    try:
        suffix = raw_input("Pick a toolchain name (the part after '%s'): " % TOOLCHAIN_PREFIX).strip()
    except KeyboardInterrupt:
        print "\nCANCELLED"
        return None
    if not re.match(r"^\w+$", suffix):
        print "ERROR: name must be only alphanumeric characters (and _)"
        return None
    new_name = TOOLCHAIN_PREFIX+suffix
    toolchain_new = os.path.join(TOOLCHAINS_DIR, new_name)
    os.mkdir(toolchain_new)
    xcode_path = current_xcode_path()
    print "Setting Xcode path to %s" % xcode_path
    save_xcode_path(new_name, xcode_path)
    return toolchain_options()[new_name]


def main():
    if not os.path.islink(TOOLCHAIN_PATH) and os.path.exists(TOOLCHAIN_PATH):
        print "Attempting to configure toolchain management."
        if setup_toolchain_management():
            print "Initial configuration success!  Continuing.\n"
        else:
            return 1

    print "Current Toolchain: %s" % current_toolchain()
    i = 0
    options_dict = toolchain_options()
    options_list = sorted(options_dict.items())
    print "Actions:"
    print "  HELP: Show help about the tool"
    print "  NEW: Create a new empty toolchain folder"
    print "Toolchains:"
    for name, toolchain in options_list:
        path = toolchain['path']
        pgxs = ""
        if toolchain['pgxs']:
            pgxs = " (%s)" % ', '.join("pgx_"+str(pgx) for pgx in toolchain['pgxs'])
        xcode = ""
        if toolchain['xcode']:
            xcode = " (%s)" % toolchain['xcode'].replace("/Applications/","").replace("/Contents/Developer","")
        i += 1
        print "  %d: %s%s%s" % (i, name, pgxs, xcode)
    try:
        choice = raw_input("Pick an action or toolchain: ").strip()
    except KeyboardInterrupt:
        print "\nCANCELLED"
        return None

    if choice == 'NEW':
        new_toolchain = create_new_toolchain()
        if new_toolchain:
            set_toolchain(new_toolchain)
            return 0
        else:
            return 1
    if choice == 'HELP':
        print HELP_STRING
        return 0
    if choice in options_dict:
        set_toolchain(options_dict[choice])
        return 0
    try:
        set_toolchain(options_list[int(choice)-1][1])
        return 0
    except ValueError:
        pass
    if TOOLCHAIN_PREFIX+choice in options_dict:
        set_toolchain(options_dict[TOOLCHAIN_PREFIX+choice])
        return 0
    print "Unrecognized choice: '%s'" % choice
    print HELP_STRING
    return 1

if __name__ == "__main__":
    sys.exit(main())
