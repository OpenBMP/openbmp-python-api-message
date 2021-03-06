
"""
    Copyright (c) 2015-2016 Cisco Systems, Inc. and others.  All rights reserved.
    This program and the accompanying materials are made available under the
    terms of the Eclipse Public License v1.0 which accompanies this distribution,
    and is available at http:#www.eclipse.org/legal/epl-v10.html
"""
from .Base import Base
from .FieldProcessors import ParseNullAsEmpty, ParseLongEmptyAsZero, NotNull, ParseInt, ParseLong, ParseTimestamp
from .Message import Message
from .MsgBusFields import MsgBusFields


class LsPrefix(Base):
    """
    Format class for ls_prefix parsed messages (openbmp.parsed.ls_prefix)

    Schema Version: 1.4
    """

    minimum_header_names = [
        MsgBusFields.ACTION.get_name(),
        MsgBusFields.SEQUENCE.get_name(),
        MsgBusFields.HASH.get_name(),
        MsgBusFields.BASE_ATTR_HASH.get_name(),
        MsgBusFields.ROUTER_HASH.get_name(),
        MsgBusFields.ROUTER_IP.get_name(),
        MsgBusFields.PEER_HASH.get_name(),
        MsgBusFields.PEER_IP.get_name(),
        MsgBusFields.PEER_ASN.get_name(),
        MsgBusFields.TIMESTAMP.get_name(),
        MsgBusFields.IGP_ROUTER_ID.get_name(),
        MsgBusFields.ROUTER_ID.get_name(),
        MsgBusFields.ROUTING_ID.get_name(),
        MsgBusFields.LS_ID.get_name(),
        MsgBusFields.OSPF_AREA_ID.get_name(),
        MsgBusFields.ISIS_AREA_ID.get_name(),
        MsgBusFields.PROTOCOL.get_name(),
        MsgBusFields.AS_PATH.get_name(),
        MsgBusFields.LOCAL_PREF.get_name(),
        MsgBusFields.MED.get_name(),
        MsgBusFields.NEXTHOP.get_name(),
        MsgBusFields.LOCAL_NODE_HASH.get_name(),
        MsgBusFields.MT_ID.get_name(),
        MsgBusFields.OSPF_ROUTE_TYPE.get_name(),
        MsgBusFields.IGP_FLAGS.get_name(),
        MsgBusFields.ROUTE_TAG.get_name(),
        MsgBusFields.EXT_ROUTE_TAG.get_name(),
        MsgBusFields.OSPF_FWD_ADDR.get_name(),
        MsgBusFields.IGP_METRIC.get_name(),
        MsgBusFields.PREFIX.get_name(),
        MsgBusFields.PREFIX_LEN.get_name()
    ]

    def __init__(self, message):
        """
        Handle the message by parsing it and storing the data in memory.

        :param message: 'Message' object.
        """
        if not isinstance(message, Message):
            raise TypeError("Expected Message object instead of type " + type(message))

        data = message.get_content()
        version = message.get_version()

        super(LsPrefix, self).__init__()
        self.spec_version = version

        version_specific_headers = []

        if version >= float(1.3):
            version_specific_headers += [MsgBusFields.ISPREPOLICY.get_name(), MsgBusFields.IS_ADJ_RIB_IN.get_name()]

        if version >= float(1.4):
            version_specific_headers += [MsgBusFields.LS_PREFIX_SID.get_name()]

        # Concatenate minimum header names and version specific header names.
        self.header_names = LsPrefix.minimum_header_names + version_specific_headers

        self.processors = self.get_processors()

        if data:
            self.parse(version, data)

    def get_processors(self):
        """
        Processors used for each field.
        Order matters and must match the same order as defined in headerNames

        :return: array of cell processors.
        """

        default_cell_processors = [
            NotNull(),  # action
            ParseLong(),  # seq
            NotNull(),  # hash
            NotNull(),  # base_hash
            NotNull(),  # router_hash
            NotNull(),  # router_ip
            NotNull(),  # peer_hash
            NotNull(),  # peer_ip
            ParseLong(),  # peer_asn
            ParseTimestamp(),  # timestamp
            ParseNullAsEmpty(),  # igp_router_id
            ParseNullAsEmpty(),  # router_id
            ParseNullAsEmpty(),  # routing_id
            ParseLongEmptyAsZero(),  # ls_id
            ParseNullAsEmpty(),  # ospf_area_id
            ParseNullAsEmpty(),  # isis_area_id
            ParseNullAsEmpty(),  # protocol
            ParseNullAsEmpty(),  # as_path
            ParseLongEmptyAsZero(),  # local_pref
            ParseLongEmptyAsZero(),  # med
            ParseNullAsEmpty(),  # nexthop
            ParseNullAsEmpty(),  # local_node_hash
            ParseNullAsEmpty(),  # mt_id
            ParseNullAsEmpty(),  # ospf_route_type
            ParseNullAsEmpty(),  # igp_flags
            ParseLongEmptyAsZero(),  # route_tag
            ParseLongEmptyAsZero(),  # ext_route_tag
            ParseNullAsEmpty(),  # ospf_fwd_addr
            ParseLongEmptyAsZero(),  # igp_metric
            NotNull(),  # prefix
            ParseInt(),  # prefix_len
        ]

        version_specific_processors = []

        if self.spec_version >= float(1.3):
            version_specific_processors += [
                ParseLongEmptyAsZero(),  # isPrePolicy
                ParseLongEmptyAsZero()  # isAdjRibIn
            ]

        if self.spec_version >= float(1.3):
            version_specific_processors += [

                ParseNullAsEmpty()  # LS Prefix SID
            ]

        return default_cell_processors + version_specific_processors
