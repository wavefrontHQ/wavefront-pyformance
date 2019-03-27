# -*- coding: utf-8 -*-
"""Delta Counter implementation and helper functions."""

from __future__ import unicode_literals

import pyformance

from . import tagged_registry


def delta_counter(registry, name, tags=None):
    """Register a DeltaCounter with the given registry.

    The given name is prefixed with
    DeltaCounter.DELTA_PREFIX for registering.

    :param registry: the metrics registry to register with
    :param name: the delta counter name
    :return: the registered DeltaCounter instance
    """
    if not name:
        raise ValueError('invalid counter name')

    name = (name if _has_delta_prefix(name)
            else DeltaCounter.DELTA_PREFIX + name)

    is_tagged_registry = isinstance(registry, tagged_registry.TaggedRegistry)

    try:
        ret_counter = DeltaCounter()
        if is_tagged_registry:
            registry.add(tagged_registry.TaggedRegistry.encode_key(name, tags),
                         ret_counter)
        else:
            registry.add(name, ret_counter)
        return ret_counter
    except LookupError:
        if is_tagged_registry:
            return registry.counter(name, tags)
        return registry.counter(name)


def is_delta_counter(name, registry):
    """Check if a DeltaCounter with the given name is in registry."""
    counter = None
    if isinstance(registry, tagged_registry.TaggedRegistry):
        if registry.has_counter(name):
            counter = registry.counter(name)
    elif name in registry._counters:  # pylint: disable=protected-access
        counter = registry.counter(name)
    return counter and isinstance(counter, DeltaCounter)


def get_delta_name(prefix, name, value_key):
    """Append delta prefix to metric name.

    Return the name of the delta metric name of the form:

        ∆prefix.name.value_key

    """
    return '{}{}.{}'.format(DeltaCounter.DELTA_PREFIX + prefix, name[1:],
                            value_key)


def _has_delta_prefix(name):
    """Check if name starts with any of two allowed delta prefixes."""
    return name and (name.startswith(DeltaCounter.DELTA_PREFIX)
                     or name.startswith(DeltaCounter.ALT_DELTA_PREFIX))


class DeltaCounter(pyformance.meters.Counter):
    """A counter for Wavefront delta metrics.

    Differs from a counter in that it is reset in the WavefrontReporter
    every time the value is reported.
    """

    DELTA_PREFIX = u'\u2206'  # '∆'
    ALT_DELTA_PREFIX = u'\u0394'  # 'Δ'
