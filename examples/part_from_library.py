#!/usr/bin/python
# coding: utf-8

r"""Example of creating a Part object from a parts library"""

import logging

import ccad.model as cm
import ccad.display as cd

url = "https://raw.githubusercontent.com/guillaume-florent/ball-bearings-library/master"
p = cm.Part.from_library(url=url,
                         name="608ZZ")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')
    v1 = cd.view()
    v1.display(p.geometry)
    cd.start()
