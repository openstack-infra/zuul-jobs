Upload javascript packages to npm

**Role Variables**

.. zuul:rolevar:: npm_credentials

   Complex argument which contains the information about the npm
   server as well as the authentication information needed.
   It is expected that this argument comes from a `Secret`.
   This role expects to be run on the executor.

  .. zuul:rolevar:: username

     Username to use to log in to npm.

  .. zuul:rolevar:: password

     Password to use to log in to npm.

  .. zuul:rolevar:: email

     Email associated with the npm account.

  .. zuul:rolevar:: author_name

     npm author name.

  .. zuul:rolevar:: author_url

     npm author url.

  .. zuul:rolevar:: author_email

     npm author email.

  .. zuul:rolevar:: registry_url
     :default: //registry.npmjs.org

     URL of npm registry server.
