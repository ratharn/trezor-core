# Automatically generated by pb2py
import protobuf as p
from .NEMMosaic import NEMMosaic


class NEMTransfer(p.MessageType):
    FIELDS = {
        1: ('recipient', p.UnicodeType, 0),
        2: ('amount', p.UVarintType, 0),
        3: ('payload', p.BytesType, 0),
        4: ('public_key', p.BytesType, 0),
        5: ('mosaics', NEMMosaic, p.FLAG_REPEATED),
    }
