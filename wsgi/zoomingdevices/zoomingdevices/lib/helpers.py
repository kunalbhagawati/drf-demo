"""Helper functions"""


def unicode_if_bytes(duck):
    """Returns unicode encoded string if duck is of type 'bytes' else returns
    the duck without converting"""

    return duck.decode('utf-8') if isinstance(duck, bytes) else duck


class RedisConverter:
    """Helps in conversion of the results fetched from redis"""

    def __init__(self, encoding='utf-8', decoding='bytes'):
        # Just dummy for now
        self.encoding = encoding
        self.decoding = decoding

    @classmethod
    def decode(cls, duck):
        """Decode the redis result into unicode ('utf-8') if
        there is a bytestring in the result else just returns the object.
        i.e. only decodes bytestrings wherever found."""

        if isinstance(duck, dict):
            return RedisConverter._decode_dict(duck)
        elif isinstance(duck, bytes):
            return RedisConverter._decode_bytes(duck)
        elif hasattr(duck, '__iter__'):     # assuming never returns string
            return RedisConverter._decode_lists(duck)
        elif (isinstance(duck, (bool, str))
                or duck is None):
            return duck
        else:   # any other case I left out?
            raise Exception("RedisConverter.decode() does not know "
                    "how to convert type '{0}' (Duck passed: {1})"
                    .format(duck.__class__, duck))

    @classmethod
    def _decode_dict(cls, duck):
        retDict = {}
        for i, v in duck.items():
            retDict[unicode_if_bytes(i)] = unicode_if_bytes(v)
        return retDict

    @classmethod
    def _decode_bytes(cls, duck):
        return duck.decode('utf-8')

    @classmethod
    def _decode_lists(cls, duck):
        return duck.__class__([unicode_if_bytes(x) for x in duck])

    @classmethod
    def multiget_to_dict(cls, keyList, resList):
        """Coverts the list like object returned by hmget and such
        into a dict."""

        return dict(
                [(keyList(i), resList(i)) for i in range(0, len(keyList))])
