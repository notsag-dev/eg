import json

def get_tools_per_keyword(tools_info):
    tools_per_keyword = {}
    for tool_name in tools_info:
        for keyword in tools_info.get(tool_name).get("keywords"):
            if keyword in tools_per_keyword:
                tools_per_keyword.get(keyword).append(tool_name)
            else:
                tools_per_keyword[keyword] = [tool_name]
    return tools_per_keyword
