#!/usr/bin/env python

from configparser import ConfigParser


class Config(ConfigParser):

    def __init__(self):
        super(Config, self).__init__()


