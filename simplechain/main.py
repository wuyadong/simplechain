#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Main for simpleChain. """

from __future__ import absolute_import

from aiohttp import web
from simplechain.blockchain import BlockChain
from simplechain.peers import Peers
from simplechain.server import Server
from simplechain.config import Config

if __name__ == '__main__':
    config = Config()
    bc = BlockChain()
    app = web.Application()
    peers = Peers(app, bc, config.option.get('peers'))
    server = Server(app, bc, peers)
    web.run_app(app, port=8080)
