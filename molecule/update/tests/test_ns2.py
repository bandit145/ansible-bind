import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('ns2')


def test_zone_files(host):
    with host.sudo():
        test_com_serial = host.check_output("dig soa test.com @127.0.0.1 | awk 'NR==15{print $7}'") # noqa 501
        assert test_com_serial == '2'
        dynamic_com_serial = host.check_output("dig soa dynamic.com @127.0.0.1 | awk 'NR==15{print $7}'") # noqa 501
        assert dynamic_com_serial == '1'
