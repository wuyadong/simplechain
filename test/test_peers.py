#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import json
from simplechain.block import Block
from simplechain.peers import Peers, MessageType
from simplechain.blockchain import BlockChain
from aiohttp import web
import aiohttp


async def test_query(test_client):
    bc = BlockChain()
    app = web.Application()
    peers = Peers(app, bc)
    client = await test_client(app)
    c = await client.ws_connect('/p2p')

    # QUERY_LASTED
    c.send_str(Peers.msg_build(MessageType.QUERY_LASTED))
    msg = await c.receive()
    assert msg.type == aiohttp.WSMsgType.TEXT
    msg_data = json.loads(msg.data)
    t = MessageType(msg_data['type'])
    assert t == MessageType.RESPONSE_LASTED
    data = msg_data['data']
    assert data == dict(peers.bc.lasted)

    # QUERY_ALL
    block = Block(1, bc.lasted.current_hash, "test")
    assert BlockChain.valid_block(bc.lasted, block)
    bc.add_block(block)
    c.send_str(Peers.msg_build(MessageType.QUERY_ALL))
    msg = await c.receive()
    assert msg.type == aiohttp.WSMsgType.TEXT
    msg_data = json.loads(msg.data)
    t = MessageType(msg_data['type'])
    assert t == MessageType.RESPONSE_ALL
    data = msg_data['data']
    assert data == peers.bc.dict()



