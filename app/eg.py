import json
import os
import re
import sys
from color import Color
from shutil import which
from get_tools_per_keyword import get_tools_per_keyword

class Eg:
    def __init__(self):
        self.tools_info = self.load_tools_info()
        self.tools_per_keyword = get_tools_per_keyword(self.tools_info)
        self.params_cache = {}
     
    def load_tools_info(self):
        with open('tools_info.json') as tools_info:
            tools_info = json.load(tools_info)
            result = {}
            for tool_name in tools_info:
                available = which(tool_name) is not None
                result[tool_name] = { **tools_info.get(tool_name), "available": available, "name": tool_name }
            return result
        
    def search_tools_per_keyword(self, keyword):
        if keyword not in self.tools_per_keyword:
            return []
        tool_names = self.tools_per_keyword[keyword]
        result = []
        for tool_name in tool_names:
            result.append(self.tools_info.get(tool_name));
        return result;

    def print_tools_per_keyword(self, keyword):
        exact_match = self.tools_info.get(keyword)
        if (exact_match):
            exact_match.update({ "exact_match": True });
        search_matches_list = self.search_tools_per_keyword(keyword)
        if exact_match == None and len(search_matches_list) == 0:
            print(f'{Color.YELLOW}\nNo tools found for keyword {keyword}\n{Color.END}')
            return []

        if len(search_matches_list) == 0 and exact_match:
            self.tools_result_list = [exact_match]
            return self.tools_result_list

        if exact_match:
            search_matches_list = [exact_match] + search_matches_list

        print(f'{Color.BOLD}\nResults for {keyword}:{Color.END}')
        sorted_tool_info_list = sorted(search_matches_list, key=lambda t: t["available"], reverse = True)
        for ind, tool in enumerate(sorted_tool_info_list):
            print(f'{ind + 1}) {Color.GREEN if tool.get("available") else Color.RED}{tool.get("name")}{Color.END}: {tool.get("description")}')
        self.tools_result_list = sorted_tool_info_list

        return sorted_tool_info_list

    def print_tool_info(self, tool_ind):
        self.tool_info = self.tools_result_list[tool_ind - 1]
        self.service_name = self.tool_info.get("name")
        examples = self.tool_info["examples"]
        if examples is None or len(examples) == 0:
            print(f'{Color.YELLOW}\nNo examples found for {self.service_name}!!!\n{Color.END}')
            return None

        print(f'{Color.BOLD}\nExamples for {self.service_name}:\n{Color.END}')
        for ind, example in enumerate(self.tool_info["examples"]):
            print(f'{Color.BOLD}{ind + 1} - {example["title"]} {Color.END}')
            if example.get("description"):
                print(example["description"] + "\n")
            print(example["command"])
            print("-------")

        if not self.tool_info.get("available"):
            print(f'{Color.YELLOW}\nInstall {self.service_name} to run examples!!!{Color.END}')

        return self.tool_info

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
            param_value = input(f'{Color.BLUE}{param}{" (" + cached + ")" if cached else ""}: {Color.END}')
            if param_value:
                self.params_cache[param] = param_value
            if not param_value and cached:
                param_value = cached
            command = command.replace(f'{{{{{param}}}}}', param_value)
        print(f'{Color.BOLD}\n${Color.END} {command}')
        os.system(command)
    
def print_help():
    print("TODO HELP")

def search_input(default = None):
    return input(f'Search for tool or service{" (" + default + ")" if default else ""}: ')

def tool_input():
    return input("\nEnter tool index: ")

def example_input():
    return input("\nEnter the index of the example to run: ")

def main():
    print(f'{Color.BOLD}\n----------------{Color.END}')
    print(f'------ {Color.BOLD}eg{Color.END} ------')
    print(f'{Color.BOLD}----------------{Color.END}')

    if (len(sys.argv) != 2):
        print_help()
        return

    search = sys.argv[1]
    eg = Eg()
    exact_match = False
    while True:
        found_tools = []
        tool_ind = None
        exact_match = False
        while not search:
            search = search_input()

        found_tools = eg.print_tools_per_keyword(search)

        if len(found_tools) == 0:
            search = None
            continue

        # Tool selection. If the search produced just an exact match
        # select it automatically
        if len(found_tools) == 1 or found_tools[0].get("exact_match") == True:
            exact_match = True
            tool_ind = 1
        else:
            tool_ind = tool_input()
            if tool_ind:
                while tool_ind and (not tool_ind.isdigit() or int(tool_ind) > len(found_tools)):
                    tool_ind = tool_input()
                    if not tool_ind:
                        continue

        if not tool_ind:
            old_search = search
            search = search_input(old_search)
            if not search:
               search = old_search
            continue

        on_examples = True
        while on_examples:
            tool = eg.print_tool_info(int(tool_ind))
            if not tool or len(tool.get("examples")) == 0 or not tool.get("available"):
                if exact_match:
                    search = None
                on_examples = False
                continue

            example_ind = example_input()
            if not example_ind:
                on_examples = False
                if exact_match:
                    search = None
                continue

            eg.run_example(example_ind)

main()
