import pytest
import ripe_ip_checker
from unittest.mock import patch
import requests
import sys

mockData = {
    'data': {
        'resources': {
            'ipv4': [
                "2.57.248.0/22",
                "2.58.176.0/22",
                "2.58.252.0/22",
                "2.59.20.0/22",
                "3.0.0.0/9",
                "3.128.0.0/9",
                "4.0.0.0/9",
                "4.128.0.0/12",
                "4.144.0.0/12",
                "4.160.0.0/12"
            ]
        }
    }
}

def test_searchPublicNetworks_found():
    with patch('ripe_ip_checker.requests.get') as mockGetResp:
        mockGetResp.return_value.json.return_value = mockData
        assert ripe_ip_checker.searchPublicNetworks("3.0.0.3") == "Found"

def test_searchPublicNetworks_not_found():
    with patch('ripe_ip_checker.requests.get') as mockGetResp:
        mockGetResp.return_value.json.return_value = mockData
        assert ripe_ip_checker.searchPublicNetworks("230.0.0.3") == "Not Found"
    
def test_searchPublicNetworks_invalid_ip():
    with pytest.raises(Exception) as e:
        ripe_ip_checker.searchPublicNetworks("3")
    assert str(e.value) == "Not a Valid IPv4 address"

def test_searchPublicNetworks_private_ip():
    with pytest.raises(Exception) as e:
        ripe_ip_checker.searchPublicNetworks("127.0.0.1")
    assert str(e.value) == "This IP address is for a private network"

def test_searchPublicNetworks_request_timeout():
    with patch('ripe_ip_checker.requests.get', side_effect=requests.Timeout):
        with pytest.raises(Exception) as e:
            ripe_ip_checker.searchPublicNetworks("3.0.0.2")
        assert str(e.value) == "Error making API call"

def test_searchPublicNetworks_data_keyerror():
    mockBadData = {
        'data': {
            'resources': {}
        }
    }
    with patch('ripe_ip_checker.requests.get') as mockGetResp:
        mockGetResp.return_value.json.return_value = mockBadData
        with pytest.raises(Exception) as e:
            ripe_ip_checker.searchPublicNetworks("3.0.0.2")
            assert str(e.value) == "Response JSON is invalid or an error occurred when converting a CIDR address"

def test_searchPublicNetworks_ip_network_valueerror():
    mockBadData = {
        'data': {
            'resources': {
                'ipv4': [
                    "bad CIDR"
                ]
            }
        }
    }
    with patch('ripe_ip_checker.requests.get') as mockGetResp:
        mockGetResp.return_value.json.return_value = mockBadData
        with pytest.raises(Exception) as e:
            ripe_ip_checker.searchPublicNetworks("3.0.0.2")
            assert str(e.value) == "Response JSON is invalid or an error occurred when converting a CIDR address"

def test_main_no_input():
    mockArgs = ["ripe_ip_checker.py"]
    with patch.object(sys, 'argv', mockArgs):
        with pytest.raises(SystemExit) as e:
            print(ripe_ip_checker.main())
        assert str(e.value) == "Usage python3 ripe_ip_checker.py <IP>"

def test_main_input_is_private_ip():
    mockArgs = ["ripe_ip_checker.py", "127.0.0.1"]
    with patch.object(sys, 'argv', mockArgs):
        with pytest.raises(SystemExit) as e:
            print(ripe_ip_checker.main())
        assert str(e.value) == "This IP address is for a private network"
