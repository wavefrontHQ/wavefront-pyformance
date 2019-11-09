# wavefront-pyformance

[![image](https://img.shields.io/pypi/v/wavefront-pyformance.svg)](https://pypi.org/project/wavefront-pyformance/)
[![image](https://img.shields.io/pypi/l/wavefront-pyformance.svg)](https://pypi.org/project/wavefront-pyformance/)
[![image](https://img.shields.io/pypi/pyversions/wavefront-pyformance.svg)](https://pypi.org/project/wavefront-pyformance/)
[![travis build status](https://travis-ci.com/wavefrontHQ/wavefront-pyformance.svg?branch=master)](https://travis-ci.com/wavefrontHQ/wavefront-pyformance)


This is a plugin for [pyformance](https://github.com/omergertel/pyformance) which adds Wavefront reporters (via proxy or direct ingestion) and an abstraction that supports tagging at the host level. It also includes support for Wavefront delta counters.

## Requirements
Python 2.7+ and Python 3.x are supported.

```
pip install wavefront-pyformance
```

## Usage

### Wavefront Reporter

The Wavefront Reporters support tagging at the host level. Tags passed to a reporter will be applied to every metric before being sent to Wavefront.

#### Create Wavefront Reporter
You can create a `WavefrontProxyReporter` or `WavefrontDirectReporter` as follows:

```Python
import pyformance
from wavefront_pyformance import wavefront_reporter

reg = pyformance.MetricsRegistry()

# report metrics to a Wavefront proxy every 60s
wf_proxy_reporter = wavefront_reporter.WavefrontProxyReporter(
    host=host, port=2878, registry=reg,
    source='wavefront-pyformance-example',
    tags={'key1': 'val1', 'key2': 'val2'},
    prefix='python.proxy.',
    reporting_interval=60)
wf_proxy_reporter.start()

# report metrics directly to a Wavefront server every 60s
wf_direct_reporter = wavefront_reporter.WavefrontDirectReporter(
    server=server, token=token, registry=reg,
    source='wavefront-pyformance-exmaple',
    tags={'key1': 'val1', 'key2': 'val2'},
    prefix='python.direct.',
    reporting_interval=60)
wf_direct_reporter.start()
```
#### Flush and stop Wavefront Reporter
 After create Wavefront Reporter, `start()` will make the reporter automatically reporting every `reporting_interval` seconds.
 Besides that, you can also call `report_now()` to perform reporting immediately.
 ```Python
# Report immediately
wf_reporter.report_now()

# Stop Wavefront Reporter
wf_reporter.stop()
```

### Delta Counter

To create a Wavefront delta counter:

```Python
import pyformance
from wavefront_pyformance import delta

reg = pyformance.MetricsRegistry()
d_0 = delta.delta_counter(reg, 'requests_delta')
d_0.inc(10)
```

Note: Having the same metric name for any two types of metrics will result in only one time series at the server and thus cause collisions.
In general, all metric names should be different. In case you have metrics that you want to track as both a Counter and Delta Counter, consider adding a relevant suffix to one of the metrics to differentiate one metric name from another.

### Wavefront Histogram

To create a [Wavefront Histogram](https://docs.wavefront.com/proxies_histograms.html):

```Python
import pyformance
from wavefront_pyformance import wavefront_histogram

reg = pyformance.MetricsRegistry()
h_0 = wavefront_histogram.wavefront_histogram(reg, 'requests_duration')
h_0.add(10)
```

### Python Runtime Metrics

To enable Python runtime metrics reporting, set the `enable_runtime_metrics` flag to True:

```Python
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
        enable_runtime_metrics=True).report_minute_distribution()
```
