import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_zone_files(host):
    with host.sudo():
        assert not host.file('/var/named/db.delete.com').exists
        assert host.file('/var/named/db.test.com').contains('2 ;serial')


def test_ports(host):
    ports = ['53/udp', '53/tcp']
    output = host.check_output('firewall-cmd --list-ports').split(' ')
    with host.sudo():
        for port in ports:
            assert port in output


def test_log(host):
    with host.sudo():
        assert host.file('/var/named/log/default_log').exists
