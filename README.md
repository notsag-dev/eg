# eg
Interactive tool to search and run cheat-sheet examples.

## Hacktoberfest
This project was created in the context of Hacktoberfest 2020 so that we can build its database together.

## Dependencies
The only dependency of this project is python 3.

## Install
There is no need for installing any extra tools. I would recommend, though, to add an alias to execute it in a simpler way:

`alias eg="python3 /path/to/eg/repo/app/eg.py"`

## Use
Print help:
```
$ eg -h

    NAME
        eg -- Interactive tool to search and run cheat-sheet examples

    SYNOPSIS
        eg [keyword]

    EXAMPLES
        # Search for tools related to dns
        python eg.py dns

        # Directly access nmap examples
        python eg.py nmap

        # Access the interactive app
        python eg.py
```

## Licence
GPL-3.0
