Sets three facts based on information in a git repo.

scm_sha
  The short sha found in the repository.

project_ver
  A string describing the project's version. It will either be the value of
  {{ zuul.tag }} or {{ scm_tag }}.{{ commits_since_tag }}.{{ scm_sha }}
  otherwise where ``scm_tag`` is either the most recent tag or the value of
  ``scm_sha`` if there are no commits in the repo.

commits_since_tag
  Number of commits since the most recent tag.

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run git in.
