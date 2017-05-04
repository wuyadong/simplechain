#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from simplechain.config import Config
import os

_dir_path = os.path.dirname(os.path.realpath(__file__))


def test_init():
    with pytest.raises(FileNotFoundError):
        Config("no.yml")

    c = Config(_dir_path + "/simplechain.yml")
    print(c.option)
    assert c.option['peers'][0] == "192.168.0.233"
