# wavefront-pyformance [![travis build status](https://travis-ci.com/wavefrontHQ/wavefront-pyformance.svg?branch=master)](https://travis-ci.com/wavefrontHQ/wavefront-pyformance)

This is a plugin for [pyformance](https://github.com/omergertel/pyformance) which adds Wavefront reporters (via proxy or direct ingestion) and an abstraction that supports tagging at the host level. It also includes support for Wavefront delta counters.

## Requirements
Python 2.7+ and Python 3.x are supported.

```
pip install wavefront-pyformance
```

## Usage

### Wavefront Reporter

The Wavefront Reporters support tagging at the host level. Tags passed to a reporter will be applied to every metric before being sent to Wavefront.

You can create a `WavefrontProxyReporter` or `WavefrontDirectReporter`:

```Python
from pyformance import MetricsRegistry
from wavefront_pyformance.wavefront_reporter import WavefrontProxyReporter, WavefrontDirectReporter

reg = MetricsRegistry()

# report metrics to a Wavefront proxy every 10s
wf_proxy_reporter = WavefrontProxyReporter(host=host, port=2878, registry=reg,
                                           source="wavefront-pyformance-example",
                                           tags={"key1":"val1", "key2":"val2"},
                                           prefix="python.proxy.",
                                           reporting_interval=10)
wf_proxy_reporter.start()

# report metrics directly to a Wavefront server every 10s
wf_direct_reporter = WavefrontDirectReporter(server=server, token=token, registry=reg,
                                             source="wavefront-pyformance-exmaple",
                                             tags={"key1":"val1", "key2": "val2"},
                                             prefix="python.direct.",
                                             reporting_interval=10)
wf_direct_reporter.start()
```

### Delta Counter

To create a Wavefront delta counter:

```Python
from pyformance import MetricsRegistry
from wavefront_pyformance import delta

reg = MetricsRegistry()
d1 = delta.delta_counter(reg, "requests_delta")
d1.inc(10)
```

Note: Having the same metric name for any two types of metrics will result in only one time series at the server and thus cause collisions.
In general, all metric names should be different. In case you have metrics that you want to track as both a Counter and Delta Counter, consider adding a relevant suffix to one of the metrics to differentiate one metric name from another.
