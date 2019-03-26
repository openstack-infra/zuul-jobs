Mirror the local git repos to remote nodes

This role uses git operations (unlike :zuul:role:`prepare-workspace`
which uses rsync) to mirror the local prepared git repos to the remote
nodes.  This may be useful if the remote node already has a copy of
some or all of the git repos.

**Role Variables**

.. zuul:rolevar:: mirror_workspace_quiet
   :default: false

   If `true` git operations will be silenced and won't print every
   changed reference.
