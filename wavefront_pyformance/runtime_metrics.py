"""Python Runtime Metrics Collection Class."""

import gc
import multiprocessing
import os
import threading

import psutil


class RuntimeCollector(object):
    """Python Runtime Metrics Collection Class."""

    # pylint: disable=E0012,R0205

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
        self.registry.gauge("cpu.times",
                            tags=self.custom_tags).set_value(system_cpu)

    def collect_cpupercent(self):
        """Collect CPU in Percentage."""
        cpupercent = self.process.cpu_percent(interval=1)
        self.registry.gauge("cpu.percent",
                            tags=self.custom_tags).set_value(cpupercent)

    def collect_memoryusage(self):
        """Collect Memory Usage."""
        usage = self.process.memory_info()[0] / float(2 ** 20)
        self.registry.gauge("memory.rss.usage",
                            tags=self.custom_tags).set_value(usage)

    def collect_memorypercent(self):
        """Collect Memory in Percentage."""
        memorypercent = self.process.memory_percent(memtype="rss")
        self.registry.gauge("memory.rss.percent",
                            tags=self.custom_tags).set_value(memorypercent)

    def collect_threads(self):
        """Collect Threading Metrics."""
        counter, alive, daemon = 0, 0, 0
        for thread in threading.enumerate():
            counter += 1
            if thread.isDaemon():
                daemon += 1
            if thread.isAlive():
                alive += 1
        self.registry.gauge("thread.count",
                            tags=self.custom_tags).set_value(counter)
        self.registry.gauge("thread.daemon",
                            tags=self.custom_tags).set_value(daemon)
        self.registry.gauge("thread.alive",
                            tags=self.custom_tags).set_value(alive)

    def collect_garbage(self):
        """Collect Garbage Collection Metrics."""
        count0, count1, count2 = gc.get_count()
        object_count = len(gc.get_objects())
        referrers_count = len(gc.get_referrers())
        referents_count = len(gc.get_referents())
        self.registry.gauge("gc.collection.count0",
                            tags=self.custom_tags).set_value(count0)
        self.registry.gauge("gc.collection.count1",
                            tags=self.custom_tags).set_value(count1)
        self.registry.gauge("gc.collection.count2",
                            tags=self.custom_tags).set_value(count2)
        self.registry.gauge("gc.objects.count",
                            tags=self.custom_tags).set_value(object_count)
        self.registry.gauge("gc.referrers.count",
                            tags=self.custom_tags).set_value(referrers_count)
        self.registry.gauge("gc.referents.count",
                            tags=self.custom_tags).set_value(referents_count)

    def collect_processes(self):
        """Collect Processes Details."""
        counter, alive, daemon = 0, 0, 0
        for proc in multiprocessing.active_children():
            counter += 1
            if proc.is_alive():
                alive += 1
            if proc.daemon:
                daemon += 1
        self.registry.gauge("processes.count",
                            tags=self.custom_tags).set_value(counter)
        self.registry.gauge("processes.alive",
                            tags=self.custom_tags).set_value(alive)
        self.registry.gauge("processes.daemon",
                            tags=self.custom_tags).set_value(daemon)

    def collect_contextswitches(self):
        """Collect Context Switches."""
        ctx_switches = self.process.num_ctx_switches()
        voluntary = ctx_switches[0]
        involuntary = ctx_switches[1]
        self.registry.gauge("ctxswitch.voluntary",
                            tags=self.custom_tags).set_value(voluntary)
        self.registry.gauge("ctxswitch.involuntary",
                            tags=self.custom_tags).set_value(involuntary)

    def collect(self):
        """All Collection Wrapper Function."""
        self.collect_cputimes()
        self.collect_cpupercent()
        self.collect_memoryusage()
        self.collect_memorypercent()
        self.collect_garbage()
        self.collect_threads()
        self.collect_processes()
        self.collect_contextswitches()
