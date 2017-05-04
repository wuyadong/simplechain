#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" BlockChain for simpleChain. """

from __future__ import absolute_import

from typing import List

from simplechain.block import Block, first_block

__all__ = ['BlockChain']


class BlockChain(object):
    """
    BlockChain
    """

    def __init__(self):
        self._blocks = [first_block()]

    def __len__(self):
        return len(self._blocks)

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        return all(s == o for s, o in zip(self._blocks, other.blocks))

    @property
    def blocks(self):
        return self._blocks

    @property
    def lasted(self):
        return self._blocks[-1]

    @property
    def index(self) -> int:
        return self.lasted.index

    @staticmethod
    def valid_block(pre_block: Block, block: Block) -> bool:
        if block.pre_hash != pre_block.current_hash:
            print("invalid pre_hash")
            return False
        if block.index != pre_block.index + 1:
            print("invalid index")
            return False
        if block.timestamp < pre_block.timestamp:
            print("invalid timestamp")
            return False
        if not block.valid():
            print("invalid block")
            return False
        return True

    @staticmethod
    def valid_blocks(blocks: List[Block]) -> bool:
        return all(BlockChain.valid_block(blocks[i], blocks[i + 1]) for i in range(len(blocks) - 1))

    def check_valid_new(self, block: Block) -> bool:
        pre_block = self.lasted
        return self.valid_block(pre_block, block)

    def generate_block(self, data):
        block = Block(self.index + 1, self.lasted.current_hash, data)
        self.add_block(block)

    def add_block(self, block: Block):
        """
        Add new Block
        :param block: 
        :return: 
        """
        if not self.check_valid_new(block):
            return
        self._blocks.append(block)

    def valid(self) -> bool:
        """
        Check self is valid block chain
        :return: 
        """
        if self._blocks[0] != first_block():
            return False

        return self.valid_blocks(self._blocks)

    def update(self, blocks: List[Block]):
        if not blocks:
            return
        if blocks[-1].index <= self.index:
            return
        if not self.valid_blocks(blocks):
            return

        s = blocks[0]
        if s.index <= 0:
            # replace
            if blocks[0] == first_block():
                self._blocks = blocks
        else:
            pre = self._blocks[s.index - 1]
            if self.valid_block(pre, s):
                replace_number = self.lasted.index - s.index
                self.blocks[s.index:] = blocks[0:replace_number]
                self.blocks.extend(blocks[replace_number:])

    def dict(self, after=None):
        if not after:
            after = 0
        return [dict(b) for b in self.blocks[after:]]

