LK Helper
=========

Build LK and flash it to devices.

Dependenceis
------------
 + Python 2.7
 + [Fabric](http://www.fabfile.org/installing.html) for Python

Usage
-----
 + Open `fabfile.py` and fill in `LK_PROJECT_BASE`, `SOD_PROJECT_BASE` and
   `OPEN_OCD_BASE` to point to the root of LK (optional), SOD (optional) and
   OpenOCD (required) respectively.
 + Create a symlink to fabfile.py in a directory that is an ancestor of both
   your SOD directory and your lk directory. For example if LK is located at
   `~/code/lk` and SOD is located at `~/code/sod`, you should invoke
   `ln -s ~/code/lkhelper/fabfile.py ~/code/fabfile.py`
 + Run `fab -l` to get a list of commands in any subdirectory.