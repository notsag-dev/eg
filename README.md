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

The examples may have parameters which will be asked for when executed. Add parameters using double curly braces, for example: `find . -name {{keyword}}`

## Contributing
Feel free to add new cheat sheet examples to `app/tools_info.json` which serves as cheat sheet db.

## Licence
GPL-3.0
