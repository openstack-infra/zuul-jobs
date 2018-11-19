Prepare an archive containing all repositories that are part of the job. This
can be used to prepare the repos archive suitable for caching in the node
image to be used by `prepare-workspace-git`.

The path to the resulting archive file will be stored in the `git_cache_file`
variable. That variable can be used to push the archive to a place where
it will be picked up to be baked into the node image.

**Role variables**

.. zuul:rolevar:: git_cache_root
   :default: {{ansible_user_dir }}/git-cache"

   Directory where the git cache should be prepared. Usually this should not
   be changed.
