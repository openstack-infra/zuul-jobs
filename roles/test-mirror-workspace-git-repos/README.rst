Mirror the local git repos to remote nodes

This role uses git operations (unlike :zuul:role:`prepare-workspace`
which uses rsync) to mirror the local prepared git repos to the remote
nodes.  This may be useful if the remote node already has a copy of
some or all of the git repos.
