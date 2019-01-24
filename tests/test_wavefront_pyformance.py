from unittest import TestCase
import unittest
from wavefront_pyformance.tagged_registry import TaggedRegistry
from wavefront_pyformance import delta, wavefront_histogram


class TestDelta(TestCase):
    def test_delta_counter(self):
        reg = TaggedRegistry()
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

    def test_wavefront_histogram(self):
        reg = TaggedRegistry()
        pyformance_hist = reg.histogram("pyformance_hist").add(1.0)
        wavefront_hist = wavefront_histogram.wavefront_histogram(
            reg, "wavefront_hist").add(2.0)
        assert(isinstance(wavefront_hist,
                          wavefront_histogram.WavefrontHistogram))


if __name__ == '__main__':
    # run 'python -m unittest discover' from toplevel to run tests
    unittest.main()
