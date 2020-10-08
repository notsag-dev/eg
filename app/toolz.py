import json
import sys
from color import Color

class Toolz:
    def __init__(self):
        self.tools_per_service = self.load_tools_per_service()
        self.tools_info = self.load_tools_info()
     
    def load_tools_per_service(self):
        with open('tools_per_service.json') as tools:
            return json.load(tools)

    def load_tools_info(self):
        with open('tools_info.json') as tools_info:
            return json.load(tools_info)
        
    def get_tools_per_service(self, service):
        if service not in self.tools_per_service:
            return
        return self.tools_per_service[service]

    def print_tools_per_service(self, service):
        print(f'{Color.BOLD}Results for {service}:{Color.END}')
        self.tools_result_list = self.get_tools_per_service(service)
        if self.tools_result_list is None:
            print("Ouch! No tools found")
            return

        for ind, tool in enumerate(self.tools_result_list):
            tool_info = self.get_tool_info(tool)
            print(f'{ind + 1}) {tool}: {tool_info["description"]}')

    def print_tool_info(self, tool_ind):
        self.service = self.tools_result_list[int(tool_ind) - 1]
        print(f'{Color.BOLD}Examples for {self.service}\n{Color.END}')
        self.tool_info = self.get_tool_info(self.service)
        for ind, example in enumerate(self.tool_info["examples"]):
            print(f'{Color.BOLD}{ind + 1} - {example["title"]} {Color.END}')
            print(example["description"] + "\n")
            print(example["command"])
            print("-------")

    def get_tool_info(self, tool):
        if tool not in self.tools_info:
            return
        return self.tools_info[tool]
    
def print_help():
    print("TODO HELP")

def main():
    print(f'\n{Color.BOLD}<--T00LZ-->{Color.END}\n')

    if (len(sys.argv) != 2):
        print_help()
        return

    toolz = Toolz()
    toolz.print_tools_per_service(sys.argv[1])
    tool_ind = input("\nEnter tool index: ")
    print()
    toolz.print_tool_info(tool_ind)

    example_ind = input("\nEnter example index: ")

main()
