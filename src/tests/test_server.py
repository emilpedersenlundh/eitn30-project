#!/home/fideloper/.envs/eitn30-project/bin/python3

import pytest

from src import server

def test_init(self):
    s = server('10.10.10.1')
    expected = ('tun', 'longge', '10.10.10.1', '255.255.255.0', '10.10.10.1')
    actual = (s.tun.nic_type, s.tun.nic_name, s.tun.ip, s.tun.mask, s.tun.gateway)
    assert expected == actual
