#!/usr/bin/env python3

import argparse
import os
import sys

DME_SECTIONS = {
        'Master Boot Sector':   [0x00000, 0x03FFF],
        'Unknown 1':            [0x04000, 0x05FFF],
        'Unknown 2':            [0x06000, 0x07FFF],
        'Parameter Space 1':    [0x08000, 0x0BFFF],
        'Blank Space 1':        [0x0C000, 0x0FFFF],
        'Program Space 4':      [0x10000, 0x1FFFF],
        'Program Space 5':      [0x20000, 0x2FFFF],
        'Program Space 6':      [0x30000, 0x3FFFF],
        'Slave Boot Sector':    [0x40000, 0x43FFF],
        'Unknown 3':            [0x44000, 0x45FFF],
        'Unknown 4':            [0x46000, 0x47FFF],
        'Parameter Space 2':    [0x48000, 0x4BFFF],
        'Blank Space 2':        [0x4C000, 0x4FFFF],
        'Program Space 1':      [0x50000, 0x5FFFF],
        'Program Space 2':      [0x60000, 0x6FFFF],
        'Program Space 3':      [0x70000, 0x7FFFF],
}

def main():
    def title_to_slug(title):
        return title.replace(' ', '-').lower()

    parser = argparse.ArgumentParser()
    for section in DME_SECTIONS:
        parser.add_argument('--' + title_to_slug(section),
                            action='store_true', help='Dump ' + section)
    parser.add_argument('FULL_DME_FILE', help='the file to read')
    args = parser.parse_args()

    dme_data = open(args.FULL_DME_FILE, 'rb').read()

    for section in DME_SECTIONS:
        if getattr(args, title_to_slug(section).replace('-', '_')):
            bounds = DME_SECTIONS[section]
            os.write(1, dme_data[bounds[0]:bounds[1]+1])

    return 0

if __name__ == '__main__':
    sys.exit(main())
