from wavefront_pyformance.tagged_registry import TaggedRegistry
from wavefront_pyformance.wavefront_reporter import \
    WavefrontProxyReporter, WavefrontDirectReporter
from wavefront_pyformance import delta, wavefront_histogram
import time
import sys


def report_metrics(host, server, token):
    reg = TaggedRegistry()

    wf_proxy_reporter = WavefrontProxyReporter(
        host=host, metrics_port=2878, registry=reg,
        source="wavefront-pyformance-example",
        tags={"key1": "val1", "key2": "val2"},
        prefix="python.proxy.").report_minute_distribution()
    wf_direct_reporter = WavefrontDirectReporter(
        server=server, token=token, registry=reg,
        source="wavefront-pyformance-exmaple",
        tags={"key1": "val1", "key2": "val2"},
        prefix="python.direct.").report_minute_distribution()

    # counter
    c1 = reg.counter("foo_count", tags={"counter_key": "counter_val"})
    c1.inc()

    # delta counter
    d1 = delta.delta_counter(reg, "foo_delta_count",
                             tags={"delta_key": "delta_val"})
    d1.inc()
    d1.inc()

    # gauge
    g1 = reg.gauge("foo_gauge", tags={"gauge_key": "gauge_val"})
    g1.set_value(2)

    # meter
    m1 = reg.meter("foo_meter", tags={"meter_key": "meter_val"})
    m1.mark()

    # timer
    t1 = reg.timer("foo_timer", tags={"timer_key": "timer_val"})
    timer_ctx = t1.time()
    time.sleep(3)
    timer_ctx.stop()

    # histogram
    h1 = reg.histogram("foo_histogram", tags={"hist_key": "hist_val"})
    h1.add(1.0)
    h1.add(1.5)

    # Wavefront Histogram
    h2 = wavefront_histogram.wavefront_histogram(reg, "wf_histogram")
    h2.add(1.0)
    h2.add(2.0)

    wf_direct_reporter.report_now()
    wf_direct_reporter.stop()
    wf_proxy_reporter.report_now()
    wf_proxy_reporter.stop()


if __name__ == "__main__":
    # python example.py proxy_host server_url server_token
    host = sys.argv[1]
    server = sys.argv[2]
    token = sys.argv[3]
    while True:
        report_metrics(host, server, token)
        time.sleep(1)
