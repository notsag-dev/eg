# eg
Interactive tool to quickly search and run cheat sheet examples.

## Hacktoberfest
This project was created in the context of Hacktoberfest 2020 so that we can build its database together.

## Dependencies
The only dependency of this project is python 3.

## Install
There is no need for installing any extra tools. I would recommend, though, to add an alias to execute it in a simpler way:

`alias eg="python3 /path/to/eg/repo/app/eg.py"`

## Use
### Print help
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

### Add new cheat sheet examples
Add them to `app/tools_info.json`. Remember to also add some keywords to them so that they are retrieved when searching by keywords.

The examples may have parameters which will be asked for when executed. Add parameters using double curly braces, for example:

`find . -name {{keyword}}`

### Execution example
Search for tools that match the dns keyword:
```
$ eg dns

----------------
------ eg ------
----------------

Results for dns:

1) nslookup: Query Internet name servers interactively
2) dig: DNS lookup utility
3) dnsrecon: DNS Enumeration and Scanning Tool
4) dnsmap: DNS Network Mapper

Enter tool index (or enter to go back):
```
Now select one of the tools to list their cheat sheet examples:
```
Enter tool index (or enter to go back): 1
Examples for nslookup:

1 - Query A records
nslookup {{RHOST}}
-------
2 - Query NS records
nslookup -type=ns {{RHOST}}
-------
3 - Query MX records
nslookup -type=mx {{RHOST}}
-------
4 - Query all available DNS records
nslookup -type=any {{RHOST}}
-------

Enter index of the example to run (or enter to go back):
```

Select the example to run, set parameters and run:

```
Enter index of the example to run (or enter to go back): 1

nslookup {{RHOST}}

Please set parameters

RHOST: google.com

$ nslookup google.com
Server:		192.168.1.1
Address:	192.168.1.1#53

Non-authoritative answer:
Name:	google.com
Address: 172.217.172.46
```

## Contributing
Feel free to add new cheat sheet examples to `app/tools_info.json` which serves as cheat sheet db. Trying to keep command parameters names consistent is key as parameter values are cached and used as default for executing other commands during the same session.

## Licence
GPL-3.0
