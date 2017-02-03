import json
from subprocess import call,check_output


def get_property(properties, key):
    #import pdb; pdb.set_trace()
    for kv in properties.split(','):
        if kv.strip().startswith(key):
            k,v = kv.split('=')
            if v[0] == '"' or v[0] == "'":
                return v[1:-1]
            else:
                return v

    return ""
       

def get_info(id):
    cmd = "openstack server show %s -f json" % id
    server = json.loads(check_output(cmd.split()))
    cmd = "openstack user show %s -f json" % server['user_id']
    user = json.loads(check_output(cmd.split()))
    cmd = "openstack project show %s -f json" % server['project_id']
    project = json.loads(check_output(cmd.split()))

    return dict(
        status="success",
        server=server['name'],
        created=server['created'],
        username=user['username'],
        user=user['name'],
        user_email=user['email'],
        project=project['name'],
        description=project['description'],
        project_email=get_property(project['properties'], 'email'),
        )
    

def match_ip(ip):
    cmd = "openstack server list --all-projects -f json"
    results = check_output(cmd.split())
    servers = json.loads(results)

    for s in servers:
        if ip in s['Networks']:
            return get_info(s['ID'])

    return { "status": "fail" }


if __name__ == '__main__':
    print match_ip('141.142.170.14')
