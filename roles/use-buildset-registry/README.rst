Adds a buildset registry to the docker configuration.

Use this role on any host which should use the buildset registry.

**Role Variables**

.. zuul:rolevar:: buildset_registry

   Information about the registry, as returned by
   :zuul:role:`run-buildset-registry`.

   .. zuul:rolevar:: host

      The host (IP address) of the registry.

   .. zuul:rolevar:: port

      The port on which the registry is listening.

   .. zuul:rolevar:: username

      The username used to access the registry via HTTP basic auth.

   .. zuul:rolevar:: password

      The password used to access the registry via HTTP basic auth.

   .. zuul:rolevar:: cert

      The (self-signed) certificate used by the registry.
