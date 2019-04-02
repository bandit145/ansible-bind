ansible-bind
=========

[![Build Status](https://travis-ci.com/bandit145/ansible-bind.svg?branch=master)](https://travis-ci.com/bandit145/ansible-bind)

This role installs and configures bind dns server. It also supports DNS over TLS using stunnel.

This is a bit of a hacky mess and tons of logic for getting existing serial numbers of zones (This will most likely be replace with a module I'll write to read and generate RFC 1035 zonefiles)

Requirements
------------

jmespath needs to be installed on the ansible control node.

Role Variables
--------------

```
isc_bind_insecure: open firewalld on tcp/udp 53 (default: true)
isc_bind_secure: open tcp/853 with stunnel and provided certs (default: false)
isc_bind_cert: must be provided if isc_bind_secure: true (cert for stunnel)
isc_bind_key: must be provided if isc_bind_secure: true (key for stunnel)
isc_bind_logging_channels: logging channels for bind (default values below)
  - name: default_log
    versions: 3
    size: 20m
    severity: info
isc_bind_logging_categories: logging categories (default config below)
  - name: default
    channels:
      - default_log
isc_bind_keys: dynamic update keys for bind (example config shown below)
    - name: testkey
     algorithim: hmac-sha512
     secret: Bt890tlZHCNMl95QMAx2WtKh9vH4ZjF//UG0Uwp/RGK1fiAOIoNtHyPaf6YEN/PH/uAwQaH7f8iStNPQ50Gmlg==
isc_bind_zones: list of zone (example config listed below, if allow-update is defined then it is considered a dynamic zone and will freeze and unthaw zones as needed. This will also merge the list of static records with what has been added dynamically). There are many supported options here. I would take a look at templates/named.conf "zones" secton to see what is supported.
    - name: test.com
      type: master
      soa: ns1.test.com
      contact: phil@test.com
      records:
        - test.com. IN NS ns1.test.com.
        - ns1 IN A 192.168.1.2
isc_bind_acls: bind acls to define
	- name: random_acl
	  acls:
	  	- 192.168.1.1
	  	- 192.168.1.2
isc_bind_servers: bind servers to define
	- address: 10.1.10.8
	  keys:
	  	- testkey
isc_bind_listen_on: listen of interfaces to listen on (defaults to 127.0.0.1)
	- any
isc_bind_listen_onv6: v6 interfaces to listen on (defaults to ::1)
	- any
isc_bind_allow_update_forwarding: list of allowed addresses to forward updates through to the master
	- 10.1.10.9
isc_bind_allow_notify: list of addresses allowed to notify server
	- 10.1.10.8
isc_bind_allow_transfer: list of addresses allowed to transfer from this servers (default: none)
	- 10.1.10.9
```

Example Playbook
----------------

```
---
- name: Converge
  hosts: all
  become: true
  pre_tasks:

    - name: start firewalld
      service:
        name: firewalld
        state: started

  vars:
    isc_bind_secure: true
    isc_bind_insecure: false
    isc_bind_cert: "{{ lookup('file','cert.pem') }}"
    isc_bind_key: "{{ lookup('file','key.pem') }}"
    isc_bind_keys:
      - name: testkey
        algorithim: hmac-sha512
        secret: Bt890tlZHCNMl95QMAx2WtKh9vH4ZjF//UG0Uwp/RGK1fiAOIoNtHyPaf6YEN/PH/uAwQaH7f8iStNPQ50Gmlg==
    isc_bind_zones:
      - name: test.com
        type: master
        soa: ns1.test.com
        contact: phil@test.com
        records:
          - test.com. IN NS ns1.test.com.
          - ns1 IN A 192.168.1.2
  roles:
    - role: ansible-bind
```

License
-------

MIT

Author Information
------------------

Philip Bove (pgbson@gmail.com)
