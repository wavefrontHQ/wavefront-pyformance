from unittest import TestCase
import unittest
from pyformance import MetricsRegistry
from wavefront_pyformance import delta


class TestDelta(TestCase):
    def test_delta_counter(self):
        reg = MetricsRegistry()
        counter = delta.delta_counter(reg, "foo")
        assert(isinstance(counter, delta.DeltaCounter))

        # test duplicate (should return previously registered counter)
        duplicate_counter = delta.delta_counter(reg, "foo")
        assert(counter == duplicate_counter)
        assert(delta.is_delta_counter(delta.DeltaCounter.DELTA_PREFIX + "foo", reg))

        different_counter = delta.delta_counter(reg, "foobar")
        assert(counter != different_counter)

    def test_has_delta_prefix(self):
        assert(delta._has_delta_prefix(delta.DeltaCounter.DELTA_PREFIX + "foo")) # valid prefix
        assert(delta._has_delta_prefix(delta.DeltaCounter.ALT_DELTA_PREFIX + "foo")) # valid prefix
        assert(delta._has_delta_prefix("foo") is False) # invalid prefix

    def test_get_delta_name(self):
        d = delta.get_delta_name('delta.prefix', delta.DeltaCounter.DELTA_PREFIX + 'foo', 'count')
        assert(d.startswith(delta.DeltaCounter.DELTA_PREFIX))


if __name__ == '__main__':
    # run 'python -m unittest discover' from toplevel to run tests
    unittest.main()
