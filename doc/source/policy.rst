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

Coding guidelines
-----------------

Role Variable Naming Policy
***************************

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

Support for Multiple Operating Systems
**************************************

Ideally, roles should be able to run regardless of the OS or the distribution
flavor of the host. A role can target a specific OS or distribution; in that case
it should be mentioned in the role's documentation and start with a `fail` task
if the host does not match the intended environment:

.. code-block:: YAML

  tasks:
    - name: Make sure the role is run on XXX version Y
      fail:
        msg: "This role supports XXX version Y only"
        when:
          - ansible_distribution != "XXX"
          - ansible_distribution_major_version != "Y"

Here are a few guidelines to help make roles OS-independent when possible:

* Use the **package** module instead of **yum**, **apt** or other
  distribution-specific commands.
* If more than one specific task is needed for a specific OS, these tasks should
  be stored in a separate YAML file in a `distros` subdirectory and named after
  the specific flavor they target. The following boilerplate code can be used to
  target specific flavors:

.. code-block:: YAML

  tasks:
    - name: Execute distro-specific tasks
      include_tasks: "{{ lookup('first_found', params) }}"
      vars:
        params:
          files:
            - "mytasks-{{ ansible_distribution }}.{{ ansible_distribution_major_version }}.{{ ansible_architecture }}.yaml"
            - "mytasks-{{ ansible_distribution }}.{{ ansible_distribution_major_version }}.yaml"
            - "mytasks-{{ ansible_distribution }}.yaml"
            - "mytasks-{{ ansible_os_family }}.yaml"
            - "mytasks-default.yaml"
          paths:
            - distros

If run on Fedora 29 x86_64, this playbook will attempt to include the first
playbook found among

* `distros/mytasks-Fedora.29.x86_64.yaml`
* `distros/mytasks-Fedora.29.yaml`
* `distros/mytasks-Fedora.yaml`
* `distros/mytasks-RedHat.yaml`
* `distros/mytasks-default.yaml`

The default playbook should return a failure explaining the host's environment is
not supported, or a skip if the tasks were optional.

Handling privileges on hosts
****************************

Zuul offers great freedom in the types and configurations of hosts on which roles
are run. Therefore roles should not assume the amount of privileges they will be
granted on hosts. Some settings may not allow any form of privilege escalation,
meaning that some tasks such as installing packages will fail.

In order to make a role available to as many hosts as possible, it is good practice
to avoid privilege escalations:

* Do not use ``become: yes`` in tasks, unless necessary
* If installing software is required, favor software deployments in user land,
  like virtualenvs, if possible.
* Check before executing a task requiring privilege escalation is actually
  needed (e.g. is the package to install already present, or is the firewall
  rule already set), and make the task skippable if its effects were already
  applied to the host.

If privilege escalation is unavoidable, this should be mentioned in the role's
documentation so that operators can choose or set up their hosts accordingly.
If relevant, the specific steps where the privilege escalation occurs should be
documented so that they can be reproduced when configuring hosts. If possible,
they should be grouped in a separate playbook that can be applied to hosts manually.

Installing Dependencies in Roles
********************************

Roles should be self-sufficient.  This makes it sometimes necessary to pull dependencies
within a role, in order to execute a task. Since this is usually an action
requiring elevated privileges on the host, the guidelines in the previous
paragraph apply. Again, ideally all the installation tasks should be grouped in
a separate playbook.

Here are the ways to install dependencies in order of preference:

* Use the **package** module to install packages
* Manage dependencies with `bindep <https://docs.openstack.org/infra/bindep/readme.html>`__
  and the `bindep` role.
* Use OS-specific tasks like **apt**, **yum** etc. to support as many OSes as
  possible.

In any case, the role's documentation should mention which dependencies are
needed, allowing users to prepare their hosts accordingly.

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
