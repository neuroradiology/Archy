# version.py
# The Raskin Center for Humane Interfaces (RCHI) 2004

# This work is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike License. To view 
# a copy of this license, visit 
# http://creativecommons.org/licenses/by-nc-sa/2.0/ 

# or send a letter to :

# Creative Commons
# 559 Nathan Abbott Way
# Stanford, California 94305, 
# USA.
# --- --- ---

VERSION = "$Id: version.hpy,v 1.1 2005/03/24 22:52:46 varmaa Exp $"

# This module is used to determine and retrieve Archy's version information.  Currently, this version information consists of a version number (e.g., "1.0") and a build number.

# The build number is entirely independent of the version number, and is an ever-increasing integer that is currently calculated by walking through the entire directory tree from Archy's root directory and determining the last SVN revision number in which each file was changed.  Archy's "build number" is the highest highest such revision number.  Archy's "build date" is the date at which this revision was committed--it is *not* the date that the build was "compiled", and it does not reflect any local changes made to source files.

# To calculate the build number, however, the ".svn" directories containing file metadata must be available; this isn't the case with certain builds (such as the Windows Executable version of Archy), so the build information must be pre-calculated at runtime and placed in the file named by the BUILD_FILE variable below.

BUILD_FILE = "build.dat"

# This is the version number of Archy.

ARCHY_VERSION_STRING = '0.1.1'

# The following two variables are auto-generated by this module upon loading.

ARCHY_BUILD_NUMBER = None
ARCHY_BUILD_DATE = None

import time

import xml.sax

class SVNEntriesContentHander(xml.sax.handler.ContentHandler):
    def startDocument(self):
        self.latest_committed_rev = 0
        self.latest_committed_date = "the big bang"

    def startElement(self, name, attrs):
        if name == "entry":
            if attrs.has_key("committed-rev"):
                rev = int(attrs["committed-rev"])
                if rev > self.latest_committed_rev:
                    self.latest_committed_rev = rev
                    self.latest_committed_date = attrs["committed-date"]

class _SVNDirError(Exception):
    pass

class _SVNBuildWalker:
    def __init__(self):
        self.handler = SVNEntriesContentHander()
        xml.sax.make_parser()

    def _calc_svn_dir_build_info(self, dir_name):
        try:
            f = open("%s/.svn/entries" % dir_name, "r")
        except IOError:
            raise _SVNDirError()

        xml.sax.parse(f, self.handler)

        if self.handler.latest_committed_rev > self._latestbuild:
            self._latestbuild = self.handler.latest_committed_rev
            self._maxdate = self.handler.latest_committed_date

    def calculate_build_info(self):
        self._maxdate = 0
        self._latestbuild = 0
        self._dirs = ['.']

        while len(self._dirs) > 0:
            dir = self._dirs.pop()
            self._calc_svn_dir_build_info(dir)

    def get_build_number(self):
        return self._latestbuild

    def get_build_date(self):
        return self._maxdate

def write_build_file():
    f = open(BUILD_FILE, "w")
    f.write("%d,%s" % (ARCHY_BUILD_NUMBER, ARCHY_BUILD_DATE))
    f.close()

def get_build_number():
    return ARCHY_BUILD_NUMBER

def get_build_date():
    return ARCHY_BUILD_DATE

def get_version():
    return ARCHY_VERSION_STRING

def get_full_version():
    return "%s (build %d - %s)" % (get_version(), get_build_number(), get_build_date())

def _init_module():
    global ARCHY_BUILD_NUMBER
    global ARCHY_BUILD_DATE

    try:
        c = _SVNBuildWalker()
        c.calculate_build_info()
        ARCHY_BUILD_NUMBER = c.get_build_number()
        ARCHY_BUILD_DATE = c.get_build_date()
    except _SVNDirError:
        f = open(BUILD_FILE, "r")
        ARCHY_BUILD_NUMBER, ARCHY_BUILD_DATE = f.read().split(",")
        ARCHY_BUILD_NUMBER = int( ARCHY_BUILD_NUMBER )
        f.close()

_init_module()
