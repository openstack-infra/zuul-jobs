Configures a VXLAN virtual network overlay through an openvswitch network
bridge between a 'switch' node and 'peer' nodes.

This allows members of the bridge to communicate with each other through the
virtual network.

By default, this role will:

- Install and start ``openvswitch``
- Set up a ``br-infra`` bridge on all nodes
- Set up the connectivity between the switch and the peer with a virtual port
- Set up an ip address on the bridge interface:

::

    172.24.4.1/23 # switch node
    172.41.4.2/23 # first peer
    172.41.4.3/23 # second peer
    ...

**Role requirements**

This role requires and expects two groups to be set up in the Ansible host
inventory in order to work:

- ``switch`` (the node acting as the switch)
- ``peers`` (nodes connected to the virtual switch ports)

**Role variables**

.. zuul:rolevar:: bridge_vni_offset
   :default: 1000000

   VXLAN Network Identifier offset (openvswitch key).

.. zuul:rolevar:: bridge_mtu
   :default: 1450

   Bridge interface MTU.

.. zuul:rolevar:: bridge_name
   :default: br-infra

   Name of the bridge interface.

.. zuul:rolevar:: bridge_configure_address
   :default: true

   Whether or not to configure an IP address on the bridge interface.

.. zuul:rolevar:: bridge_authorize_internal_traffic
   :default: false

   When ``bridge_configure_address`` is ``true``, whether or not to set up
   firewall rules in order to allow traffic to flow freely within the bridge
   subnet (``bridge_address_prefix``.0/``bridge_address_subnet``).

.. zuul:rolevar:: bridge_address_prefix
   :default: 172.24.4

   The IP address range prefix.

.. zuul:rolevar:: bridge_address_offset
   :default: 1

   The IP address offset, used with ``bridge_address_prefix`` to provide the
   full IP address. The initial offset defines the IP address of the switch
   node in the virtual network.

.. zuul:rolevar:: bridge_address_subnet
   :default: 23

   The IP address range CIDR/subnet.
