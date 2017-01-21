from shade import *

#simple_logging(debug=True)
conn = openstack_cloud(cloud='admin')
servers = conn.list_servers()
print len(servers)
#for s in servers:
#    if s.public_v4:
#        print s.name, s.public_v4

ips = conn.list_floating_ips()
print ips[0]
#for ip in ips:
#    project = conn.search_projects(ip.project_id)
#    print ip.floating_ip_address, project[0].name, ip.attached

