Create kerberos / afs tokens

**Role Variables**

.. zuul:rolevar:: afs

  Complex argument which contains the information about authentication
  information. It is expected this argument comes from a `Secret`.

  .. zuul:rolevar:: keytab

    Base64 encoded contents of a keytab file. We'll base64 decode before writing
    it to disk as a temporary file.

  .. zuul:rolevar:: service_name

    The service name to use for kinit command.
