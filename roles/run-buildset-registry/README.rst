Runs a docker registry for the use of this buildset.

This may be used for a single job running on a single node, or it may
be used at the root of a job graph so that multiple jobs running for a
single change can share the registry.  Two registry endpoints are
provided -- one is a read-only endpoint which acts as a pull-through
proxy and serves upstream images as well as those which are pushed to
the registry.  The second is intended only for pushing images.

**Role Variables**

.. zuul:rolevar:: buildset_registry_root
   :default: {{ ansible_user_dir }}/buildset_registry

   Path for the registry volumes.

**Return Values**

.. zuul:rolevar:: buildset_registry

   Information about the registry.

   .. zuul:rolevar:: host

      The host (IP address) of the registry.

   .. zuul:rolevar:: port

      The port on which the registry is listening.

   .. zuul:rolevar:: push_host

      The host (IP address) to use when pushing images to the registry.

   .. zuul:rolevar:: push_port

      The port to use when pushing images to the registry.

   .. zuul:rolevar:: username

      The username used to access the registry via HTTP basic auth.

   .. zuul:rolevar:: password

      The password used to access the registry via HTTP basic auth.

   .. zuul:rolevar:: cert

      The (self-signed) certificate used by the registry.
