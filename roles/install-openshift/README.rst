Setup openshift requirements and pull the container images.
The deploy-openshift role can be used to start the services.

This role only works on CentOS.

**Role Variables**

.. zuul:rolevar:: origin_repo
   :default: centos-release-openshift-origin39

   The origin repository.

.. zuul:rolevar:: origin_version
   :default: v3.9.0

   The origin version.
