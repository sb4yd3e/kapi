import json
import datetime
import decimal
import uuid

from kapi import codecs
from kapi.types import Type


class _CustomEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Type):
            return dict(o)
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        elif isinstance(o, (decimal.Decimal, uuid.UUID)):
            return str(o)
        else:
            # pass
            return super().default(o)
        # return json.JSONEncoder.default(self, o)


def encode_json(data, indent=False):
    kwargs = {
        'ensure_ascii': False,
        'allow_nan': False,
        'cls': _CustomEncoder
    }
    if indent:
        kwargs.update({
            'indent': None,
            'separators': (',', ':')
        })
    else:
        kwargs.update({
            'indent': 4,
            'separators': (',', ': ')
        })
    return json.dumps(data, **kwargs).encode('utf-8')


def encode_jsonschema(validator, to_data_structure=False):
    codec = codecs.JSONSchemaCodec()
    return codec.encode(validator, to_data_structure=to_data_structure)
