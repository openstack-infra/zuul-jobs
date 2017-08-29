Add launchpadlib credentials and launchpadlib to a host

**Role Variables**

.. zuul:rolevar:: lp_creds

   Complex argument which contains the information needed to log in
   to Launchpad. It is expected that this argument comes from a `Secret`.

  .. zuul:rolevar:: access_token

     Launchpad access token

  .. zuul:rolevar:: access_secret

     Launchpad access secret

  .. zuul:rolevar:: consumer_key

     Launchpad consumer key
