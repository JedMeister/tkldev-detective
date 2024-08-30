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

"""
Encapsulates "Classifier"s & the "Item"s they operate on

code here provides ability to "classify" different files
"""

from dataclasses import dataclass
from typing import Generator, Iterable, Type, cast
from os.path import dirname


@dataclass(frozen=True)
class Item:
    """Some "thing" which can be classified

    tags are used to classify items,
    value is dependant on type of "thing"
    """

    __slots__ = ["value", "_tags"]

    value: str
    """context dependant value, either the thing being classified itself or
    information on how to acccess it (such as a path)"""

    _tags: dict[str, set[str]]
    """maps classifiers to tags, so if necessary it can be determined
    exactly how an item got classsified in a certain way """

    @property
    def tags(self) -> Generator[str, None, None]:
        """ yields all tags, may contain duplicates """
        for tags in self._tags.values():
            yield from tags

    def add_tags(self, classifier: "Classifier", tags: Iterable[str]):
        """convenience method for adding tags to an item"""
        name = classifier.__class__.__name__
        if name not in self._tags:
            self._tags[name] = set()
        self._tags[name].update(tags)

    def pretty_print(self):
        """show item value as well as tags"""
        print(f"{self.value}")
        for src in self._tags:
            print("\t", src, self._tags[src])


@dataclass(frozen=True)
class FileItem(Item):
    """Specifically files which can be classified

    value is the raw path found by the locator
    """

    __slots__ = ["relpath", "abspath"]

    relpath: str
    """path relative to the appliance root, use this when inspecting the
    path itself"""

    abspath: str
    """absolute path to file, use this when inspecting the file the path points
    to"""


@dataclass(frozen=True)
class PackageItem(Item):
    """Specifically packages installed via plan which can be classied

    value is the package name
    """

    __slots__ = ["plan_stack"]

    plan_stack: list[str]
    """a list of paths, in order from the "base" plan (appliance-specific) all
    the way to the exact plan that included this package. Note this will only
    contain 1 value if a package was included in the appliance specific plan"""


class Classifier:
    """Classifier base class

    all registered classifiers are called with each item yielded by the locator.

    the tags determined by the classifiers determine which linters are run on
    which files.
    """

    WEIGHT: int = 100
    """weight is used to order classifiers, as tthey can read tags as well,
    classifier can leverage information provided (or omitted) by previous
    classifiers"""

    ItemType: Type[Item] = Item

    def do_classify(self, item: Item):
        """actually perform a classification so long as the concrete item type
        is compatible with this classifier"""
        if isinstance(item, self.ItemType):
            self.classify(item)

    def classify(self, item: Item):
        """abstract method to be implemented by subclass"""
        raise NotImplementedError()


class FileClassifier(Classifier):
    """Specialized classifer which operates on "FileItem"s"""

    ItemType: Type[Item] = FileItem


class PackageClassifier(Classifier):
    """Specialized classifier which operates on "PackageItem"s"""

    ItemType: Type[Item] = PackageItem


class ExactPathClassifier(FileClassifier):
    """Classifies an item which matches some exact path"""

    path: str
    "exact path to match"

    tags: list[str]
    "exact tags to add to matched item"

    def classify(self, item: Item):
        item = cast(FileItem, item)
        # item will definitely be subclass of
        # cls.ItemType, just need to convince the type checker

        if item.relpath == self.path:
            item.add_tags(self, self.tags[:])


class SubdirClassifier(FileClassifier):
    """Classifies an item which is inside a given subdirectory"""

    path: str
    "the parent directory"

    recursive: bool
    "whether to match a child of any depth or only files directly inside the given dir"

    tags: list[str]
    "exact tags to add to matched item"

    def classify(self, item: Item):
        item = cast(FileItem, item)
        # item will definitely be subclass of
        # cls.ItemType, just need to convince the type checker

        if self.recursive:
            if item.relpath.startswith(self.path):
                # XXX doesn't handle any `..` in path, hopefully doesn't matter
                item.add_tags(self, self.tags[:])
        else:
            if dirname(item.relpath) == self.path:
                item.add_tags(self, self.tags[:])


_CLASSIFIERS: list[Type[Classifier]] = []


def register_classifier(classifier: Type[Classifier]):
    """registers a classifier for use in tkldev-detective, must be called on all
    classifiers added"""
    _CLASSIFIERS.append(classifier)
    return classifier


def get_weighted_classifiers() -> list[Classifier]:
    """returns instances of registered classifiers in order of weight"""
    return sorted(
        map(lambda x: x(), _CLASSIFIERS), key=lambda x: (x.WEIGHT, x.__class__.__name__)
    )
