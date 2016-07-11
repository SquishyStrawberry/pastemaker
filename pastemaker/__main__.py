#!/usr/bin/env python3
import sys

from getopt import gnu_getopt

import yaml

from .pastemaker import create_paste


def main():
    if len(sys.argv) < 2:
        print("USAGE: pastemaker PASTESERVICE FILENAME [--OPTION VALUE]")
        sys.exit(1)
    with open("pasteservices.yaml") as pasteservices_fobj:
        paste_services = yaml.safe_load(pasteservices_fobj)
    needed_flags = (paste_services[sys.argv[1]]["required_flags"] +
                    paste_services[sys.argv[1]]["optional_flags"])
    flags = gnu_getopt(sys.argv[1:], "", [i + "=" for i in needed_flags])[0]
    print(create_paste(paste_services,
                       sys.argv[1],
                       sys.argv[2],
                       dict((k[2:], v) for k, v in flags)))

if __name__ == "__main__":
    main()
