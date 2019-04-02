import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('ns1')


def test_zone_files(host):
    with host.sudo():
        assert not host.file('/var/named/db.delete.com').exists
        test_content = host.file('/var/named/db.test.com').content_string.split('\n') # noqa 501
        assert test_content[2] == '\t2 ;serial'
        dynamic_content = host.file('/var/named/db.dynamic.com').content_string.split('\n') # noqa 501
        assert dynamic_content[2] == '\t1 ;serial'
        assert dynamic_content[10] == 'combine-record IN A 192.168.1.3'
