import argparse
import io
import os
import sys
import tkinter as tk
from os import listdir, sep
from os.path import abspath, basename, isdir
from typing import IO


def tree(path: os.PathLike, indent: int, prefix: str, files: bool, last: bool, root: bool, out: IO) -> None:
    path = abspath(path)
    if root:
        print(basename(path) + sep if isdir(path) else basename(path), file=out)
    else:
        prefix_add: str = "└── " if last else "├── "
        print(
            prefix[:-(indent + 1)] + prefix_add + basename(path)
            + sep if isdir(path) else prefix + prefix_add + basename(path),
            file=out
        )
    prefix = prefix[:-1]

    whitespace = " " * indent
    ls = listdir(path)
    for i, item in enumerate(ls):
        check_dir = path + sep + item
        is_last = i == len(ls) - 1
        if isdir(check_dir):
            tree(
                path=check_dir,
                indent=indent,
                prefix=prefix + (" " + whitespace * 2 if is_last else f"{whitespace}│{whitespace}"),
                files=files,
                last=is_last,
                root=False,
                out=out
            )
        elif files:
            print(prefix + (f"{whitespace}└── " if is_last else f"{whitespace}├── ") + item, file=out)


def main():
    args = argparse.ArgumentParser()
    args.add_argument("-d", nargs="?", default=".", help="directory to print tree of")
    args.add_argument("-f", action="store_true", default=False, help="print files")
    args.add_argument("-i", default=2, type=int, help="indentation")
    args.add_argument("-c", action="store_true", default=False, help="copy to clipboard")
    args = args.parse_args()

    if args.c:
        out = io.StringIO()
    else:
        out = sys.stdout
    tree(args.d, args.i, "", args.f, False, True, out)

    if args.c:
        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        for l in out.getvalue().splitlines():
            r.clipboard_append("\n" + l.strip())
        r.update()  # now it stays on the clipboard after the window is closed
        r.destroy()
        out.close()
