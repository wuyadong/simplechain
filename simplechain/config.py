#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Config module for simpleChain, it's only support YAML file. """

from __future__ import absolute_import
from typing import Optional
from path import Path
from yaml import load


class Config(object):
    """
    Configuration for simpleChain.
    """

    # singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_file: Optional[str] = None):
        if not config_file:
            self.config_file = "~/.simplechain.yml"
        else:
            self.config_file = config_file

        self.option = dict()
        if not Path(self.config_file).isfile():
            print("{0}  is not file".format(self.config_file))
            return

        with open(self.config_file) as f:
            c = load(f)
            self.option.update(c)
