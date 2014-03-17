# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

"""
Benchmark a function for its behavior with respect to N.

How to use this module:

1. Define a function which runs the code that you want to benchmark. The
function takes a single argument which is the size of the task (i.e. the "N"
parameter). Pass this function as the first argument to rep_bench(), and N as
the second, e.g.:

>>> from pyutil.benchutil import rep_bench
>>> def fib(N):
...  if N <= 1:
...   return 1
...  else:
...   return fib(N-1) + fib(N-2)
...
>>> rep_bench(fib, 25, UNITS_PER_SECOND=1000)
best: 1.968e+00,   3th-best: 1.987e+00, mean: 2.118e+00,   3th-worst: 2.175e+00, worst: 2.503e+00 (of     10)

The output is reporting the number of milliseconds that executing the
function took, divided by N, from ten different invocations of
fib(). It reports the best, worst, M-th best, M-th worst, and mean,
where "M" is 1/4 of the number of invocations (in this case 10).

2. Now run it with different values of N and look for patterns:

>>> for N in 1, 5, 9, 13, 17, 21:
...  print "%2d" % N,
...  rep_bench(fib, N, UNITS_PER_SECOND=1000000)
...
 1 best: 9.537e-01,   3th-best: 9.537e-01, mean: 1.121e+00,   3th-worst: 1.192e+00, worst: 2.146e+00 (of     10)
 5 best: 5.722e-01,   3th-best: 6.199e-01, mean: 7.200e-01,   3th-worst: 8.106e-01, worst: 8.106e-01 (of     10)
 9 best: 2.437e+00,   3th-best: 2.464e+00, mean: 2.530e+00,   3th-worst: 2.570e+00, worst: 2.676e+00 (of     10)
13 best: 1.154e+01,   3th-best: 1.168e+01, mean: 5.638e+01,   3th-worst: 1.346e+01, worst: 4.478e+02 (of     10)
17 best: 6.230e+01,   3th-best: 6.247e+01, mean: 6.424e+01,   3th-worst: 6.460e+01, worst: 7.294e+01 (of     10)
21 best: 3.376e+02,   3th-best: 3.391e+02, mean: 3.521e+02,   3th-worst: 3.540e+02, worst: 3.963e+02 (of     10)
>>> print_bench_footer(UNITS_PER_SECOND=1000000)
all results are in time units per N
time units per second: 1000000; seconds per time unit: 0.000001

(The pattern here is that as N grows, the time per N grows.)

2. If you need to do some setting up before the code can run, then put the
setting-up code into a separate function so that it won't be included in the
timing measurements. A good way to share state between the setting-up function
and the main function is to make them be methods of the same object, e.g.:

>>> import random
>>> class O:
...  def __init__(self):
...   self.l = []
...  def setup(self, N):
...   del self.l[:]
...   self.l.extend(range(N))
...   random.shuffle(self.l)
...  def sort(self, N):
...   self.l.sort()
...
>>> o = O()
>>> for N in 1000, 10000, 100000, 1000000:
...  print "%7d" % N,
...  rep_bench(o.sort, N, o.setup)
...
   1000 best: 4.830e+02,   3th-best: 4.950e+02, mean: 5.730e+02,   3th-worst: 5.858e+02, worst: 7.451e+02 (of     10)
  10000 best: 6.342e+02,   3th-best: 6.367e+02, mean: 6.678e+02,   3th-worst: 6.851e+02, worst: 7.848e+02 (of     10)
 100000 best: 8.309e+02,   3th-best: 8.338e+02, mean: 8.435e+02,   3th-worst: 8.540e+02, worst: 8.559e+02 (of     10)
1000000 best: 1.327e+03,   3th-best: 1.339e+03, mean: 1.349e+03,   3th-worst: 1.357e+03, worst: 1.374e+03 (of     10)

3. Useful fact! rep_bench() returns a dict containing the numbers.

4. Things to fix:

 a. I used to have it hooked up to use the "hotshot" profiler on the
 code being measured. I recently tried to change it to use the newer
 cProfile profiler instead, but I don't understand the interface to
 cProfiler so it just gives an exception if you pass
 profile=True. Please fix this and send me a patch. xxx change it to
 statprof

 b. Wouldn't it be great if this script emitted results in a json format that
 was understood by a tool to make pretty interactive explorable graphs? The
 pretty graphs could look like those on http://speed.pypy.org/ . Please make
 this work and send me a patch!
"""

import cProfile, operator, time
from decimal import Decimal as D
import thread

#from pyutil import jsonutil as json

import platform
if 'windows' in platform.system().lower():
    clock = time.clock
else:
    clock = time.time

from assertutil import _assert

def makeg(func):
    def blah(n, func=func):
        for i in xrange(n):
            func()
    return blah

def to_decimal(x):
    """
    See if D(x) returns something. If instead it raises TypeError, x must have been a float, so convert it to Decimal by way of string. (In Python >= 2.7, D(x) does this automatically.
    """
    try:
        return D(x)
    except TypeError:
        return D("%0.54f" % (x,))

def mult(a, b):
    """
    If we get TypeError from * (possibly because one is float and the other is Decimal), then promote them both to Decimal.
    """
    try:
        return a * b
    except TypeError:
        return to_decimal(a) * to_decimal(b)

def _measure_empty_func_with_runtime(profile=False):
    return  _bench_it_until_time(do_nothing, 2**32, runtime=0.03)

def _measure_empty_func_with_reps(profile=False):
    return  _bench_it_until_reps(do_nothing, 2**32, runreps=1000)

def rep_bench(func, n, runtime=None, initfunc=None, runreps=None, runiters=10, profile=False, profresults="pyutil-benchutil.prof", UNITS_PER_SECOND=1, quiet=False):
    """
    @param quiet Don't print anything--just return the results dict.
    @param runtime How many seconds to run the inner loop (for measuring the time of the code-under-measurement). If None then do it runreps times regardless of how many seconds it takes.
    @param runreps How many times to run the inner loop (for measuring the time of the code-under-measurement). If None then do it until runtime seconds have passed.
    @param runiters How many times to run the outer loop (for generating statistics about the distribution of runtimes of the code-under-measurement).
    """
    assert isinstance(n, int), (n, type(n))
    assert (runtime is None) != (runreps is None), "Choose either runtime mode or runreps mode. runtime: %s, runreps: %s" % (runtime, runreps,)

    global worstemptymeasure
    if runtime is not None:
        (time_per_rep, reps) = _measure_empty_func_with_runtime(profile=profile)
        if time_per_rep * MARGINOFERROR >= runtime:
            raise BadMeasure("Apparently simply invoking an empty Python function can take as long as %0.10f seconds, and we were running reps for only about %0.10f seconds. So the measurement of the runtime of the code under benchmark is not reliable. Please pass a higher number for the 'runtime' argument to rep_bench().")
    else:
        (time_per_rep, reps) = _measure_empty_func_with_reps(profile=profile)
        if (worstemptymeasure is None) or (time_per_rep > worstemptymeasure):
            worstemptymeasure = time_per_rep

    tls = [] # (elapsed time per rep in seconds, numreps)
    while len(tls) < runiters:
        if initfunc:
            initfunc(n)
        if profile:
            import statprof
            statprof.start()
            try:
                tl, reps = bench_it(func, n, runtime=runtime, runreps=runreps)
            finally:
                statprof.stop()
        else:
            tl, reps = bench_it(func, n, runtime=runtime, runreps=runreps)
        tls.append((tl, reps))
    sumtls = sum([tl for (tl, reps) in tls])
    mean = sumtls / len(tls)
    tls.sort()
    worst = tls[-1][0]
    best = tls[0][0]

    if best < (worstemptymeasure * MARGINOFERROR):
        raise BadMeasure("Apparently simply invoking an empty Python function can take as long as %0.10f seconds, and we were running reps for only about %0.10f seconds. So the measurement of the runtime of the code under benchmark is not reliable. Please pass a higher number for the 'runtime' argument to rep_bench().")

    m = len(tls)/4
    if m > 0:
        mthbest = tls[m-1][0]
        mthworst = tls[-m][0]
    else:
        mthbest = tls[0][0]
        mthworst = tls[-1][0]

    # The +/-0 index is the best/worst, the +/-1 index is the 2nd-best/worst,
    # etc, so we use mp1 to name it.
    mp1 = m+1
    res = {
        'worst': mult(worst, UNITS_PER_SECOND)/n,
        'best': mult(best, UNITS_PER_SECOND)/n,
        'mp1': mp1,
        'mth-best': mult(mthbest, UNITS_PER_SECOND)/n,
        'mth-worst': mult(mthworst, UNITS_PER_SECOND)/n,
        'mean': mult(mean, UNITS_PER_SECOND)/n,
        'num': len(tls),
        }

    if not quiet:
        print "best: %(best)#8.03e, %(mp1)3dth-best: %(mth-best)#8.03e, mean: %(mean)#8.03e, %(mp1)3dth-worst: %(mth-worst)#8.03e, worst: %(worst)#8.03e (of %(num)6d)" % res

    return res

MARGINOFERROR = 10

worstemptymeasure = 0

class BadMeasure(Exception):
    """ Either the clock wrapped (which happens with time.clock()) or
    it went backwards (which happens with time.time() on rare
    occasions), or the code being measured completed too fast to
    accurately measure. """
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.msg)

    def __str__(self):
        return self.__repr__()

def do_nothing(n):
    pass

def _interrupt_me_later(delay):
    time.sleep(delay)
    thread.interrupt_main()

def _bench_it_until_time(func, n, runtime=1.0):
    reps = 0
    st = clock()

    # We run it once before starting the timer so that we'll have a
    # resulting measurement, even if interrupted before we finish the
    # first interruptible run.
    func(n)
    reps += 1
    sto = clock()

    try:
        timer_thread =  thread.start_new_thread(_interrupt_me_later, (runtime,))
        while True:
            func(n)
            reps += 1
            sto = clock()
    except KeyboardInterrupt:
        timeelapsed = sto - st
        if timeelapsed <= 0:
            raise BadMeasure("timeelapsed: %s, reps: %s" % (timeelapsed, reps))
        return (timeelapsed / reps, reps)

def _bench_it_until_reps(func, n, runreps=1000):
    st = clock()
    for i in range(runreps):
        func(n)
    sto = clock()
    timeelapsed = sto - st
    if timeelapsed <= 0:
        raise BadMeasure("timeelapsed: %s, runreps: %s" % (timeelapsed, runreps))
    return (timeelapsed / runreps, runreps)

def bench_it(func, n, runtime=1.0, runreps=None):
    assert (runtime is None) != (runreps is None), "Choose either runtime mode or runreps mode. runtime: %s, runreps: %s" % (runtime, runreps,)

    if runtime is not None:
        return _bench_it_until_time(func, n, runtime=runtime)
    else:
        return _bench_it_until_reps(func, n, runreps=runreps)

def bench(func, initfunc=None, runtime=1.0, TOPXP=21, profile=False, profresults="pyutil-benchutil.prof", outputjson=False, jsonresultsfname="pyutil-benchutil-results.json", UNITS_PER_SECOND=1):
    BSIZES = []
    for i in range(TOPXP-6, TOPXP+1, 2):
        n = int(2 ** i)
        if n < 1:
            n = 1
        if BSIZES and n <= BSIZES[-1]:
            n *= 2
        BSIZES.append(n)

    res = {}
    for BSIZE in BSIZES:
        print "N: %7d," % BSIZE,
        r = rep_bench(func, BSIZE, initfunc=initfunc, runtime=runtime, profile=profile, profresults=profresults, UNITS_PER_SECOND=UNITS_PER_SECOND)
        res[BSIZE] = r

    #if outputjson:
    #    write_file(jsonresultsfname, json.dumps(res))

    return res

def print_bench_footer(UNITS_PER_SECOND=1):
    print "all results are in time units per N"
    print "time units per second: %s; seconds per time unit: %s" % (UNITS_PER_SECOND, D(1)/UNITS_PER_SECOND)
