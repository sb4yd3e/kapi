import queries
from settings import uri
from kapi.utils import encode_json
from kapi.http import Response


class Meta(type):
    db_table = None
    fields = None
    list_fields = None
    geo_fields = None

    limit = 10
    offset = 0


class SQLSerializer(metaclass=Meta):

    def __init__(self, *arg, **kwargs):
        super(SQLSerializer, self).__init__()
        self._meta = getattr(self, 'Meta')
        self.fields_iter = ", ".join(list(iter(self._meta.fields)))
        self.limit = kwargs['limit']
        self.offset = kwargs['offset']

    def sql_query_builder(self, fields, db_table, limit, offset):
        return "SELECT {} FROM {} LIMIT {} OFFSET {};".format(fields, db_table, limit, offset)

    def query_set(self):
        return self.sql_query_builder(self.fields_iter, self._meta.db_table, self.limit, self.offset)

    @property
    def json_respone(self):
        with queries.Session(uri) as s:
            result_set = [row for row in s.query(self.query_set())]
            for items in result_set:
                for f in self._meta.list_fields:
                    if items[f]:
                        items[f] = items[f].split(',')

                for f in self._meta.geo_fields:
                    if items[f]:
                        items[f] = list(map(float, items[f].split(',')))
        return Response(encode_json({"data": result_set}, True))
