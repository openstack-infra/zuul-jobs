Pull artifacts from the intermediate registry

This role will pull any artifacts built for changes ahead of this
change which have been placed in an intermediate registry into the
buildset registry for this buildset.

Run this in a trusted pre-playbook at the start of a job (which, in
the case of multiple dependent jobs in a buildset, should be at the
root of the job dependency graph).

This requires the :zuul:role:`run-buildset-registry` role already
applied.  It also requires an externally managed "intermediate"
registry operating for the use of Zuul, and it requires "skopeo" to be
installed on the Zuul executors.

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

.. zuul:rolevar:: intermediate_registry

   Information about the registry.  This is expected to be provided as
   a secret.

   .. zuul:rolevar:: host

      The host (IP address) of the registry.

   .. zuul:rolevar:: port

      The port on which the registry is listening.

   .. zuul:rolevar:: username

      The username used to access the registry via HTTP basic auth.

   .. zuul:rolevar:: password

      The password used to access the registry via HTTP basic auth.
