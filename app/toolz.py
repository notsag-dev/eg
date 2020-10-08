import json
import re
import sys
import os
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
        self.service_name = self.tools_result_list[int(tool_ind) - 1]
        print(f'{Color.BOLD}Examples for {self.service_name}\n{Color.END}')
        self.tool_info = self.get_tool_info(self.service_name)
        for ind, example in enumerate(self.tool_info["examples"]):
            print(f'{Color.BOLD}{ind + 1} - {example["title"]} {Color.END}')
            print(example["description"] + "\n")
            print(example["command"])
            print("-------")

    def get_tool_info(self, tool):
        if tool not in self.tools_info:
            return
        return self.tools_info[tool]

    def run_example(self, example_ind):
        self.example = self.tool_info["examples"][int(example_ind) - 1]
        command = self.example["command"]
        pattern = '\{\{(.*?)\}\}'
        params = re.findall(pattern, command)
        print(f'{Color.BOLD}{Color.BLUE}\nSet parameters:\n{Color.END}')
        param_values = []
        for param in params:
            param_value = input(f'{Color.BLUE}{param}: {Color.END}')
            command = command.replace(f'{{{{{param}}}}}', param_value)
        print(f'{Color.BOLD}\n${Color.END} {command}')
        os.system(command)
    
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
    toolz.run_example(example_ind)

main()
