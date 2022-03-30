openstack user create --password admin admin
openstack user create --password nova nova
openstack user create --password glance glance
openstack user create --password demo demo
openstack user create --password neutron neutron
openstack user create --password cinder cinder

openstack group create admin
openstack group create premium
openstack group create standard

openstack role create admin
openstack role create reader

openstack group add user admin admin
openstack group add user premium admin
openstack group add user standard admin
openstack group add user premium nova
openstack group add user standard nova
openstack group add user premium glance
openstack group add user standard glance
openstack group add user standard demo
openstack group add user standard neutron
openstack group add user standard cinder

openstack project create admin
openstack project create nova
openstack project create glance
openstack project create demo
openstack project create neutron
openstack project create cinder
openstack project create public

openstack role add --group admin --project admin admin
openstack role add --group admin --project admin reader
openstack role add --group admin --project nova admin
openstack role add --group admin --project nova reader
openstack role add --group admin --project glance admin
openstack role add --group admin --project glance reader
openstack role add --group admin --project demo admin
openstack role add --group admin --project demo reader
openstack role add --group admin --project cinder admin
openstack role add --group admin --project cinder reader
openstack role add --group admin --project neutron admin
openstack role add --group admin --project neutron reader
openstack role add --group premium --project public admin
openstack role add --group premium --project public reader
openstack role add --group standard --project public reader

openstack role add --user admin --project admin admin
openstack role add --user admin --project admin reader
openstack role add --user nova --project nova admin
openstack role add --user nova --project nova reader
openstack role add --user glance --project glance admin
openstack role add --user glance --project glance reader
openstack role add --user demo --project demo reader
openstack role add --user cinder --project cinder reader
openstack role add --user neutron --project neutron reader