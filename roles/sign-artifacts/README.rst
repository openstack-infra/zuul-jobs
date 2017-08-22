Sign artifacts

**Role Variables**

.. zuul:rolevar:: gpg_key

   Complex argument which contains the GPG public and secret keyrings
   for signing the artifacts. It is expected that this argument comes
   from a `Secret`.

  .. zuul:rolevar:: pubring

     The binary contents of the GPG pubring.

  .. zuul:rolevar:: secring

     The binary contents of the GPG secring.

.. zuul:rolevar:: gpg_artifact_path
   :default: "{{ zuul.executor.work_root }}/artifacts/"

   Path to a directory containing artifacts to sign.
