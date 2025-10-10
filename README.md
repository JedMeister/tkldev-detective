TKLDev-Detective
================

tkldev-detective is a simple framework for linting TurnKey GNU/Linux appliance
code. It leverages existing linting tools, as well as supporting custom
handmade lints and provides a unified output format/interface for utilizing
these tools.

Dependencies
------------

Mandatory Dependencies:

- `apt-file`        - for figuring out what packages provide certain files
                      (debian package)

Highly Recommended (but optional) Dependencies:

- `shellcheck`      - required for bash lints (debian package)
- `ruff`            - required for python lints (or `pylint` below) (pip/pipx
                      package or pre-built binary from upstream)
- `pylint`          - alternate requirement for python lints (debian package)
- `mypy`            - required for type checking (debian package)

Optional Dependencies:

- `python3-yaml`    - enables yaml lint (debian package)

Installation
------------

**Using apt** - best for direct usage

1. Install `tkldev-detective` from TurnKey apt repo (will also install
apt-file)
```
apt update
apt install --yes tkldev-detective
```

2. Install dependencies (installs `ruff` globally using `pipx`)
```
apt install --yes shellcheck mypy pipx python3-yaml
mkdir -p /usr/local/{bin,src}
PIPX_HOME=/usr/local/src PIPX_BIN_DIR=/usr/local/bin pipx install ruff
```

---

**From source** - best for development of `tkldev-detective` itself

1. Clone this repo somewhere, `/turnkey/public` is recommended:
```bash
mkdir -p /turnkey/public
cd /turnkey/public
git clone git@github.com:turnkeylinux/tkldev-detective
```

2. Add ``tkldev-detective`` to your path:
```bash
ln -s /turnkey/public/tkldev-detective/tkldev-detective /usr/local/bin/tkldev-detective
```

3. Install dependencies (installs `ruff` globally using `pipx`)
```
apt update
apt install --yes apt-file shellcheck mypy pipx python3-yaml
mkdir -p /usr/local/{bin,src}
PIPX_HOME=/usr/local/src PIPX_BIN_DIR=/usr/local/bin pipx install ruff
```

Usage
-----

Run:
`tkldev-detective lint <appliance>` where `<appliance>` can be:

- the name of an appliance
- the path to an appliance
- the path to a specific file in an appliance

Note the given appliance's build code must already be locally available.

E.g.
```bash
cd /turnkey/fab/products
tkldev-detective lint zoneminder
```

Color support
-------------

tkldev-detective supports color highlighting and will attempt to detect whether
the stdout supports color (i.e. check for a terminal). This behavior can be
changed with the `--color=always|never|auto` option where:

- `auto`        provides default behavior
- `always`      always enables color
- `never`       disables color entirely

For more information on how it works and how to develop more functionality, see
[overview], [custom modules] and [tools and tricks].

Licence
-------

This file is part of tkldev-detective.

tkldev-detective is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

tkldev-detective is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
tkldev-detective. If not, see <https://www.gnu.org/licenses/>.

[overview]: ./docs/overview.rst
[custom modules]: ./docs/custom_modules.rst
[tools and tricks]: ./docs/tools_and_tricks.rst
