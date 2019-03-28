# -*- coding: utf-8 -*-
"""Delta Counter implementation and helper functions."""

from __future__ import unicode_literals

import pyformance

from wavefront_sdk.entities.histogram import histogram_impl

from . import tagged_registry


def wavefront_histogram(registry, name, tags=None):
    """
    Register a DeltaCounter with the given registry and returns the instance.

    The given name is prefixed with DeltaCounter.DELTA_PREFIX for registering.

    :param registry: the metrics registry to register with
    :param name: the delta counter name
    :return: the registered DeltaCounter instance
    """
    if not name:
        raise ValueError('invalid counter name')

    is_tagged_registry = isinstance(registry, tagged_registry.TaggedRegistry)

    try:
        wf_histogram = WavefrontHistogram()
        if is_tagged_registry:
            name = tagged_registry.TaggedRegistry.encode_key(name, tags)
        registry.add(name, wf_histogram)
        return wf_histogram
    except LookupError:
        if is_tagged_registry:
            return get(name, registry)
        return registry.histogram(name)


def get(name, registry):
    """Get Wavefront Histogram with the given name is in registry.

    This method will return None if given name doesn't exist or is not the type
    of WavefrontHistogram.
    """
    histogram = None
    if isinstance(registry, tagged_registry.TaggedRegistry):
        if registry.has_histogram(name):
            histogram = registry.histogram(name)
    elif name in registry._histograms:  # pylint: disable=protected-access
        histogram = registry.histogram(name)

    return histogram if (histogram and
                         isinstance(histogram, WavefrontHistogram)) else None


class WavefrontHistogram(pyformance.meters.Histogram):
    """Wavefront Histogram Meter."""

    def __init__(self, clock_millis=None):
        """Construct a delegate Wavefront Histogram.

        @param clock_millis: A function which returns timestamp.
        @type clock_millis: function
        """
        super(WavefrontHistogram, self).__init__()
        self._delegate = histogram_impl.WavefrontHistogramImpl(clock_millis)

    def add(self, value):
        """Update the value."""
        self._delegate.update(value)
        return self

    def clear(self):
        """Instantiate brand new WevefrontHistogramImpl()."""
        self._delegate = histogram_impl.WavefrontHistogramImpl()

    def get_count(self):
        """Get Count."""
        return self._delegate.get_count()

    def get_sum(self):
        """Get Sum."""
        return self._delegate.get_sum()

    def get_max(self):
        """Get Max."""
        return self._delegate.get_max()

    def get_min(self):
        """Get Min."""
        return self._delegate.get_min()

    def get_mean(self):
        """Get Mean."""
        return self._delegate.get_mean()

    def get_stddev(self):
        """Get Standard Deviation."""
        return self._delegate.std_dev()

    def get_var(self):
        """Return None."""
        return None

    def get_snapshot(self):
        """Get Snapshot."""
        return pyformance.stats.Snapshot([0])

    def get_distribution(self):
        """Get Distribution."""
        return self._delegate.flush_distributions()
