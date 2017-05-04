#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" REST Interface server """
from aiohttp import web
import json

from simplechain.blockchain import BlockChain
from simplechain.peers import Peers


class Server(object):
    def __init__(self, app, bc: BlockChain, peers: Peers):
        self.app = app
        self.bc = bc
        self.peers = peers
        self.app.router.add_get('/blocks', self.blocks)
        self.app.router.add_post('/block', self.mine_block)
        self.app.router.add_get('/peers', self.get_peers)
        self.app.router.add_post('/peer', self.add_peer)

    async def blocks(self, request):
        # return web.Response(text=self.blockchain.json(), content_type='application/json')
        return self.response({'blocks': self.bc.dict()})

    async def get_peers(self, request):
        return self.response({'peers': self.peers.peers})

    async def mine_block(self, request):
        data = json.loads((await request.read()).decode('utf-8')).get('data')
        if not data:
            return self.response({'block': None})
        self.bc.generate_block(data)
        # Broadcast new block to other peers
        await self.peers.broad_lasted()
        return self.response({'block': dict(self.bc.lasted)})

    async def peers(self, request):
        return self.response({'peers': self.peers.peers})

    async def add_peer(self, request):
        peer = json.loads((await request.read()).decode('utf-8')).get('peer')
        if not peer:
            return
        if type(peer) is not list:
            peer = [peer]
        await self.peers.add_peers(peer)
        return self.response({'peers': self.peers.peers})

    @staticmethod
    def response(msg):
        return web.json_response(msg)
