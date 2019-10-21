import argparse
import time
import sys

sys.path.insert(1, '../')

from wavefront_pyformance import tagged_registry
from wavefront_pyformance import wavefront_reporter

def report_metrics(host):
    reg = tagged_registry.TaggedRegistry()

    wf_proxy_reporter = wavefront_reporter.WavefrontProxyReporter(
        host=host, port=2878, registry=reg,
        source='runtime-metric-test',
        tags={'global_tag1': 'val1', 'global_tag2': 'val2'},
        prefix='python.runtime.',
        runtime_metric=True).report_minute_distribution()

    wf_proxy_reporter.report_now()
    wf_proxy_reporter.stop()

if __name__ == '__main__':
    arg = argparse.ArgumentParser()
    arg.add_argument('host', help='Wavefront proxy host name.')
    ARGS = arg.parse_args()

    while True:
        report_metrics(ARGS.host)
        time.sleep(30)
