# Copyright (c) Turnkey GNU/Linux <admin@turnkeylinux.org>
#
# this file is part of tkldev-detective.
#
# tkldev-detective is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# tkldev-detective is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# tkldev-detective. If not, see <https://www.gnu.org/licenses/>.

""" handles loading / managing tkldev-detective-modules """

import importlib.machinery
import importlib.util
from os.path import join, dirname, abspath, splitext, isfile, exists
from os import listdir
import sys

from . import colors as co
from .error import TKLDevDetectiveError

# priortise local tkldet_modules path, fallback to OS path
MOD_PATH = [ dirname(dirname(abspath(__file__))), '/usr/share/tkldev-detective']


def _load_all_modules_from_dir(root: str):
    print(
        co.BRIGHT_BLACK + co.BOLD + "load all modules from", root + co.RESET, file=sys.stderr
    )
    root = abspath(root)
    for filename in listdir(root):
        path = join(root, filename)
        mod_name, ext = splitext(filename)
        if isfile(path) and ext == ".py":
            spec = importlib.util.spec_from_file_location(mod_name, path)
            assert spec is not None
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)

            print(co.BRIGHT_BLACK + co.BOLD + "loaded", spec.name + co.RESET, file=sys.stderr)


def load_modules():
    """load all tkldev-detective modules"""
    for _path in (join(x, "tkldet_modules") for x in MOD_PATH):
        if exists(_path):
            _load_all_modules_from_dir(_path)
            return
    raise TKLDevDetectiveError(f"Mod path 'tkldet_modules' not found - tried {MOD_PATH}")
