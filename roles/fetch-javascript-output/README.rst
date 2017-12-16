Collect outputs from a javascript build

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to work in

.. zuul:rolevar:: javascript_content_dir
   :default: dist

   Directory, relative to zuul_work_dir, in which javascript output content
   is to be found.
