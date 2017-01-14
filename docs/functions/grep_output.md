# Function Logic:

Parses `output_file` line by line and checks for `term`, returning true if the
`term` was found, otherwise it returns false.

# Function parameters

1. term
   A string to search the `output_file` for.
2. output_file
   A file to read line by line, generally a readable stream from `OUT_FILE`
