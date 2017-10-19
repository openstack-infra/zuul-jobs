Install a GPG private key onto a host.

**Role Variables**

.. zuul:rolevar:: gpg_key

   Complex argument which contains the GPG private key.  It is
   expected that this argument comes from a `Secret`.

  .. zuul:rolevar:: private

     The ascii-armored contents of the GPG private key.
