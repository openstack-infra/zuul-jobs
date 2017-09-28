Remove sudo access for the Zuul user.

If the file ``/etc/sudoers.d/zuul`` exists, then it will be
removed.  This is to facilitate systems which may use the same image
for tests which require sudo and those which do not.

This role also asserts that sudo access has been removed and will
fail if it has not.
