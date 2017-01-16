# Function logic

Returns a [subprocess.Popen][1] object that runs `nmap -sP` for the `ip_range`.

# Function Arguments

1. output_file:
   - Any python file object, should generally be `OUT_FILE`
2. ip_range:
   - A valid ip range to pass to the call to `nmap -sP`.
     Should be an internal network range such as `192.16.1.0/24` or
     `172.16.1.0/24`


[1]: https://docs.python.org/3/library/subprocess.html#popen-constructor
