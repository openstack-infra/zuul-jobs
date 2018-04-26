Deprecation Policy
==================

Because `zuul-jobs` is intended for wide use by any Zuul, we try to
take care when making backwards incompatible changes.

If we need to do so, we will send a notice to the `zuul-announce`_
mailing list describing the change and indicating when it will be
merged.  We will usually wait at least two weeks between sending the
announcement and merging the change.

If the change affects your jobs, and you are unable to adjust to it
within the timeframe, please let us know with a message to the
`zuul-discuss`_ mailing list -- we may be able to adjust the
timeframe.  Otherwise, you may wish to temporarily switch to a local
fork of `zuul-jobs` (or stop updating it if you already have).

New Zuul Features
-----------------

When a new feature is available in Zuul, the jobs in `zuul-jobs` may
not be able to immediately take advantage of it.  We need to allow
time for folks to upgrade their Zuul installations so they will be
compatible with the change.  In these cases, we will wait four weeks
after the first Zuul release with the required feature before merging
a change to `zuul-jobs` which uses it.

Deprecated Zuul Features
------------------------

Before deprecating a feature in Zuul which is used by `zuul-jobs`, the
usage of the feature must be removed from `zuul-jobs` according to the
deprecation policy described above.

.. _zuul-announce: http://lists.zuul-ci.org/cgi-bin/mailman/listinfo/zuul-announce
.. _zuul-discuss: http://lists.zuul-ci.org/cgi-bin/mailman/listinfo/zuul-discuss

