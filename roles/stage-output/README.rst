Stage job output on the remote node

Takes as input a dictionary of files/folders named 'zuul_copy_output'.
Copies contents into {{ zuul_output_dir }} on the remote node and is
intended to be used before output fetching in a base job's post-playbook.

**Role Variables**

.. zuul:rolevar:: zuul_copy_output
   :default: None

   Dictionary of files and folders to be staged.

   The input is a dictionary so that it can accumulated via zuul variable
   merging. Keys of the dictionary will be things to copy. Valid values
   describe the type of output to copy:

   * logs
   * artifacts
   * docs
   * null   # ansible null, not the string null

   null overrides the will of a parent job to copy something instructing
   not to copy.

.. zuul:rolevar:: stage_dir
   :default: {{ ansible_user_dir }}

   The stage directory on the remote node.

.. zuul:rolevar:: extensions_to_txt
   :default: null

   A dict of file extensions to be replaced with .txt when staging.
   This can be useful to ensure that text files with an extension not
   registered in the web server may be viewed via browser when uploaded
   to a file server.

   Note that this is only used for files listed directly in
   `zuul_copy_output` and it won't be applied to files contained in
   folders listed in `zuul_copy_output`.

   Example:

     extensions_to_txt:
       conf: True
       log: True
       txt: False

     zuul.conf --(staged as)--> zuul_conf.txt

.. zuul:rolevar:: stage_compress_logs
   :default: True

   When True, files staged as logs will be compressed individually.
