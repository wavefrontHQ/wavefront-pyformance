# -*- coding: utf-8 -*-
"""WavefrontDirectReporter and WavefrontProxyReporter implementations."""

from __future__ import unicode_literals
import json
from pyformance.reporters import reporter
from wavefront_python_sdk import WavefrontDirectClient, WavefrontProxyClient
from . import delta

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class WavefrontReporter(reporter.Reporter):
    """Base reporter for reporting data in Wavefront format."""

    # pylint: disable=too-many-arguments
    def __init__(self, source='wavefront-pyformance', registry=None,
                 reporting_interval=10, clock=None, prefix='', tags=None):
        """Construct Wavefront Reporter."""
        super(WavefrontReporter, self).__init__(
            registry=registry, reporting_interval=reporting_interval,
            clock=clock)
        self.wavefront_client = None
        self.source = source
        self.prefix = prefix
        self.tags = tags or {}

    @staticmethod
    def decode_key(key):
        """Decode encoded key into original key and dict of tags."""
        if '-tags=' in key:
            decoded_str = key.split('-tags=')
            return decoded_str[0], json.loads(decoded_str[1])
        return key, None

    def report_now(self, registry=None, timestamp=None):
        """Collect metrics from registry and report them to Wavefront."""
        registry = registry or self.registry
        metrics = registry.dump_metrics()
        for key in metrics.keys():
            is_delta = delta.is_delta_counter(key, registry)
            for value_key in metrics[key].keys():
                metric_name, metric_tags = self.decode_key(key)
                tags = {}
                tags.update(self.tags)
                if metric_tags:
                    tags.update(metric_tags)
                if is_delta:
                    self.wavefront_client.send_delta_counter(
                        name=delta.get_delta_name(self.prefix, metric_name,
                                                  value_key),
                        value=metrics[key][value_key], source=self.source,
                        tags=tags
                    )
                    # decrement delta counter
                    registry.counter(key).dec(metrics[key][value_key])
                else:
                    self.wavefront_client.send_metric(
                        name='{}{}.{}'.format(self.prefix, metric_name,
                                              value_key),
                        value=metrics[key][value_key], timestamp=timestamp,
                        source=self.source, tags=tags)

    def stop(self):
        """Stop pyformance and wavefront reporter."""
        super(WavefrontReporter, self).stop()
        self.wavefront_client.close()


class WavefrontProxyReporter(WavefrontReporter):
    """Requires a host and port to report data to a Wavefront proxy."""

    # pylint: disable=too-many-arguments
    def __init__(self, host, port=2878, source='wavefront-pyformance',
                 registry=None, reporting_interval=10, clock=None,
                 prefix='proxy.', tags=None):
        """Run parent __init__ and do proxy reporter specific setup."""
        super(WavefrontProxyReporter, self).__init__(
            source=source, registry=registry,
            reporting_interval=reporting_interval, clock=clock, prefix=prefix,
            tags=tags)
        self.wavefront_client = WavefrontProxyClient(host=host,
                                                     metrics_port=port,
                                                     distribution_port=None,
                                                     tracing_port=None)

    def report_now(self, registry=None, timestamp=None):
        """Collect metrics from registry and report them to Wavefront."""
        timestamp = timestamp or int(round(self.clock.time()))
        super(WavefrontProxyReporter, self).report_now(registry, timestamp)


class WavefrontDirectReporter(WavefrontReporter):
    """Direct Reporter for sending metrics using direct ingestion.

    This reporter requires a server and a token to report data
    directly to a Wavefront server.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, server, token, source='wavefront-pyformance',
                 registry=None, reporting_interval=10, clock=None,
                 prefix='direct.', tags=None):
        """Run parent __init__ and do direct reporter specific setup."""
        super(WavefrontDirectReporter, self).__init__(
            source=source, registry=registry,
            reporting_interval=reporting_interval, clock=clock, prefix=prefix,
            tags=tags)
        self.server = self._validate_url(server)
        self.token = token
        self.batch_size = 10000
        self.wavefront_client = WavefrontDirectClient(
            self.server, token, batch_size=self.batch_size,
            flush_interval_seconds=reporting_interval)

    @staticmethod
    def _validate_url(server):  # pylint: disable=no-self-use
        """Validate URL of server."""
        parsed_url = urlparse(server)
        if not all((parsed_url.scheme, parsed_url.netloc)):
            raise ValueError('invalid server url')
        return server

    def report_now(self, registry=None, timestamp=None):
        """Collect metrics from registry and report them to Wavefront."""
        super(WavefrontDirectReporter, self).report_now(registry, timestamp)
        self.wavefront_client.flush_now()
