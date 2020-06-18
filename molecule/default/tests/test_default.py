import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_packages(host):
    assert host.package('stunnel').is_installed
    assert host.package('bind').is_installed


def test_named_running(host):
    named = host.service('named')
    stunnel = host.service('stunnel')
    assert named.is_running
    assert named.is_enabled
    assert stunnel.is_running
    assert stunnel.is_running

def test_nginx_running(host):
    nginx = host.service('nginx')
    assert nginx.is_running
    assert nginx.is_enabled

def test_stunnel(host):
    output = host.check_output("openssl s_client -connect 127.0.0.1:853 < /dev/null 2>&1 | awk '{if($1 == \"Protocol\"){print $3}}'")  # noqa 501
    assert output.lower() == 'tlsv1.2'


def test_zone_files(host):
    with host.sudo():
        assert host.file('/var/named/db.test.com').contains('1 ;serial')


def test_ports(host):
    no_ports = ['53/udp', '53/tcp']
    with host.sudo():
        output = host.check_output('firewall-cmd --list-ports')
    assert '853/tcp' in output
    for port in no_ports:
        assert port not in output.split(' ')


def test_log(host):
    with host.sudo():
        assert host.file('/var/named/log/default_log').exists
