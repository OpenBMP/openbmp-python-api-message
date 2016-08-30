#!/usr/bin/env python

import time
import datetime
import calendar
import getopt
import sys
import os
import yaml
import socket
import kafka
import traceback

from UnicastPrefix import *
from Router import *
from Peer import *
from Collector import *
from BmpStat import *
from BaseAttribute import *
from LsNode import *
from LsLink import *
from LsPrefix import *

from Message import *

def processMessage(msg):
    """ Process the message

    :param msg:     Message consumed

    :return:
    """

    m = Message(msg.value)
    t = msg.topic

    if t == "openbmp.parsed.router":
        router = Router(m.getVersion(), m.getContent())

    elif t == "openbmp.parsed.peer":
        peer = Peer(m.getVersion(), m.getContent())

    elif t == "openbmp.parsed.collector":
        collector = Collector(m.getVersion(), m.getContent())

    elif t == "openbmp.parsed.bmp_stat":
        bmp_stat = BmpStat(m.getVersion(), m.getContent())

    elif t == "openbmp.parsed.unicast_prefix":
        unicastPrefix = UnicastPrefix(m.getVersion(), m.getContent())
        print unicastPrefix.toJsonPretty()

    elif t == "openbmp.parsed.base_attribute":
        base_attribute = BaseAttribute(m.getVersion(), m.getContent())

    elif t == "openbmp.parsed.ls_node":
        ls_node = LsNode(m.getVersion(), m.getContent())

    elif t == "openbmp.parsed.ls_link":
        ls_link = LsLink(m.getVersion(), m.getContent())

    elif t == "openbmp.parsed.ls_prefix":
        ls_prefix = LsPrefix(m.getVersion(), m.getContent())

def main():
    # Enable to topics/feeds
    topics = [ 'openbmp.parsed.router', 'openbmp.parsed.peer', 'openbmp.parsed.collector',
               'openbmp.parsed.bmp_stat', 'openbmp.parsed.unicast_prefix', 'openbmp.parsed.base_attribute',
               'openbmp.parsed.ls_node', 'openbmp.parsed.ls_link', 'openbmp.parsed.ls_prefix' ]


    try:
        # connect and bind to topics
        print "Connecting to kafka... takes a minute to load offsets and topics, please wait"
        consumer = kafka.KafkaConsumer(
                            *topics,
                            bootstrap_servers="kafka-int.openbmp.org",
                            client_id="dev-testing" + str(time.time()),
                            group_id="dev-testing" + str(time.time()),
                            enable_auto_commit=True,
                            auto_commit_interval_ms=1000,
                            auto_offset_reset="largest")

        print "Now consuming/waiting for messages..."
        for m in consumer:
            processMessage(m)

    except kafka.common.KafkaUnavailableError as err:
        print "Kafka Error: %s" % str(err)

    except KeyboardInterrupt:
        print "User stop requested"

if __name__ == '__main__':
    main()