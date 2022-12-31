import argparse
import fnmatch
import io
import os
import sys
import tkinter as tk
from os import listdir, sep
from os.path import abspath, basename, isdir
from typing import IO, List, Optional


def filter_paths(paths: list, remove_files: bool, ignore_by_glob: Optional[List[str]]) -> list:
    if not ignore_by_glob and not remove_files:
        return paths

    filtered_paths = []
    for path in paths:
        if remove_files and os.path.isfile(path):
            continue
        if ignore_by_glob and any(fnmatch.fnmatch(path, glob) for glob in ignore_by_glob):
            continue
        filtered_paths.append(path)
    return filtered_paths


def tree(path: os.PathLike, prefix: str, files: bool, out: IO, ignore_globs: Optional[List[str]], depth: int) -> None:
    path = abspath(path)
    if os.path.isfile(path) and not files:
        return

    print(prefix + basename(path) + sep if isdir(path) else prefix + basename(path), file=out)

    if isdir(path):
        ls = filter_paths(listdir(path), not files, ignore_globs)
        # We are a directory, so lets remove our own prefix and replace it with whitespace
        prefix = prefix.replace("├── ", "│   ", 1).replace("└── ", "    ", 1)
        walk_tree(path, prefix, files, ls, out, ignore_globs, depth)


def walk_tree(path: str, prefix: str, files: bool, ls: list, out: IO, ignore_globs: Optional[List[str]],
              depth: int) -> None:
    if depth == 0:
        return
    for i, item in enumerate(ls):
        is_last = i == len(ls) - 1
        next_prefix = prefix + ("└── " if is_last else "├── ")

        tree(os.path.join(path, item), next_prefix, files, out, ignore_globs, depth - 1)


def root(path: os.PathLike, files: bool, out: IO, ignore_globs: Optional[List[str]], depth: int) -> None:
    path = abspath(path)
    print(basename(path) + sep if isdir(path) else basename(path), file=out)
    ls = filter_paths(listdir(path), not files, ignore_globs)
    walk_tree(path, "  ", files, ls, out, ignore_globs, depth)


def main():
    args = argparse.ArgumentParser()
    args.add_argument("-p", "--path", nargs="?", default=".", help="Path to start from")
    args.add_argument("-f", "--files", action="store_true", default=False, help="print files")
    args.add_argument("-c", "--clip", action="store_true", default=False, help="copy to clipboard")
    args.add_argument("-i", "--ignore", nargs="*", default=None, help="ignore files matching glob")
    args.add_argument("-d", "--depth", type=int, default=-1, help="depth to traverse, negative for infinite")
    args = args.parse_args()

    if args.clip:
        out = io.StringIO()
    else:
        out = sys.stdout
    root(args.path, args.files, out, args.ignore, args.depth)

    if args.clip:
        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        for l in out.getvalue().splitlines():
            r.clipboard_append("\n" + l.strip())
        r.update()  # now it stays on the clipboard after the window is closed
        r.destroy()
        out.close()
