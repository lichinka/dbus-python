#!/usr/bin/env python

#
# This software is distributed under the GNU General Public License.
# See the file COPYING for details.
#

""" dbus-python setup script """

import os
import sys

from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext

from configure import configure


class BuildExt (build_ext):
    def initialize_options (self):
        """
        Configure the compilation before starting.-
        """
        build_ext.initialize_options (self)
        all_found = configure (['-i', '.',
                                '-i', '/usr/lib/dbus-1.0/include',
                                '-i', '/usr/include/dbus-1.0/dbus',
                                '-i', '/usr/lib/glib-2.0/include',
                                '-i', '/usr/include/glib-2.0'])
        if not all_found:
            sys.stderr.write ('*** ERROR not all files, required for compilation, have been found.\n')
            sys.stderr.write ('*** ERROR Please make sure you have installed all the requirements.\n')
            sys.stderr.write ('*** ERROR Also check that the path list in "setup.py" is correct.\n')
            sys.exit (1)

    def finalize_options (self):
        build_ext.finalize_options (self)
        #
        # split libraries, since Python does not expand them by default
        #
        if self.libraries:
            self.libraries = self.libraries[0].split (os.pathsep)


DBUS_SOURCES = ['_dbus_bindings/abstract.c',
                '_dbus_bindings/message-append.c',
                '_dbus_bindings/exceptions.c',
                '_dbus_bindings/float.c',
                '_dbus_bindings/int.c',
                '_dbus_bindings/module.c',
                '_dbus_bindings/mainloop.c',
                '_dbus_bindings/conn-methods.c',
                '_dbus_bindings/containers.c',
                '_dbus_bindings/validation.c',
                '_dbus_bindings/pending-call.c',
                '_dbus_bindings/debug.c',
                '_dbus_bindings/conn.c',
                '_dbus_bindings/unixfd.c',
                '_dbus_bindings/message.c',
                '_dbus_bindings/bytes.c',
                '_dbus_bindings/libdbusconn.c',
                '_dbus_bindings/bus.c',
                '_dbus_bindings/generic.c',
                '_dbus_bindings/message-get-args.c',
                '_dbus_bindings/signature.c',
                '_dbus_bindings/server.c',
                '_dbus_bindings/string.c']
DBUS_GLIB_SOURCES = ['_dbus_glib_bindings/module.c']

setup (
    name	 = 'dbus-python',
    version	 = '1.1.1',
    description	 = 'Python bindings for D-Bus',
    author	 = 'Olivier Andrieu <oliv__a@users.sourceforge.net>, \
                    Philip Blundell <pb@nexus.co.uk>, \
                    Anders Carlsson <andersca@gnome.org>, \
                    Kristian Hogsberg  <krh@redhat.com>, \
                    Alex Larsson <alexl@redhat.com>, \
                    Robert McQueen <robot101@debian.org>, \
                    Simon McVittie <simon.mcvittie@collabora.co.uk>, \
                    Michael Meeks <michael@ximian.com>, \
                    Osvaldo Santana Neto <osvaldo.santana@indt.org.br>, \
                    Seth Nickell <seth@gnome.org>, \
                    John (J5) Palmieri <johnp@redhat.com>, \
                    Havoc Pennington <hp@redhat.com>, \
                    Harri Porten <porten@kde.org>, \
                    Matthew Rickard <mjricka@epoch.ncsc.mil>, \
                    Zack Rusin <zack@kde.org>, \
                    Joe Shaw <joe@assbarn.com>, \
                    Colin Walters <walters@verbum.org>, \
                    David Zeuthen <david@fubar.dk>',
    author_email = 'robot101@debian.org',
    packages	 = ['dbus'],
    ext_modules  = [Extension ('_dbus_bindings', sources=DBUS_SOURCES),
                    Extension ('_dbus_glib_bindings', sources=DBUS_GLIB_SOURCES),],
    cmdclass     = {'build_ext' : BuildExt})
