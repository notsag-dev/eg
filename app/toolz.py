import json
import re
import sys
import os
from color import Color
from shutil import which

class Toolz:
    def __init__(self):
        self.tools_per_service = self.load_tools_per_service()
        self.tools_info = self.load_tools_info()
        self.params_cache = {}
     
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
        self.tools_result_list = self.get_tools_per_service(service)
        if self.tools_result_list is None:
            print(f'{Color.YELLOW}\nOuch! No tools found for {service}\n{Color.END}')
            return None

        print(f'{Color.BOLD}\nResults for {service}:{Color.END}')
        for ind, tool in enumerate(self.tools_result_list):
            tool_info = self.get_tool_info(tool)
            available = which(tool) is not None
            print(f'{ind + 1}) {Color.GREEN if available else Color.RED}{tool}{Color.END}: {tool_info["description"]}')

        return self.tools_result_list

    def print_tool_info(self, tool_ind):
        self.service_name = self.tools_result_list[tool_ind - 1]
        self.tool_info = self.get_tool_info(self.service_name)
        examples = self.tool_info["examples"]
        if examples is None or len(examples) == 0:
            print(f'{Color.YELLOW}No examples found for {self.service_name}!!!{Color.END}')
            return None

        print(f'{Color.BOLD}Examples for {self.service_name}:\n{Color.END}')
        for ind, example in enumerate(self.tool_info["examples"]):
            print(f'{Color.BOLD}{ind + 1} - {example["title"]} {Color.END}')
            if example["description"]:
                print(example["description"] + "\n")
            print(example["command"])
            print("-------")

        return self.tool_info["examples"]

    def get_tool_info(self, tool):
        if tool not in self.tools_info:
            return
        return self.tools_info[tool]

    def run_example(self, example_ind):
        self.example = self.tool_info["examples"][int(example_ind) - 1]
        command = self.example["command"]
        param_pattern = '\{\{(.*?)\}\}'
        params_with_duplicates = re.findall(param_pattern, command)
        params = list(set(params_with_duplicates))
        print(f'{Color.BOLD}\nSet parameters:\n{Color.END}')
        param_values = []
        for param in params:
            cached = None
            if param in self.params_cache:
                cached = self.params_cache[param]
            param_value = input(f'{Color.BLUE}{param}{"(" + cached + ")" if cached else ""}: {Color.END}')
            if param_value:
                self.params_cache[param] = param_value
            if not param_value and cached:
                param_value = cached
            command = command.replace(f'{{{{{param}}}}}', param_value)
        print(f'{Color.BOLD}\n${Color.END} {command}')
        os.system(command)
    
def print_help():
    print("TODO HELP")

def main():
    print(f'\n{Color.BOLD}{Color.RED}<-----T00LZ----->{Color.END}')

    if (len(sys.argv) != 2):
        print_help()
        return

    search = sys.argv[1]
    toolz = Toolz()
    tool_ind = None
    while True:
        found_tools = toolz.print_tools_per_service(search)
        if not found_tools:
            search = None
            while not search:
                search = input("Search for tool or service: ")
            continue

        tool_ind = input("\nEnter tool index: ")
        if tool_ind:
            while not tool_ind.isdigit() or int(tool_ind) > len(found_tools):
                tool_ind = input("\nEnter tool index: ")
                if not tool_ind:
                    continue
        print()

        if not tool_ind:
            old_search = search
            search = input("Search for tool or service: ")
            if not search:
               search = old_search
            continue

        on_examples = True
        while on_examples:
            found_examples = toolz.print_tool_info(int(tool_ind))
            if not found_examples:
                on_examples = False
                continue

            example_ind = input("\nEnter example to run: ")
            if not example_ind:
                on_examples = False
                continue

            toolz.run_example(example_ind)

main()
