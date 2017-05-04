#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Block for simpleChain. """

from __future__ import absolute_import
from typing import Any, Optional
from hashlib import sha256
from datetime import datetime

__all__ = ['Block', 'first_block']

_BLOCK_VERSION = 0x1


class Block(object):
    """
    Block for simpleChain. 
    
    """

    __slots__ = ['version', 'index', 'pre_hash', 'timestamp', 'data', 'current_hash']

    def __init__(self, index: int, pre_hash: str, data: Any, timestamp: Optional[int] = None,
                 current_hash: Optional[str] = None):
        self.version = _BLOCK_VERSION
        self.index = index
        self.pre_hash = pre_hash
        self.timestamp = timestamp if timestamp else int(datetime.utcnow().timestamp())
        # self.merkle
        self.data = data
        self.current_hash = current_hash  # hash is python builtin keyword
        if not self.current_hash:
            self.current_hash = self._calculate_hash()
        elif not self.valid():
            raise ValueError("invalid hash value")

    @classmethod
    def from_dict(cls, block_dict):
        return Block(block_dict['index'], block_dict['pre_hash'],
                     block_dict['data'], block_dict.get('timestamp'),
                     block_dict.get('current_hash'))

    def __eq__(self, other) -> bool:
        return self.current_hash == other.current_hash

    def __iter__(self):
        yield 'version', self.version
        yield 'index', self.index
        yield 'pre_hash', self.pre_hash
        yield 'timestamp', self.timestamp
        yield 'data', self.data
        yield 'current_hash', self.current_hash

    def _calculate_hash(self) -> str:
        """
        calculate Block hash used sha256
        :return: sha256 string
        """
        data_str = str(self.version) + str(self.index) + self.pre_hash + str(self.timestamp) + str(self.data)
        return sha256(data_str.encode('utf-8')).hexdigest()

    def valid(self) -> bool:
        return self.current_hash == self._calculate_hash()


def first_block() -> Block:
    return Block(0, "0", "Let's GO!", 1493317238, "7410f9f78b44fc862e4450632d275ade816a43030e5e82a50ae6677102b083cd")
