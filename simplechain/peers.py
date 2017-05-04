#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" P2P network function """

from enum import IntEnum
from typing import List
import json
from aiohttp import web
import aiohttp

from simplechain.blockchain import BlockChain
from simplechain.block import Block


class MessageType(IntEnum):
    QUERY_LASTED = 0
    RESPONSE_LASTED = 1
    QUERY_ALL = 2
    RESPONSE_ALL = 3
    QUERY_PEERS = 4
    RESPONSE_PEERS = 5


# TODO: 1. 每对节点之间只需要建立一个链接就足够了 2. 限制下最多链接的数目
class Peers(object):
    """
    Manage peers websocket communication.
    """

    def __init__(self, app, bc: BlockChain, peers: List[str] = None):
        self.peers = peers
        self.app = app
        self.bc = bc
        self.session = None
        self.peer_connections = list()
        self.msg2method = {
            MessageType.QUERY_LASTED: self.query_lasted,
            MessageType.RESPONSE_LASTED: self.response_lasted,
            MessageType.QUERY_ALL: self.query_all,
            MessageType.RESPONSE_ALL: self.response_all,
            MessageType.QUERY_PEERS: self.query_peers,
            MessageType.RESPONSE_PEERS: self.response_peers,
        }
        self.app.router.add_get("/p2p", self.websocket_handler)

        if peers:
            self.connect_to_peers(peers)

    async def add_peers(self, peers: List[str]):
        new_peers = [set(peers) - set(self.peers)]
        if new_peers:
            self.peers = self.peers + new_peers
            # connect
            await self.connect_to_peers(new_peers)

    async def connect_to_peers(self, peers: List[str]):
        if not self.session:
            self.session = aiohttp.ClientSession()

        for peer in peers:
            connection = await self.session.ws_connect(peer)
            self.peer_connections.append(connection)
            # TODO: send lasted request
            await connection.send_str(Peers.msg_build(MessageType.QUERY_LASTED))
            await connection.send_str(Peers.msg_build(MessageType.QUERY_PEERS))

    async def broad_lasted(self):
        self._broadcast(Peers.msg_build(MessageType.RESPONSE_LASTED, dict(self.bc.lasted)))

    async def _broadcast(self, msg: str):
        for pc in self.peer_connections:
            await pc.send_str(msg)

    @staticmethod
    def msg_build(t: MessageType, data=None):
        if data:
            return json.dumps({'type': t, 'data': data})
        else:
            return json.dumps({'type': t})

    async def query_lasted(self, ws, msg):
        print(ws)
        ws.send_str(Peers.msg_build(MessageType.RESPONSE_LASTED, dict(self.bc.lasted)))

    async def response_lasted(self, ws, msg):
        # check lasted is longer than local
        index = msg['index']
        if index and index > self.bc.lasted.index:
            if index == self.bc.lasted.index + 1:
                self.bc.add_block(msg)
            else:
                ws.send_str(Peers.msg_build(MessageType.QUERY_ALL, {'after': self.bc.lasted.index}))

    async def query_all(self, ws, msg):
        after = 0
        if msg and msg.get('after'):
            after = msg.get('after')

        bc_list = self.bc.dict(after)
        ws.send_str(Peers.msg_build(MessageType.RESPONSE_ALL, bc_list))

    async def response_all(self, ws, msg):
        if not msg:
            return
        bc_list = [Block.from_dict(b) for b in msg]
        self.bc.update(bc_list)

    async def query_peers(self, ws, msg):
        ws.send_str(Peers.msg_build(MessageType.RESPONSE_PEERS, self.peers))

    async def response_peers(self, ws, msg):
        if type(msg) is not list:
            return
        await self.add_peers(msg)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                msg_data = json.loads(msg.data)

                if 'type' not in msg_data:
                    raise ValueError('Wrong message format')

                t = MessageType(msg_data['type'])
                print(t)
                # print(MessageType.__members__)
                # if t not in MessageType.__members__:
                #     raise ValueError('Unknown message type')

                # call msg process method
                m = self.msg2method[t]
                await m(ws, msg_data.get('data'))

            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

        print('websocket connection closed')
        return ws
