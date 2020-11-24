
from zenoss_client import ZenossClient
import xml.etree.ElementTree as ET
from datetime import datetime


def create_host(name, ip, descrip, state):
    tree = ET.parse('host.xml')
    host = tree.getroot()
    host.find('name').text = name
    host.find('host').text = name
    host.find('interfaces').find('interface').find('ip').text = ip
    host.find('description').text = descrip

    return host


def create_xml(host_list):
    tree = ET.parse('base.xml')
    root = tree.getroot()
    date = datetime.now()
    root.find('date').text = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    hosts = root.find('hosts')
    for host in host_list:
        E_host = create_host(host[0], host[1], host[2], host[3])
        hosts.append(E_host)
    tree.write(open('output.xml', 'wb'))

    return root


if __name__ == '__main__':
    api = ZenossClient(host="http://zenoss.eltl.ru/", user="vikhor.m.g", passwd="Aa15162342")
    api.baseurl = 'http://zenoss.eltl.ru:8080/zport/dmd'

    endpoint = api.endpoint('device_router')
    action = endpoint.action('DeviceRouter')
    method = action.method('getDevices')

    devises = method(params={}, limit=1000)

    dev_list = list()
    for dev in devises['result']['devices']:
        ip = dev['ipAddressString']
        state = dev['productionState']
        groups = dev['groups']
        name = dev['name']
        groupName = None
        if len(groups) > 0:
            groupName = groups[0]['name']
        dev_list.append((name, ip, groupName, state))

    print('total ' + str(len(dev_list)))
    create_xml(dev_list)



