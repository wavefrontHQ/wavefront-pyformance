"""Python Runtime Metrics Collection Class."""

import gc
import multiprocessing
import os
import resource
import threading

import psutil

class Collector(object):
    """Python Runtime Metrics Collection Class."""


    def __init__(self, registry=None):
        """Construct Runtime Metrics Collector."""
        self.registry = registry
        self.pid = os.getpid()
        self.process = psutil.Process(self.pid)
        self.pname = self.process.name()
        self.status = self.process.status()
        self.custom_tags = {"process_id": str(self.pid),
                            "process_name": self.pname,
                            "process_status": self.status}

    def collect_cputimes(self):
        """Collect CPU Times."""
        cputimes = self.process.cpu_times()
        system_cpu = cputimes[1]  # system cpu
        metric1 = self.registry.gauge("cpu.times",
                                      tags=self.custom_tags)
        metric1.set_value(system_cpu)

    def collect_cpupercent(self):
        """Collect CPU in Percentage."""
        cpupercent = self.process.cpu_percent(interval=1)
        metric1 = self.registry.gauge("cpu.percent",
                                      tags=self.custom_tags)
        metric1.set_value(cpupercent)

    def collect_io(self):
        """Collect IO Counters."""
        io_counters = self.process.io_counters()
        read_count = io_counters[0]
        write_count = io_counters[1]
        read_bytes = io_counters[2]
        write_bytes = io_counters[3]
        metric1 = self.registry.gauge("io.read_count",
                                      tags=self.custom_tags)
        metric1.set_value(read_count)
        metric2 = self.registry.gauge("io.write_count",
                                      tags=self.custom_tags)
        metric2.set_value(write_count)
        metric3 = self.registry.gauge("io.read_bytes",
                                      tags=self.custom_tags)
        metric3.set_value(read_bytes)
        metric4 = self.registry.gauge("io.write_bytes",
                                      tags=self.custom_tags)
        metric4.set_value(write_bytes)

    def collect_memoryusage(self):
        """Collect Memory Usage."""
        if resource:
            usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        else:
            usage = self.process.memory_info()[0] / float(2 ** 20)
        metric1 = self.registry.gauge("memory.rss.usage",
                                      tags=self.custom_tags)
        metric1.set_value(usage)

    def collect_memorypercent(self):
        """Collect Memory in Percentage."""
        memorypercent = self.process.memory_percent(memtype="rss")
        metric1 = self.registry.gauge("memory.rss.percent",
                                      tags=self.custom_tags)
        metric1.set_value(memorypercent)

    def collect_threads(self):
        """Collect Threading Metrics."""
        counter = 0
        alive = 0
        daemon = 0
        for thread in threading.enumerate():
            counter += 1
            if thread.isDaemon():
                daemon += 1
            if thread.isAlive():
                alive += 1
        metric1 = self.registry.gauge("thread.count",
                                      tags=self.custom_tags)
        metric1.set_value(counter)
        metric2 = self.registry.gauge("thread.daemon",
                                      tags=self.custom_tags)
        metric2.set_value(daemon)
        metric3 = self.registry.gauge("thread.alive",
                                      tags=self.custom_tags)
        metric3.set_value(alive)

    def collect_garbage(self):
        """Collect Garbage Collection Metrics."""
        (count0, count1, count2) = gc.get_count()
        object_count = len(gc.get_objects())
        referrers_count = len(gc.get_referrers())
        referents_count = len(gc.get_referents())
        metric1 = self.registry.gauge("gc.collection.count0",
                                      tags=self.custom_tags)
        metric1.set_value(count0)
        metric2 = self.registry.gauge("gc.collection.count1",
                                      tags=self.custom_tags)
        metric2.set_value(count1)
        metric3 = self.registry.gauge("gc.collection.count2",
                                      tags=self.custom_tags)
        metric3.set_value(count2)
        metric4 = self.registry.gauge("gc.objects.count",
                                      tags=self.custom_tags)
        metric4.set_value(object_count)
        metric5 = self.registry.gauge("gc.referrers.count",
                                      tags=self.custom_tags)
        metric5.set_value(referrers_count)
        metric6 = self.registry.gauge("gc.referents.count",
                                      tags=self.custom_tags)
        metric6.set_value(referents_count)


    def collect_processes(self):
        """Collect Processes Details."""
        counter = 0
        alive = 0
        daemon = 0
        for proc in multiprocessing.active_children():
            counter += 1
            if proc.is_alive():
                alive += 1
            if proc.daemon:
                daemon += 1
        metric1 = self.registry.gauge("processes.count",
                                      tags=self.custom_tags)
        metric1.set_value(counter)
        metric2 = self.registry.gauge("processes.alive",
                                      tags=self.custom_tags)
        metric2.set_value(alive)
        metric2 = self.registry.gauge("processes.daemon",
                                      tags=self.custom_tags)
        metric2.set_value(daemon)

    def collect_pgfault(self):
        """Collect Page Faults."""
        major_pgfault = resource.getrusage(resource.RUSAGE_SELF).ru_majflt
        minor_pgfault = resource.getrusage(resource.RUSAGE_SELF).ru_minflt
        metric1 = self.registry.gauge("pgfault.major",
                                      tags=self.custom_tags)
        metric1.set_value(major_pgfault)
        metric2 = self.registry.gauge("pgfault.minor",
                                      tags=self.custom_tags)
        metric2.set_value(minor_pgfault)

    def collect_exectime(self):
        """Collect Process Execution Time."""
        utime = resource.getrusage(resource.RUSAGE_SELF).ru_utime
        stime = resource.getrusage(resource.RUSAGE_SELF).ru_stime
        metric1 = self.registry.gauge("exectime.user",
                                      tags=self.custom_tags)
        metric1.set_value(utime)
        metric2 = self.registry.gauge("exectime.kernel",
                                      tags=self.custom_tags)
        metric2.set_value(stime)

    def collect_contextswitches(self):
        """Collect Context Switches."""
        vconsw = resource.getrusage(resource.RUSAGE_SELF).ru_nvcsw
        iconsw = resource.getrusage(resource.RUSAGE_SELF).ru_nivcsw
        metric1 = self.registry.gauge("conswitch.voluntary",
                                      tags=self.custom_tags)
        metric1.set_value(vconsw)
        metric2 = self.registry.gauge("conswitch.involuntary",
                                      tags=self.custom_tags)
        metric2.set_value(iconsw)

    def collect(self):
        """All Collection Wrapper Function."""
        self.collect_cputimes()
        self.collect_cpupercent()
        self.collect_io()
        self.collect_memoryusage()
        self.collect_memorypercent()
        self.collect_garbage()
        self.collect_threads()
        self.collect_processes()
        self.collect_pgfault()
        self.collect_exectime()
        self.collect_contextswitches()
