# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import sys
from pyformance.reporters.reporter import Reporter
from wavefront_python_sdk import WavefrontDirectClient, WavefrontProxyClient
from . import delta

if sys.version_info[0] > 2:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


class WavefrontReporter(Reporter):
    """
    Base reporter for reporting data in Wavefront format.
    """

    def __init__(self, wavefront_client, source="wavefront-pyformance",
                 registry=None,
                 reporting_interval=10, clock=None, prefix="", tags=None):
        super(WavefrontReporter, self).__init__(
            registry=registry, reporting_interval=reporting_interval,
            clock=clock)
        self.wavefront_client = wavefront_client
        self.source = source
        self.prefix = prefix
        self.tags = tags or {}

    def report_now(self, registry=None, timestamp=None):
        timestamp = timestamp or int(round(self.clock.time()))
        registry = registry or self.registry
        metrics = registry.dump_metrics()
        for key in metrics.keys():
            is_delta = delta.is_delta_counter(key, registry)
            for value_key in metrics[key].keys():
                if is_delta:
                    self.wavefront_client.send_delta_counter(
                        name=delta.get_delta_name(self.prefix, key, value_key),
                        value=metrics[key][value_key], source=self.source,
                        tags=self.tags
                    )
                    # decrement delta counter
                    registry.counter(key).dec(metrics[key][value_key])
                else:
                    self.wavefront_client.send_metric(
                        name="%s%s.%s" % (self.prefix, key, value_key),
                        value=metrics[key][value_key], timestamp=timestamp,
                        source=self.source,  tags=self.tags)

    def stop(self):
        super(WavefrontReporter, self).stop()
        self.wavefront_client.close()


class WavefrontProxyReporter(WavefrontReporter):
    """
    This reporter requires a host and port to report data to a Wavefront proxy.
    """

    def __init__(self, host, port=2878, source="wavefront-pyformance",
                 registry=None, reporting_interval=10, clock=None,
                 prefix="proxy.", tags=None):
        tags = tags or {}
        self.proxy_client = WavefrontProxyClient(host=host,
                                                 metrics_port=port,
                                                 distribution_port=None,
                                                 tracing_port=None)
        super(WavefrontProxyReporter, self).__init__(
            wavefront_client=self.proxy_client, source=source,
            registry=registry, reporting_interval=reporting_interval,
            clock=clock, prefix=prefix, tags=tags)

    def report_now(self, registry=None, timestamp=None):
        timestamp = timestamp or int(round(self.clock.time()))
        registry = registry or self.registry
        super(WavefrontProxyReporter, self).report_now(registry, timestamp)

    def stop(self):
        super(WavefrontProxyReporter, self).stop()


class WavefrontDirectReporter(WavefrontReporter):
    """
    This reporter report data directly to a Wavefront server.

    Requires a server and a token.
    """

    def __init__(self, server, token, source="wavefront-pyformance",
                 registry=None, reporting_interval=10, clock=None,
                 prefix="direct.", tags=None):
        tags = tags or {}
        self.server = self._validate_url(server)
        self.token = token
        self.batch_size = 10000
        self.direct_client = WavefrontDirectClient(
            self.server, token, batch_size=self.batch_size,
            flush_interval_seconds=reporting_interval)
        super(WavefrontDirectReporter, self).__init__(
            wavefront_client=self.direct_client, source=source,
            registry=registry, reporting_interval=reporting_interval,
            clock=clock, prefix=prefix, tags=tags)

    def stop(self):
        super(WavefrontDirectReporter, self).stop()

    @staticmethod
    def _validate_url(server):
        parsed_url = urlparse(server)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("invalid server url")
        return server

    def report_now(self, registry=None, timestamp=None):
        timestamp = timestamp or int(round(self.clock.time()))
        registry = registry or self.registry
        super(WavefrontDirectReporter, self).report_now(registry, timestamp)
        self.direct_client.flush_now()
