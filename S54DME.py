#!/usr/bin/env python3

import argparse
import sys

import dme_tables

class S54DME:
    def __init__(self, path):
        self.path = path
        with open(self.path, 'rb') as f:
            self.data = f.read()

    def _extract_data(self, offset, length):
        return self.data[offset:offset + length]

    def version(self):
        return self._extract_data(0x7FB8, 16).decode('ascii')

    def hw_version(self):
        return dme_tables.VERSION_TO_HW_VERSION[self.version()]

    def shift_lights_status(self):
        offset = dme_tables.HW_VERSION_SHIFT_LIGHTS_OFFSET[self.hw_version()]
        status = self._extract_data(offset, 1)[0]
        return dme_tables.SHIFT_LIGHTS_STATUS_STR[status]

    def sport_mode_status(self):
        offset = dme_tables.HW_VERSION_SPORT_MODE_OFFSET[self.hw_version()]
        status = self._extract_data(offset, 1)[0]
        return dme_tables.SPORT_MODE_STATUS_STR[status]

    def vmax_status(self):
        offset = dme_tables.HW_VERSION_VMAX_OFFSET[self.hw_version()]
        raw_data = self._extract_data(offset, 32)
        data = {}
        for i in range(8):
            gear_str = 'neutral' if i == 0 else 'reverse' if i == 7 else str(i)
            raw_data = self._extract_data(offset + 16 + 2 * i, 2)
            data[gear_str] = round((raw_data[0] * 256 + raw_data[1]) / 16, 2)
        return data

    def gear_ratios_status(self):
        offset = dme_tables.HW_VERSION_GEAR_RATIOS_OFFSET[self.hw_version()]
        raw_data = self._extract_data(offset, 8)
        data = {}
        for i in range(8):
            gear_str = 'final drive' if i == 0 else 'reverse' if i == 7 else str(i)
            data[gear_str] = round(raw_data[i] / 60, 2)
        return data

    def rev_limit_status(self):
        offset = dme_tables.HW_VERSION_REV_LIMIT_OFFSET[self.hw_version()]
        raw_data = self._extract_data(offset, 32)
        data = {}
        for i in range(8):
            gear_str = 'neutral' if i == 0 else 'reverse' if i == 7 else str(i)
            raw_data = self._extract_data(offset + 16 + 2 * i, 2)
            data[gear_str] = round(raw_data[0] * 256 + raw_data[1], 2)
        return data

    def dyno_rev_limit_status(self):
        offset = dme_tables.HW_VERSION_DYNO_REV_LIMIT_OFFSET[self.hw_version()]
        raw_data = self._extract_data(offset, 2)
        return raw_data[0] * 256 + raw_data[1]

    def oil_warmup_levels_status(self):
        offset = dme_tables.HW_VERSION_OIL_WARMUP_LEVELS_OFFSET[self.hw_version()]
        raw_data = self._extract_data(offset, 7)
        data = []
        for i in range(7):
            data.append(raw_data[i] - 48)
        return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('DME_FILE', help='the file to read')
    args = parser.parse_args()

    dme = S54DME(args.DME_FILE)
    print('Version: %s' % dme.version())
    print('HW version: %s' % dme.hw_version())
    print('Shift lights: %s' % dme.shift_lights_status())
    print('Sport mode: %s' % dme.sport_mode_status())
    print('VMax: %s' % dme.vmax_status())
    print('Gear ratios: %s' % dme.gear_ratios_status())
    print('Rev limit: %s' % dme.rev_limit_status())
    print('Dyno rev limit: %s' % dme.dyno_rev_limit_status())
    print('Oil warmup levels: %s' % dme.oil_warmup_levels_status())

    return 0

if __name__ == '__main__':
    sys.exit(main())
