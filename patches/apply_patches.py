#!/usr/bin/env python3

import subprocess
import os
import re
from typing import List

PATCHES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patches.vcsdiff')
SPLITTER_RE = re.compile(r'=== (.*)\(git\) ===')


def apply_patch(patch_path: str, patch_lines: List[str]):
    print(f'Figuring out whether the patch should be applied in {patch_path}')
    if not os.path.exists(patch_path):
        print(f'{patch_path} does not exist, skipping patch')
        return

    print(f'Saving diff file in {patch_path}')
    with open(os.path.join(patch_path, 'ros-noetic-jammy.patch'), 'w') as f:
        f.writelines(patch_lines)

    print(f"Applying patch in {patch_path}")
    subprocess.call(['git', 'apply', 'ros-noetic-jammy.patch'], cwd=patch_path)


if __name__ == '__main__':
    contents = open(PATCHES_FILE, 'r').readlines()
    patch_start_line = 0
    while(patch_start_line < len(contents)):
        line = contents[patch_start_line]
        if matches := SPLITTER_RE.match(line):
            print(f"match on line {patch_start_line}: {matches.group(1)}")
            patch_path = matches.group(1).strip()
            patch_end_line = patch_start_line + 1
            while(patch_end_line < len(contents)):
                line = contents[patch_end_line]
                if SPLITTER_RE.match(line) or patch_end_line == len(contents) - 1:
                    patch_lines = contents[patch_start_line + 1 : patch_end_line]
                    apply_patch(patch_path, patch_lines)
                    break

                patch_end_line += 1
            patch_start_line = patch_end_line
        else:
            patch_start_line += 1
