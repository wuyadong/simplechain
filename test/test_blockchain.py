#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from simplechain.blockchain import first_block, Block
from simplechain.blockchain import BlockChain


@pytest.fixture()
def bc():
    return BlockChain()

def test_first(bc):
    assert bc.blocks
    assert bc.blocks[0] == first_block()
    assert bc.lasted == bc.blocks[0]
    assert bc.index == 0


def test_add(bc):
    block = Block(1, first_block().current_hash, "test")
    assert BlockChain.valid_block(bc.lasted, block)
    bc.add_block(block)
    assert bc.index == 1
    assert bc.lasted.data == "test"
    assert bc.lasted.pre_hash == first_block().current_hash
    assert BlockChain.valid_blocks(bc.blocks)
    assert bc.valid()


def test_update(bc):
    block = Block(1, bc.lasted.current_hash, "test")
    block2 = Block(2, block.current_hash, "data")
    block_list = [block, block2]
    assert BlockChain.valid_block(bc.lasted, block)
    assert BlockChain.valid_blocks(block_list)
    bc.update(block_list)
    assert bc.valid()
    assert bc.index == 2
    assert bc.lasted.data == "data"

    block3 = Block(3, block2.current_hash, "test_data")
    block_list.append(block3)
    assert BlockChain.valid_block(bc.lasted, block3)
    assert BlockChain.valid_blocks(block_list)
    bc.update(block_list)
    assert bc.valid()
    assert bc.index == 3
    assert bc.lasted.data == "test_data"






