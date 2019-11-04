#! /usr/bin/env python3
"""Python Runtime Metric Collection Example."""


import argparse
import time


from wavefront_pyformance import tagged_registry
from wavefront_pyformance import wavefront_reporter


def report_metrics(host, server='', token=''):
    """Runtime Metric Reporting Function Example."""
    reg = tagged_registry.TaggedRegistry()
    
    wf_proxy_reporter = wavefront_reporter.WavefrontProxyReporter(
        host=host, port=2878, registry=reg,
        source='runtime-metric-test',
        tags={'global_tag1': 'val1', 'global_tag2': 'val2'},
        prefix='python.proxy.',
        enable_runtime_metrics=True).report_minute_distribution()
    wf_direct_reporter = wavefront_reporter.WavefrontDirectReporter(
        server=server, token=token, registry=reg,
        source='runtime-metric-test',
        tags={'global_tag1': 'val1', 'global_tag2': 'val2'},
        prefix='python.direct.',
        enable_runtime_metrics=False).report_minute_distribution()

    wf_proxy_reporter.report_now()
    wf_proxy_reporter.stop()
    wf_direct_reporter.report_now()
    wf_direct_reporter.stop()


if __name__ == '__main__':
    # python example_runtime_metrics.py proxy_host server_url server_token
    arg = argparse.ArgumentParser()
    arg.add_argument('host', help='Wavefront proxy host name.')
    arg.add_argument('server', help='Wavefront server for direct ingestion.')
    arg.add_argument('token', help='Wavefront API token.')
    ARGS = arg.parse_args()
    while True:
        # report_metrics(ARGS.host)
        report_metrics(ARGS.host, ARGS.server, ARGS.token)
        time.sleep(5)
