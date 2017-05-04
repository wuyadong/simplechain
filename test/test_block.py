#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from simplechain.block import *


def test_init():
    with pytest.raises(ValueError):
        invalid_block = Block(1, "0", "1", None, "1")
        assert not invalid_block.valid()

    block = Block(1, "1234", "test")
    assert block.pre_hash == "1234"
    assert block.index == 1
    assert block.data == "test"
    assert block.valid() is True

    block2 = Block(2, "12345", "test2", 100, "0ad2fc79d6d481dec2a31a59f8f4e5aba35c8f90619dd991e171f5d0e92c2e26")
    assert block2.index == 2
    assert block2.pre_hash == "12345"
    assert block2.data == "test2"
    assert block2.timestamp == 100
    assert block2.valid() is True


def test_eq():
    block2 = Block(2, "12345", "test2", 100, "0ad2fc79d6d481dec2a31a59f8f4e5aba35c8f90619dd991e171f5d0e92c2e26")
    block2_1 = Block(2, "12345", "test2", 100)
    block1 = Block(1, "12345", "test2")
    assert block2 == block2_1
    assert block2 != block1


def test_iter():
    b = Block(2, "12345", "test2", 100, "0ad2fc79d6d481dec2a31a59f8f4e5aba35c8f90619dd991e171f5d0e92c2e26")
    d = dict(b)
    print(d)
    assert d['version'] == b.version
    assert d['index'] == b.index
    assert d['pre_hash'] == b.pre_hash
    assert d['timestamp'] == b.timestamp
    assert d['data'] == b.data
    assert d['current_hash'] == b.current_hash
    assert d['current_hash'] == "0ad2fc79d6d481dec2a31a59f8f4e5aba35c8f90619dd991e171f5d0e92c2e26"

