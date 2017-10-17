Upload python packages to PyPI

**Role Variables**

.. zuul:rolevar:: pypi_info

   Complex argument which contains the information about the PyPI
   server as well as the authentication information needed. It is
   expected that this argument comes from a `Secret`.

  .. zuul:rolevar:: username

     Username to use to log in to PyPI.

  .. zuul:rolevar:: password

     Password to use to log in to PyPI.

  .. zuul:rolevar:: repository
     :default: pypi

     Name of the repository to upload to.

  .. zuul:rolevar:: repository_url
     :default: The built-in twine default for the production pypi.org service.

     URL of the PyPI repostory.

.. zuul:rolevar:: pypi_path
   :default: src/{{ zuul.project.canonical_name }}/dist

   Path containing artifacts to upload.

.. zuul:rolevar:: pypi_twine_executable
   :default: twine

   Path to twine executable.
