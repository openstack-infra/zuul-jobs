Download an artifact from a completed build of a Zuul job

Given a change downloads an artifact from a previous build (by default
of the current change) into the work directory.

**Role Variables**

.. zuul:rolevar:: download_artifact_api

   The Zuul API endpoint to use.  Example: ``https://zuul.example.org/api/tenant/{{ zuul.tenant }}``

.. zuul:rolevar:: download_artifact_pipeline

   The pipeline in which the previous build ran.

.. zuul:rolevar:: download_artifact_job

   The job of the previous build.

.. zuul:rolevar:: download_artifact_name

   The artifact name.

.. zuul:rolevar:: download_artifact_query
   :default: change={{ zuul.change }}&patchset={{ zuul.patchset }}&pipeline={{ download_artifact_pipeline }}&job_name={{ download_artifact_job }}

   The query to use to find the build.  This should return exactly one
   result.  Normally the default is used.
