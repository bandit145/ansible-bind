ansible-bind
=========

[![Build Status](https://travis-ci.com/bandit145/ansible-bind.svg?branch=master)](https://travis-ci.com/bandit145/ansible-bind)

This role installs and configures bind dns server. It also supports DNS over TLS using stunnel.

Requirements
------------

jmespath needs to be installed on the ansible control node

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

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
