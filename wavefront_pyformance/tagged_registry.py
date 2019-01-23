"""
Tagged Metrics Registry.

@author: Hao Song (songhao@vmware.com)
"""
import json
from pyformance import MetricsRegistry


class TaggedRegistry(MetricsRegistry):
    """Tagged Metrics Registry."""

    @staticmethod
    def encode_key(key, tags):
        """
        Encode key and tags into a <key>-tags=<tags> format str.

        :param key: Key name
        :type key: str
        :param tags: Tags
        :type tags: dict
        :return: Encoded key
        :rtype: str
        """
        if tags is not None:
            key += '-tags='
            key += json.dumps(tags, sort_keys=True)
        return key

    # pylint: disable=arguments-differ
    def counter(self, key, tags=None):
        """Get a counter based on a encoded key."""
        return super(TaggedRegistry, self).counter(self.encode_key(key, tags))

    # pylint: disable=arguments-differ
    def histogram(self, key, tags=None):
        """Get a histogram based on a encoded key."""
        return super(TaggedRegistry, self).histogram(
            self.encode_key(key, tags))

    # pylint: disable=arguments-differ
    def gauge(self, key, gauge=None, default=float("nan"), tags=None):
        """Get a gauge based on a encoded key."""
        return super(TaggedRegistry, self).gauge(
            self.encode_key(key, tags), gauge, default)

    # pylint: disable=arguments-differ
    def meter(self, key, tags=None):
        """Get a meter based on a encoded key."""
        return super(TaggedRegistry, self).meter(self.encode_key(key, tags))

    # pylint: disable=arguments-differ
    def timer(self, key, tags=None):
        """Get a timer based on a encoded key."""
        return super(TaggedRegistry, self).timer(self.encode_key(key, tags))

    def has_counter(self, key, tags=None):
        return self.encode_key(key, tags) in self._counters
