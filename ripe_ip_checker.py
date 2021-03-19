import requests, sys, ipaddress

if __name__ == "__main__":
  # Check for correct number of args
  if len(sys.argv) < 2:
    print("Usage python3 ripe_ip_checker.py <IP>")
    sys.exit(1)

  # Try to convert the ip address into an IPv4Address object
  # Stop if the IP address is private
  try:
    inputIP = ipaddress.IPv4Address(sys.argv[1])
    if inputIP.is_private:
      print("This IP address is for a private network")
      sys.exit(1)
  except ValueError:
    raise SystemExit("Not a Valid IPv4 address")

  # Try calling the api and dump the resp json
  try:
    resp = requests.get('https://stat.ripe.net/data/country-resource-list/data.json?resource=US&v4_format=prefix')
    data = resp.json()
  except requests.exceptions.RequestException:
    raise SystemExit("Error making API call")

  try:
    for ip in data['data']['resources']['ipv4']:
      if inputIP in ipaddress.ip_network(ip):
        print("Found")
        sys.exit(0)
    print("Not Found")
    sys.exit(0)
  except (ValueError, KeyError):
    raise SystemExit("Response JSON is invalid or an error occurred when converting a CIDR address")
