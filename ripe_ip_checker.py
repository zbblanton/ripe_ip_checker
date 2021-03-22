import sys
import ipaddress
import requests

def searchPublicNetworks(inputIP):
    """
    Gets a list of US public CIDR ranges RIPE database and then checks if given IP is in one of the networks
    
    Parameters: 
    inputIP (string): IP address (Ex: 3.0.0.2)
  
    Returns: 
    String: Found or Not Found
    """
    # Try to convert the ip address into an IPv4Address object
    # Stop if the IP address is private
    try:
        ip = ipaddress.IPv4Address(inputIP)
        if ip.is_private:
            raise Exception("This IP address is for a private network")
    except ValueError:
        raise Exception("Not a Valid IPv4 address")

    # Try calling the api and dump the resp json
    try:
        resp = requests.get('https://stat.ripe.net/data/country-resource-list/data.json?resource=US&v4_format=prefix')
        data = resp.json()
    except requests.exceptions.RequestException:
        raise Exception("Error making API call")

    try:
        for network in data['data']['resources']['ipv4']:
            if ip in ipaddress.ip_network(network):
                return "Found"
        return "Not Found"
    except (ValueError, KeyError):
        raise Exception("Response JSON is invalid or an error occurred when converting a CIDR address")

def main():
    try:
        # Check for correct number of args
        if len(sys.argv) < 2:
            raise Exception("Usage python3 ripe_ip_checker.py <IP>")
        ip = sys.argv[1]
        print(searchPublicNetworks(ip))
    except Exception as e:
        raise SystemExit(e)

if __name__ == "__main__": # pragma: no cover
    main()
