from kapi import validators
from kapi.codecs import BaseCodec
from kapi.parse import parse_yaml

TOMYUM_CONFIG = validators.Object(
    properties=[
        ('schema', validators.Object(
            properties=[
                ('path', validators.String()),
                ('format', validators.String(enum=['openapi', 'swagger'])),
            ],
            additional_properties=False,
            required=['path', 'format']
        )),
        ('docs', validators.Object(
            properties=[
                ('theme', validators.String(enum=['kapi', 'redoc', 'swaggerui'])),
            ],
            additional_properties=False,
        ))
    ],
    additional_properties=False,
    required=['schema'],
)


class ConfigCodec(BaseCodec):
    media_type = 'application/x-yaml'
    format = 'kapi'

    def decode(self, content, **options):
        return parse_yaml(content, validator=TOMYUM_CONFIG)
