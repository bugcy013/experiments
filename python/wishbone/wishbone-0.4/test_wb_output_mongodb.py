#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  test_wb_input_amqp.py
#
#  Copyright 2013 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from wishbone import Actor
from wishbone.router import Default
from wishbone.tools import Measure

from wishbone.module import Graphite
from wishbone.module import Null
from wishbone.module import LogFormatFilter
from wishbone.module import STDOUT
from wb_input_dictgenerator import DictGenerator
from wb_output_tcp import TCP
from wb_output_mongodb import MongoDB

from gevent import sleep, spawn

#Initialize router
router = Default(interval=1, context_switch=100, rescue=False, uuid=False)
router.registerLogModule((LogFormatFilter, "logformatfilter", 0), "inbox", debug=True)
router.registerMetricModule((Graphite, "graphite", 0), "inbox")
router.register((STDOUT, "stdout", 0))
router.register((Null, "null", 0))
router.register((TCP, 'graphite_out', 0), host="graphite-001", port=2013, stream=True )
router.connect("logformatfilter.outbox", "stdout.inbox")
router.connect("graphite.outbox", "graphite_out.inbox")

#Consume events to STDOUT
router.register((DictGenerator, "dictgenerator", 0), max_elements=10)
router.register((MongoDB, "mongodb", 0), host="sandbox", capped=True, drop_db=False)

router.connect("dictgenerator.outbox", "mongodb.inbox")

#start
router.start()
router.block()