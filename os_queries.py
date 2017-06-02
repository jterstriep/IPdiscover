import ipaddress
import json
from subprocess import call,check_output


def get_property(properties, key):
    for prop in properties.split(','):
        if prop.strip().startswith(key):
            k,v = prop.split('=')
            if v[0] == '"' or v[0] == "'":
                return v[1:-1]
            else:
                return v

    return ""
       

def unpack_properties(props, prefix=''):
    d = {}
    if not props:
        return d
    for prop in props.split(','):
        k,v = prop.strip().split('=')
        if v[0] == '"' or v[0] == "'":
            d[prefix+k] = v[1:-1]
        else:
            d[prefix+k] = v
    return d


def get_info(id):
    cmd = "openstack server show %s -f json" % id
    server = json.loads(check_output(cmd.split()))
    cmd = "openstack user show %s -f json" % server['user_id']
    user = json.loads(check_output(cmd.split()))
    cmd = "openstack project show %s -f json" % server['project_id']
    project = json.loads(check_output(cmd.split()))

    info = {
        'status': 'ok',
        'server': server['name'],
        'created': server['created'],
        'username': user['username'],
        'user': user['name'],
        'user_email': user['email'],
        'project_name': project['name'],
        'project_description': project['description'],
        }

    info.update(unpack_properties(project['properties'], 
            prefix='project_'))
    return info


def networks(s):
    """parses server's network field and returns list of IPs"""
    netname, addrs = s['Networks'].split('=')
    return [n.strip() for n in addrs.split(',')]


def match_ip(ip):

    try:
        ipaddress.ip_address(ip)
    except ValueError as e:
        return dict(status='error', address=ip, msg=str(e))

    cmd = "openstack server list --all-projects -f json"
    results = check_output(cmd.split())
    servers = json.loads(results)

    for s in servers:
        if ip in networks(s):
            print s['Networks']
            return get_info(s['ID'])

    return dict(status="error", address=ip, msg='IP not in use')


if __name__ == '__main__':
    print match_ip('141.142.170.14')
