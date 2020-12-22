#!python
# coding=utf-8
import logging


def setup_logging():
    logging.basicConfig(format="%(asctime)s %(filename)s:%(lineno)d\t%(levelname)-8s - %(message)s")
    L = logging.getLogger()
    L.setLevel(logging.INFO)
    return L


logger = setup_logging()
