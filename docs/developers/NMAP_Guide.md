# A Newbs Guide to NMAP

What is NMAP?

From [wikipedia][wikipedia]:

> Nmap (Network Mapper) is a security scanner originally written by Gordon
> Lyon *[...]* used to discover hosts and services on a computer network, thus
> creating a "map" of the network. To accomplish its goal, Nmap sends specially
> crafted packets to the target host and then analyzes the responses.
> 
> The software provides a number of features for probing computer networks,
> including host discovery and service and operating system detection.

## Enough with the copypasta, just tell me!

In short, Nmap *(or nmap)* is a tool for analyzing computer networks.

It has more features than is entirely necessary, but we only use a few of them:

1. -sP

> bypasses most router's internal packet blocking.

2. IP range specifications 
> specifying a range of IP's *(i.e 192.16.1.0/24 instead of just 192.16.1.0,
> 192.16.1.1, 192.16.1.2 and so on)*


[wikepdia]: https://en.wikipedia.org/wiki/Nmap
