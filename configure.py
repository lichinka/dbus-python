#!/usr/bin/env python

#
# This software is distributed under the GNU General Public License.
# See the file COPYING for details.
#

""" dbus-python configure script """

from __future__ import print_function

from argparse import ArgumentParser

try:
    from ConfigParser import RawConfigParser
except ImportError:
    from configparser import RawConfigParser

import os
import sys


INCLUDE_DIRS = ['/usr/include/dbus-1.0',
                '/usr/lib/dbus-1.0/include',
                '/usr/local/include/dbus-1.0',
                os.path.join (os.path.dirname (os.path.realpath (__file__)),
                              'include')]
LIBRARY_DIRS = ['/usr/lib', '/usr/local/lib']

if os.uname()[-1] == 'x86_64':
    LIBRARY_DIRS = LIBRARY_DIRS + list (map (lambda s: s + '64', LIBRARY_DIRS))

DBUS_LIBS = ['dbus-1',
             'dbus-glib-1']
HEADERS = ['dbus-python.h',
           'glib-object.h',
           'glibconfig.h']



def static_library (lib_dir, libname):
    return os.path.join(lib_dir, 'lib' + libname + '.a')

def shared_library (lib_dir, libname):
    return os.path.join(lib_dir, 'lib' + libname + '.so')

def find_library (library, lib_dirs):
    for lib_dir in lib_dirs:
        if os.path.exists(static_library(lib_dir, library)) or \
           os.path.exists(shared_library(lib_dir, library)):
            return True
    return False

def find_file (one_file, dirs):
    for one_dir in dirs:
        if os.path.exists (os.path.join (one_dir, one_file)):
            return True
    return False


def find_files (files, dirs, search_libraries=False):
    all_found = True
    flist = []
    for f in files:
        print ('Checking for %s ...' % f, end=' ')
        if (search_libraries and find_library (f, dirs)) or find_file (f, dirs):
            print ('ok')
            flist.append (f)
        else:
            all_found = False
            print ('FAIL')
    if all_found:
        return flist
    else:
        return None


def print_tab_list (plist):
    for item in plist:
        print('\t', item)


def configure (args=None):
    usage  = 'usage: %prog [options]'
    desc   = 'Configure script to setup local environment for dbus-python'
    parser = ArgumentParser (usage=usage, description=desc)

    parser.add_argument ('-c', '--config_file', action='store',
                         metavar='file', default='setup.cfg',
                         help='Output setup configuration file (defaults to setup.cfg)')

    parser.add_argument ('-i', '--include_dir', action='append',
                         metavar='path',
                         help='Path to header files')

    parser.add_argument ('-l', '--library_dir', action='append',
                         metavar='path',
                         help='Path to library files')

    parser.add_argument ('-p', '--prefix', action='store',
                         metavar='path',
                         help='Install prefix path')

    options = parser.parse_args (args)

    include_dirs = INCLUDE_DIRS
    library_dirs = LIBRARY_DIRS

    config = RawConfigParser ( )

    if options.include_dir:
        include_dirs.extend (options.include_dir)

    if options.library_dir:
        library_dirs.extend (options.library_dir)

    if options.prefix:
        config.add_section ('install')
        config.set ('install', 'prefix', options.prefix)
        print ('Using the following install prefix:', options.prefix)

        include_dirs.append (os.path.join (options.prefix, 'include'))
        library_dirs.append (os.path.join (options.prefix, 'lib'))

    config.add_section ('build_ext')
    config.set ('build_ext', 'library_dirs', os.pathsep.join (library_dirs))

    print('Looking for header files in the following include paths:')
    print_tab_list (include_dirs)

    headers = find_files (HEADERS,
                          include_dirs)
    if headers:
        config.set ('build_ext', 'include_dirs', os.pathsep.join (include_dirs))

    print('Looking for libraries in the following library paths:')
    print_tab_list (library_dirs)

    libraries = find_files (DBUS_LIBS,
                            library_dirs,
                            True)
    if libraries:
        config.set('build_ext', 'libraries', os.pathsep.join(libraries))

    if headers and libraries:
        with open (options.config_file, 'w+') as config_file:
            config.write (config_file)
            print ('Configuration saved to:', options.config_file)
        return True
    else:
        print ("WARNING: configuration not created because of missing files")
        return False


if __name__ == '__main__':
    configure (sys.argv)

