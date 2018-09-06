import json
from pyformance import MetricsRegistry


class TaggedRegistry(MetricsRegistry):

    @staticmethod
    def encode_key(key, tags):
        if tags is not None:
            key += '-tags='
            key += json.dumps(tags, sort_keys=True)
        return key

    def counter(self, key, tags=None):
        return super(TaggedRegistry, self).counter(self.encode_key(key, tags))

    def histogram(self, key, tags=None):
        return super(TaggedRegistry, self).histogram(
            self.encode_key(key, tags))

    def gauge(self, key, gauge=None, default=float("nan"), tags=None):
        return super(TaggedRegistry, self).gauge(
            self.encode_key(key, tags), gauge, default)

    def meter(self, key, tags=None):
        return super(TaggedRegistry, self).meter(self.encode_key(key, tags))

    def timer(self, key, tags=None):
        return super(TaggedRegistry, self).timer(self.encode_key(key, tags))
