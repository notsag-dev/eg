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

        self.search = None
        self.search_results = []
        self.selected_tool = 0
        self.search_exact_match = False
     
    def load_tools_info(self):
        result = {}
        with open('tools_info.json') as tools_info:
            tools_info = json.load(tools_info)
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
        search_exact_match = self.tools_info.get(keyword)
        if (search_exact_match):
            search_exact_match.update({ "exact_match": True });

        search_matches_list = self.search_tools_per_keyword(keyword)

        if search_exact_match == None and len(search_matches_list) == 0:
            print(f'{Color.YELLOW}No tools found for keyword {keyword}\n{Color.END}')
            self.search = None
            self.search_results = []
            return []

        if len(search_matches_list) == 0 and search_exact_match:
            self.tools_result_list = [search_exact_match]
            return self.tools_result_list

        if search_exact_match:
            search_matches_list = [search_exact_match] + search_matches_list

        print(f'{Color.BOLD}Results for {keyword}:\n{Color.END}')
        sorted_tool_info_list = sorted(search_matches_list, key=lambda t: t["available"], reverse = True)
        for ind, tool in enumerate(sorted_tool_info_list):
            print(f'{ind + 1}) {Color.GREEN if tool.get("available") else Color.RED}{tool.get("name")}{Color.END}: {tool.get("description")}')
        self.tools_result_list = sorted_tool_info_list

        return sorted_tool_info_list

    def print_tool_info(self, selected_tool_index):
        self.tool_info = self.tools_result_list[selected_tool_index - 1]
        self.service_name = self.tool_info.get("name")
        examples = self.tool_info["examples"]
        if examples is None or len(examples) == 0:
            print(f'{Color.YELLOW}\nNo examples found for {self.service_name}!!!\n{Color.END}')
            return None

        print(f'{Color.BOLD}Examples for {self.service_name}:\n{Color.END}')
        for ind, example in enumerate(self.tool_info["examples"]):
            print(f'{Color.BOLD}{ind + 1} - {example["title"]} {Color.END}')
            if example.get("description"):
                print(example["description"] + "\n")
            print(example["command"])
            print("-------")

        if not self.tool_info.get("available"):
            print(f'{Color.YELLOW}\nInstall {self.service_name} to run examples!!!{Color.END}')

        return self.tool_info

    def run_example(self, example_ind):
        self.example = self.tool_info["examples"][int(example_ind) - 1]
        command = self.example["command"]
        param_pattern = '\{\{(.*?)\}\}'
        params = re.findall(param_pattern, command)
        print(f'{Color.BOLD}\nPlease set parameters\n{Color.END}')
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

    def execute_search_state(self, initial_search):
        search = initial_search
        if (self.search):
            search = self.search
        while not search:
            search = get_user_input_search()
        self.search = search
        self.search_results = self.print_tools_per_keyword(search)
        return self.search_results

    def execute_tool_selection_state(self):
        go_back_to_search = False

        if len(self.search_results) == 1 and self.search_results[0].get("exact_match"):
            self.search_exact_match = True
        else:
            user_input_tool_selection = get_user_input_index_selection(len(self.search_results), "\nEnter tool index: ")

            if not user_input_tool_selection:
                self.search = None
                go_back_to_search = True
                return { "go_back_to_search": go_back_to_search }

            self.selected_tool_index = int(user_input_tool_selection)
            self.selected_tool = self.search_results[self.selected_tool_index - 1]

        return { "go_back_to_search": go_back_to_search }

    def execute_example_selection_state(self):
        while True:
            tool = self.print_tool_info(int(self.selected_tool_index))
            if not tool or len(tool.get("examples")) == 0 or not tool.get("available"):
                if self.search_exact_match:
                    self.search = None
                return 

            user_input_example_selection = get_user_input_index_selection( \
                len(tool.get("examples")), \
                "\nEnter index of the example to run (or enter to go back): " \
            )
            if not user_input_example_selection:
                if self.search_exact_match:
                    self.search = None
                return 

            print(f'\n{Color.BOLD}{tool.get("examples")[int(user_input_example_selection)-1].get("command")}{Color.END}')
            self.run_example(user_input_example_selection)
    
def print_help():
    print("TODO HELP")

def get_user_input_search(default = None):
    default_value_string = ""
    if default:
        default_value_string = f' ({default})'

    res =input(f'Search for tool or service{default_value_string}: ')
    if res:
        print()
    return res

def get_user_input_index_selection(max_ind, message):
    user_input = "placeholder"
    while user_input and not is_valid_digit_option(user_input, max_ind):
        user_input = input("\nEnter tool index: ")
    return user_input


def is_valid_digit_option(user_input, max_option_value):
    if not user_input.isdigit():
        return False
    if int(user_input) > max_option_value or int(user_input) < 1:
        return False
    return True;

def banner():
    print(f'{Color.BOLD}\n----------------{Color.END}')
    print(f'------ {Color.BOLD}eg{Color.END} ------')
    print(f'{Color.BOLD}----------------\n{Color.END}')

def main():
    banner()

    if (len(sys.argv) > 2):
        print_help()
        return

    search = None
    if len(sys.argv) == 2:
        search = sys.argv[1]

    eg = Eg()
    while True:
        search_results = eg.execute_search_state(search)

        if len(search_results) == 0:
            search = None
            continue

        tool_selection_result = eg.execute_tool_selection_state()
        if tool_selection_result.get("go_back_to_search"):
            continue

        eg.execute_example_selection_state()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
