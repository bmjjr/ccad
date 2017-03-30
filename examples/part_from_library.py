#!/usr/bin/python
# coding: utf-8

r"""Example of creating a Part object from a parts library"""

import logging

import ccad.model as cm
import ccad.display as cd

logger = logging.getLogger(__name__)

url = "https://raw.githubusercontent.com/guillaume-florent/standard-cad-parts/master/parts/rolling_bearings/scripts/"
# p, anchors = cm.Part.from_library(url=url, name="608ZZ")
p, anchors = cm.Part.from_library(url=url, name="F63800ZZ")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')
    v1 = cd.view()
    multiplier = 10.

    v1.display(p.geometry, color=(0.1, 0.1, 1.0), transparency=0.3)

    for anchor in anchors:
        logger.debug("Showing an anchor: %s;%s" % (str(anchor[0]), str(anchor[1])))
        v1.display_vector(origin=anchor[0], direction=(anchor[1][0] * multiplier,
                                                       anchor[1][1] * multiplier,
                                                       anchor[1][2] * multiplier))

    cd.start()
