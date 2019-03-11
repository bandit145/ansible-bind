import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_named_running(host):
    named = host.service('named')
    assert named.is_running
    assert named.is_enabled


def test_zone_files(host):
    delete_com = host.file('/var/named/db.delete.com')
    test_com = host.file('/var/named/db.test.com')
    assert not delete_com.exists
    assert test_com.contains('2 ;serial')
