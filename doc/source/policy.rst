Policy
======

Below are some guidelines for developers contributing to `zuul-jobs`.

.. contents::
   :local:

Deprecation Policy
------------------

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
*****************

When a new feature is available in Zuul, the jobs in `zuul-jobs` may
not be able to immediately take advantage of it.  We need to allow
time for folks to upgrade their Zuul installations so they will be
compatible with the change.  In these cases, we will wait four weeks
after the first Zuul release with the required feature before merging
a change to `zuul-jobs` which uses it.

Deprecated Zuul Features
************************

Before deprecating a feature in Zuul which is used by `zuul-jobs`, the
usage of the feature must be removed from `zuul-jobs` according to the
deprecation policy described above.

Python Version Policy
---------------------

``zuul-jobs`` targets Python 2.7 onwards and Python 3.5 onwards (note
this differs slightly from Ansible upstream, where the policy is 2.6
onwards unless libraries depend on newer features.  `zuul-jobs` does
not support Python 2.6).

Library code should be written to be compatible with both.  There are
some tips on this in `Ansible and Python 3
<https://docs.ansible.com/ansible/2.5/dev_guide/developing_python_3.html>`__.

Role Variable Naming Policy
---------------------------

Variables referenced by roles from global scope (often intended to be
set via ``host_vars`` and ``group_vars``, but also set during role
inclusion) must be namespaced by prepending their role-name to the
variable.  Thus ``example-role`` would have variables with names such
as ``example_role_variable``; e.g.

.. code-block:: yaml

  tasks:
    - name: Call "example" role
      include_role:
        name: example-role
      vars:
        example_role_variable: 'something'

Testing
-------

`zuul-jobs` is often consumed from the master branch and many parts of
`zuul-jobs` are involved in base setup.  Thus bad changes have a
larger than usual potential to quickly produce global problems.
Demonstrated testing of changes is very important and is requested of
all proposed changes.

Since many roles in `zuul-jobs` are run from trusted jobs that run
directly on the executor, often changes are not self-testing.  In such
cases, it may be possible to demonstrate sufficient testing via
external methods.  This should be noted carefully in the review.

To use the OpenStack gate, you should develop your change as usual
with as much testing as possible.  Once you have pushed the main
review, you should clone the changes to the role being tested to a
``test-<rolename>`` role in a new change (there may already be a
``test-<rolename>`` if someone has done this before you; in this case,
update it with your change).  Then rebase this testing change *before*
your main change (the commit message should say something along the
lines of "This change is for pre-testing of change I...").

Reviewers can commit this change without affecting production jobs.
You then need to look at the ``playbooks/base-test/`` files in
``project-config`` and make sure they are using the
``test-<rolename>`` role, which should now be committed (in some
cases, if it has been done before, it may already be; otherwise
propose a change to swap the role in ``base-test`` that Depends-On
your ``test-<rolename>`` addition).  You can then reparent a
do-not-merge job to ``base-test`` and your changes will be executed.

After this, the actual change can be merged.  Note that after this,
the ``test-<rolename>`` and ``<rolename>`` roles will be identical,
which is how it should remain until the next proposed change.

.. _zuul-announce: http://lists.zuul-ci.org/cgi-bin/mailman/listinfo/zuul-announce
.. _zuul-discuss: http://lists.zuul-ci.org/cgi-bin/mailman/listinfo/zuul-discuss

