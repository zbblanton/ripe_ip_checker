# Description

Simple CLI tool to check if a given IP address is registered in one of the CIDR ranges from RIPE NCC Regional Internet Registry Database.

# Usage

Enter any valid IPv4 IP as an argument. The result will either be "Found" or "Not Found". For example:

```bash
zbblanton@DESKTOP-IMPMTVB:~/workspace$ python3 ripe_ip_checker.py 3.0.10.3
Found
```

# Thought Process

So this was a fun problem. Seems simple at first but there are a few gotchas.

To start I loaded up Postman and made a GET request to the API to examine the data. The first problem became clear, the data is large (around 300KB).

So after examing the response data, I decided to look around at the documentation (https://stat.ripe.net/docs/data_api). I wanted to see if I could maybe add a parameter to the API call to limit my response to only 'ipv4'. No success, oh well.

Next, I started looking more at the specifics of the input. At first I thought I needed to accept any IP addresses like 192.168.0.120/32 but technically that input contains the `/32` subnet mask. The instructions state "Takes an __IP address__ as a command-line argument". So the only valid inputs I decided to check for are valid IPs with no subnet mask.

Now I went down a small rabbit hole trying to find out the best way to search the data for a valid subnet. There are nearly 60k subnet ranges in the data. At first, I thought about trying to splice the array up. I tried a few methods like searching each ip with strings `startswith()` but there were cases when that didn't work well, for example, startswith('1') could return any `1*.` address. So I tried adding `.` like `startswith('1' + '.')`, this gave me much better results but still not amazing (The `128.x.x.x` space had like 936 different allocated address spaces). 

After playing around with few other ideas I ended up putting a pin in it and looked at how to check if the input IP address was in one of the subnet spaces. So I searched around and it turns out that python 3.3 has a very convenient `ipaddress` module that has exactly what I want:

```python
if ipaddress.ip_address(inputIP) in ipaddress.ip_network(network):
    #Do something
```

Perfect! Then I wrote a for loop that would check each CIDR range against the input IP address. I was thinking this would be slow since the for loop would check each CIDR range until a match was found, but to my surprise, it was pretty fast (I even ran it on a raspberry pi):

```bash
zbblanton@DESKTOP-IMPMTVB:~/workspace$ time python3 ripe_ip_checker.py 3.0.0.3
Found

real    0m16.242s
user    0m0.094s
sys     0m0.078s
zbblanton@DESKTOP-IMPMTVB:~/workspace$ time python3 ripe_ip_checker.py 3.0.0.3
Found

real    0m3.055s
user    0m0.063s
sys     0m0.094s
```

Notice that the first time is much larger. This is the API computing our response, in Postman the call also took about 15 seconds. However the good news is I believe there's some server caching on the API side, so our program call after that is much faster. The cache seems to last for about 1-2 minutes.

With such good results using the built-in `ipaddress` module I decided that it wasn't worth trying to slice the array up into a smaller chuck as I had discussed above.

# Testing

This script doesn't have any functions other than main so I decided not to do any unit tests. However, I wanted to do some kind of testing so I wrote a quick and dirty shell script to run integration tests.

```bash
chmod +x test_ripe_ip_checker.sh
./test_ripe_ip_checker.sh
```

# Dependecies:
* `Python v3.3 or greater`

