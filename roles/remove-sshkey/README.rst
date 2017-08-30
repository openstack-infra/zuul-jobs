Remove an added ssh key from the host.

**Role Variables**

.. zuul:rolevar:: ssh_key

  Complex argument which contains the ssh key information. It is
  expected that this argument comes from a `Secret`.

  .. zuul:rolevar:: ssh_known_hosts

    String containing known host signature for the remote host.

  .. zuul:rolevar:: fqdn

    The FQDN of the remote host.
