#! /usr/bin/env python3
"""Wavefront PyFormance Usage Example."""

import argparse
import time

from wavefront_pyformance import delta
from wavefront_pyformance import tagged_registry
from wavefront_pyformance import wavefront_histogram
from wavefront_pyformance import wavefront_reporter


def report_metrics(proxy_reporter, direct_reporter):
    """Metrics Reporting Function Example."""

    # counter
    c_1 = reg.counter('foo_count', tags={'counter_key': 'counter_val'})
    c_1.inc()

    # delta counter
    d_1 = delta.delta_counter(reg, 'foo_delta_count',
                              tags={'delta_key': 'delta_val'})
    d_1.inc()
    d_1.inc()

    # gauge
    g_1 = reg.gauge('foo_gauge', tags={'gauge_key': 'gauge_val'})
    g_1.set_value(2)

    # meter
    m_1 = reg.meter('foo_meter', tags={'meter_key': 'meter_val'})
    m_1.mark()

    # timer
    t_1 = reg.timer('foo_timer', tags={'timer_key': 'timer_val'})
    timer_ctx = t_1.time()
    time.sleep(3)
    timer_ctx.stop()

    # histogram
    h_1 = reg.histogram('foo_histogram', tags={'hist_key': 'hist_val'})
    h_1.add(1.0)
    h_1.add(1.5)

    # Wavefront Histogram
    h_2 = wavefront_histogram.wavefront_histogram(reg, 'wf_histogram')
    h_2.add(1.0)
    h_2.add(2.0)

    direct_reporter.report_now()
    direct_reporter.stop()
    proxy_reporter.report_now()
    proxy_reporter.stop()


if __name__ == '__main__':
    # python example.py proxy_host server_url server_token
    _ = argparse.ArgumentParser()
    _.add_argument('host', help='Wavefront proxy host name.')
    _.add_argument('server', help='Wavefront server for direct ingestion.')
    _.add_argument('token', help='Wavefront API token.')
    ARGS = _.parse_args()

    reg = tagged_registry.TaggedRegistry()

    wf_proxy_reporter = wavefront_reporter.WavefrontProxyReporter(
        host=ARGS.host, port=2878, distribution_port=2878, registry=reg,
        source='wavefront-pyformance-example',
        tags={'key1': 'val1', 'key2': 'val2'},
        prefix='python.proxy.').report_minute_distribution()

    wf_direct_reporter = wavefront_reporter.WavefrontDirectReporter(
        server=ARGS.server, token=ARGS.token, registry=reg,
        source='wavefront-pyformance-exmaple',
        tags={'key1': 'val1', 'key2': 'val2'},
        prefix='python.direct.').report_minute_distribution()

    while True:
        report_metrics(wf_proxy_reporter, wf_direct_reporter)
        time.sleep(1)
