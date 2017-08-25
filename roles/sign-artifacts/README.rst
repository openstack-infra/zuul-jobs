Sign artifacts

**Role Variables**

.. zuul:rolevar:: gpg_key

   Complex argument which contains the GPG public and secret keyrings
   for signing the artifacts. It is expected that this argument comes
   from a `Secret`.

  .. zuul:rolevar:: public

     The ascii-armored contents of the GPG public key.

  .. zuul:rolevar:: private

     The ascii-armored contents of the GPG private key.

.. zuul:rolevar:: gpg_artifact_path
   :default: "{{ zuul.executor.work_root }}/artifacts/"

   Path to a directory containing artifacts to sign.
