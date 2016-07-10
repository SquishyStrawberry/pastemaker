#!/usr/bin/env python3
import os
import sys

from getopt import gnu_getopt as getopt

import yaml

from .pastemaker import create_paste


def main():
    if len(sys.argv) < 2:
        print("USAGE: pastemaker PASTESERVICE FILENAME [--OPTION VALUE]")
        sys.exit(1)
    with open("pasteservices.yaml") as pasteservices_fobj:
        paste_services = yaml.safe_load(pasteservices_fobj)
    required_options = paste_services[sys.argv[1]]["required_options"]
    options = getopt(sys.argv[1:], "", [i + "=" for i in required_options])[0]
    print(create_paste(paste_services,
                       sys.argv[1],
                       sys.argv[2],
                       dict((k[2:], v) for k, v in options)))

if __name__ == "__main__":
    main()
