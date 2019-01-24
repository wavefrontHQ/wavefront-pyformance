# -*- coding: utf-8 -*-
"""Delta Counter implementation and helper functions."""

from __future__ import unicode_literals
from pyformance import meters
from pyformance.stats import Snapshot
from wavefront_pyformance.tagged_registry import TaggedRegistry
from wavefront_sdk.entities.histogram import histogram_impl


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

    is_tagged_registry = isinstance(registry, TaggedRegistry)

    try:
        wf_histogram = WavefrontHistogram()
        if is_tagged_registry:
            name = TaggedRegistry.encode_key(name, tags)
        registry.add(name, wf_histogram)
        return wf_histogram
    except LookupError:
        if is_tagged_registry:
            return registry.histogram(name, tags)
        return registry.histogram(name)


class WavefrontHistogram(meters.Histogram):
    def __init__(self, clock_millis=None):
        """
        Construct a delegate Wavefront Histogram.

        @param clock_millis: A function which returns timestamp.
        @type clock_millis: function
        """
        self._delegate = histogram_impl.WavefrontHistogramImpl(clock_millis)

    def add(self, value):
        self._delegate.update(value)
        return self

    def clear(self):
        self._delegate = histogram_impl.WavefrontHistogramImpl()

    def get_count(self):
        return self._delegate.get_count()

    def get_sum(self):
        return self._delegate.get_sum()

    def get_max(self):
        return self._delegate.get_max()

    def get_min(self):
        return self._delegate.get_min()

    def get_mean(self):
        return self._delegate.get_mean()

    def get_stddev(self):
        return self._delegate.std_dev()

    def get_var(self):
        return None

    def get_snapshot(self):
        return Snapshot([0])
