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

    def get_tool_info(self, tool):
        if tool not in self.tools_info:
            return
        return self.tools_info[tool]
    
def print_help():
    print("TODO HELP")

def main():
    print("\n<--T00LZ-->\n")

    toolz = Toolz()
    if (len(sys.argv) != 2):
        print_help()

    tools_list = toolz.get_tools_per_service(sys.argv[1])
    if tools_list is None:
        print("Ouch! No tools found")
        return

    for ind, tool in enumerate(tools_list):
        tool_info = toolz.get_tool_info(tool)
        print(f'{ind + 1}) {tool}: {tool_info["description"]}')

    tool_ind = input("\nPlease enter tool index: ")
    print()
    info = toolz.get_tool_info(tools_list[int(tool_ind) - 1])
    for ind, example in enumerate(info["examples"]):
        print(f'{Color.BOLD}{ind + 1} - {example["title"]} {Color.END}')
        print(example["description"] + "\n")
        print(example["command"])
        print("-------")

main()
