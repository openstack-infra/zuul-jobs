Mirror the local git repos to remote nodes

This role uses git operations (unlike :zuul:role:`prepare-workspace`
which uses rsync) to mirror the locally prepared git repos to the remote
nodes while taking advantage of cached repos on the node if they exist.
This role works generically regardless of the existence of a cached
repo on the node.

The cached repos need to be placed using the canonical name under the
`cached_repos_root` directory.

**Role Variables**

.. zuul:rolevar:: cached_repos_root
   :default: /opt/git

   The root of the cached repos.
