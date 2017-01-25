
"""
    Copyright (c) 2015-2016 Cisco Systems, Inc. and others.  All rights reserved.
    This program and the accompanying materials are made available under the
    terms of the Eclipse Public License v1.0 which accompanies this distribution,
    and is available at http://www.eclipse.org/legal/epl-v10.html
"""


class Message(object):
    """
    Kafka Message class. This class processes header of raw Kafka messages.
    """

    def __init__(self, data):
        """
        Handle the message by parsing header of it.

        :param data: Raw Kafka message as string.
        """

        if not data.strip():  # If "data" is not string, throws error.
            raise "Invalid data!", data

        self.version = float()
        self.collector_hash_id = str()
        self.length = long()
        self.records = long()
        self.router_hash_id = str()
        self.content = str()
        self.content_pos = int()
        self.router_ip = str()

        self.__parse(data)

    def __parse(self, data):
        """
        Parses header of raw Kafka messages and set the version, length, number of records and router hash id.

        :param data: Raw Kafka message as string.
        """

        data_end_pos = data.find("\n\n")
        header_data = data[:data_end_pos]

        self.content_pos = data_end_pos + 2
        self.content = data[self.content_pos:]

        headers = header_data.split("\n")

        for header in headers:
            value = header.split(":")[1].strip()
            attr = header.split(":")[0].strip()

            # Attribute names are from http://openbmp.org/#!docs/MESSAGE_BUS_API.md headers
            if attr == "V":
                self.version = float(value)

            elif attr == "C_HASH_ID":
                self.collector_hash_id = value

            elif attr == "L":
                self.length = long(value)

            elif attr == "R":
                self.records = long(value)

            elif attr == "R_HASH_ID":
                self.router_hash_id = value

            elif attr == "R_IP":
                self.router_ip = value

    def get_version(self):
        return self.version

    def get_collector_hash_id(self):
        return self.collector_hash_id

    def get_length(self):
        return self.length

    def get_records(self):
        return self.records

    def get_router_hash_id(self):
        return self.router_hash_id

    def get_router_ip(self):
        return self.router_ip

    def get_content_pos(self):
        return self.content_pos

    def get_content(self):
        return self.content
