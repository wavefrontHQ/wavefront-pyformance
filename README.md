# wavefront-pyformance

[![GitHub Actions](https://github.com/wavefrontHQ/wavefront-pyformance/actions/workflows/main.yml/badge.svg)](https://github.com/wavefrontHQ/wavefront-pyformance/actions)
[![PyPI - Version](https://img.shields.io/pypi/v/wavefront-pyformance)](https://pypi.org/project/wavefront-pyformance)
[![PyPI - License](https://img.shields.io/pypi/l/wavefront-pyformance)](https://pypi.org/project/wavefront-pyformance)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/wavefront-pyformance)](https://pypi.org/project/wavefront-pyformance)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/wavefront-pyformance)](https://pypi.org/project/wavefront-pyformance)


This is a plugin for [pyformance](https://github.com/omergertel/pyformance) which adds VMware Aria Operations™ for Applications (formerly known as Wavefront) reporters (via proxy or direct ingestion) and an abstraction that supports tagging at the host level. It also includes support for Wavefront delta counters.

Note: We're in the process of updating the product name to Operations for Applications, but in many places we still refer to it as Wavefront.

## Requirements
Python 3.x are supported.

```
pip install wavefront-pyformance
```

## Usage

### Wavefront Reporter

The Wavefront Reporters support tagging at the host level. If you pass a tag through a reporter, the reporter tags the metrics before sending the metrics to our service.



#### Create a Reporter
You can create a `WavefrontProxyReporter` or `WavefrontDirectReporter` as follows:

```Python
import pyformance
from wavefront_pyformance import wavefront_reporter

reg = pyformance.MetricsRegistry()

# report metrics to a Wavefront proxy every 60s
wf_proxy_reporter = wavefront_reporter.WavefrontProxyReporter(
    host=host,  # required
    port=2878,  # default: 2878
    source='wavefront-pyformance-example',  # default: 'wavefront-pyformance'
    registry=reg,  # default: None
    reporting_interval=60,  # default: 60
    prefix='python.proxy.',  # default: 'proxy.'
    tags={'key1': 'val1',
          'key2': 'val2'},
    enable_runtime_metrics: False,  # default: False
    enable_internal_metrics: True)  # default: True
wf_proxy_reporter.start()

# report metrics directly to a Wavefront server every 60s
wf_direct_reporter = wavefront_reporter.WavefrontDirectReporter(
    server=server,  # required
    token=token,  # required
    source='wavefront-pyformance-example',  # default: 'wavefront-pyformance'
    registry=reg,  # default: None
    reporting_interval=60,  # default: 60
    clock=None,  # default: None
    prefix='python.direct.',  # default: 'direct.'
    tags={'key1': 'val1',
          'key2': 'val2'},  # default: None
    enable_runtime_metrics=False,  # default: False
    enable_internal_metrics=False)  # default: False
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

To enable Python runtime metrics reporting, 
set the `enable_runtime_metrics` flag to `True`:

```Python
    wf_proxy_reporter = wavefront_reporter.WavefrontProxyReporter(
        host=host,
        port=2878,
        registry=reg,
        source='runtime-metric-test',
        tags={'global_tag1': 'val1',
              'global_tag2': 'val2'},
        prefix='python.proxy.',
        enable_runtime_metrics=True).report_minute_distribution()

    wf_direct_reporter = wavefront_reporter.WavefrontDirectReporter(
        server=server,
        token=token,
        registry=reg,
        source='runtime-metric-test',
        tags={'global_tag1': 'val1',
              'global_tag2': 'val2'},
        prefix='python.direct.',
        enable_runtime_metrics=True).report_minute_distribution()
```
