import random
import string
from math import ceil


# 无关名称替换 工具1-10 参数1-5
def random_name(min, max):
    count = random.choice(range(min, max + 1))
    str_list = [random.choice(string.ascii_letters) for i in range(count)]
    random_str = "".join(str_list)
    return random_str


# 逆序
def reverse(str):
    return str[::-1]


# 轻度变化：字符级变动 增删改
def tool_slight_transform(config: list, function: str):
    match_dict = {}
    trans_dict = {}
    # 选出半数需要变化的工具(算上ask_to_user和finish)
    tool_list = []
    tool_change_list = [function]
    for tool in config:
        tool_list.append(tool["name"])
    tool_change_list += random.sample(tool_list, ceil(len(tool_list)/2))
    tool_change_list = list(set(tool_change_list))
    # 修改config
    for tool in config:
        if tool["name"] in tool_change_list:
            name = tool["name"]
            l = len(name)
            # range(1, l)确保一定有改动，但不会全改
            if name == function:
                change_count = random.choice(range(1, ceil(l/3))) if ceil(l/3) > 1 else 1
            else:
                change_count = random.choice(range(0, ceil(l/3)))
            index_list = random.sample(range(l), change_count)
            index_list.sort(reverse=True)
            action = random.choice([1, 2, 3])
            # 增
            if action == 1:
                for index in index_list:
                    name = name[:index] + random.choice(string.ascii_letters) + name[index:]
            # 删
            elif action == 2:
                for index in index_list:
                    name = name[:index] + name[index + 1:]
            # 改
            elif action == 3:
                for index in index_list:
                    name = name[:index] + random.choice(string.ascii_letters) + name[index + 1:]
            match_dict[tool["name"]] = tool["name"]
            trans_dict[tool["name"]] = name
            tool["name"] = name
    return config, match_dict, trans_dict


# 中度变化：无关名称替换 + 原名称逆序
def tool_medium_transform(config: list, function: str):
    match_dict = {}
    trans_dict = {}
    # 选出半数需要变化的工具
    tool_list = []
    tool_change_list = [function]
    for tool in config:
        tool_list.append(tool["name"])
    tool_change_list += random.sample(tool_list, ceil(len(tool_list)/2))
    tool_change_list = list(set(tool_change_list))
    # 修改config
    for tool in config:
        if tool["name"] in tool_change_list:
            name = tool["name"]
            prob = random.random()
            # 确保一定有改动
            if prob > 0.5 or reverse(name) == name:
                name = random_name(1, 10)
            else:
                name = reverse(name)
            match_dict[tool["name"]] = tool["name"]
            trans_dict[tool["name"]] = name
            tool["name"] = name
    return config, match_dict, trans_dict


# 重度变化：工具意义交换 shift 带上ask_to_user和finish
def tool_heavy_transform(config: list, function: str):
    match_dict = {}
    trans_dict = {}
    tool_list = []
    loc = -1
    for index, tool in enumerate(config):
        if tool["name"] == function:
            loc = index
        tool_list.append(tool["name"])
    # 确保要用的工具一定变
    if function != "" and loc != -1:
        while tool_list.index(function) == loc:
            random.shuffle(tool_list)
    else:
        random.shuffle(tool_list)
    for index in range(len(config)):
        match_dict[config[index]["name"]] = f"<<<{index}>>>"
        trans_dict[f"<<<{index}>>>"] = tool_list[index]
        config[index]["name"] = tool_list[index]
    return config, match_dict, trans_dict


# 轻度变化：字符级变动 增删改
def param_slight_transform(config: list, function: str, input: dict):
    match_dict = {}
    trans_dict = {}
    for tool in config[:-2]:
        # 选出半数需要变化的参数
        param_list = []
        param_change_list = []
        if tool["name"] == function:
            param_change_list += list(input.keys())
        for param in tool["parameters"]["properties"].keys():
            param_list.append(param)
        param_change_list += random.sample(param_list, ceil(len(param_list)/2))
        param_change_list = list(set(param_change_list))
        # 修改config
        match_dict[tool["name"]] = {}
        trans_dict[tool["name"]] = {}
        new_properties = {}
        for param_key, param_value in tool["parameters"]["properties"].items():
            if param_key in param_change_list:
                l = len(param_key)
                if param_key in input.keys():
                    change_count = random.choice(range(1, ceil(l/3))) if ceil(l/3) > 1 else 1
                else:
                    change_count = random.choice(range(0, ceil(l/3)))
                index_list = random.sample(range(l), change_count)
                index_list.sort(reverse=True)
                action = random.choice([1, 2, 3])
                name = param_key
                # 增
                if action == 1:
                    for index in index_list:
                        name = name[:index] + random.choice(string.ascii_letters) + name[index:]
                # 删
                elif action == 2:
                    for index in index_list:
                        name = name[:index] + name[index + 1:]
                # 改
                elif action == 3:
                    for index in index_list:
                        name = name[:index] + random.choice(string.ascii_letters) + name[index + 1:]
                match_dict[tool["name"]][param_key] = param_key
                trans_dict[tool["name"]][param_key] = name
                new_properties[name] = param_value
            else:
                new_properties[param_key] = param_value
        tool["parameters"]["properties"] = new_properties
        for index, parameter in enumerate(tool["required"]):
            if parameter in trans_dict[tool["name"]].keys():
                tool["required"][index] = trans_dict[tool["name"]][parameter]
    return config, match_dict, trans_dict


# 中度变化：无关名称替换 + 原名称逆序
def param_medium_transform(config: list, function: str, input: dict):
    match_dict = {}
    trans_dict = {}
    for tool in config[:-2]:
        # 选出半数需要变化的参数
        param_list = []
        param_change_list = []
        if tool["name"] == function:
            param_change_list += list(input.keys())
        for param in tool["parameters"]["properties"].keys():
            param_list.append(param)
        param_change_list += random.sample(param_list, ceil(len(param_list)/2))
        param_change_list = list(set(param_change_list))
        # 修改config
        match_dict[tool["name"]] = {}
        trans_dict[tool["name"]] = {}
        new_properties = {}
        for param_key, param_value in tool["parameters"]["properties"].items():
            if param_key in param_change_list:
                prob = random.random()
                if prob > 0.5 or reverse(param_key) == param_key:
                    name = random_name(1, 5)
                else:
                    name = reverse(param_key)
                match_dict[tool["name"]][param_key] = param_key
                trans_dict[tool["name"]][param_key] = name
                new_properties[name] = param_value
            else:
                new_properties[param_key] = param_value
        tool["parameters"]["properties"] = new_properties
        for index, parameter in enumerate(tool["required"]):
            if parameter in trans_dict[tool["name"]].keys():
                tool["required"][index] = trans_dict[tool["name"]][parameter]
    return config, match_dict, trans_dict


def compare_dicts(dict1, dict2):
    count = 0
    for key, value in dict1.items():
        if key in dict2 and dict2[key] == value:
            count += 1
    return count


# 重度变化：参数意义交换 shift + 新增必要参数
def param_heavy_transform(config: list, function: str, input: dict):
    required_param = {"type": "string", "description": "Whenever you use this parameter, please set it as \"yes\"."}  # used_or_not
    match_dict = {}
    trans_dict = {}
    # 选出半数需要变化的工具
    tool_list = []
    tool_change_list = [function]
    for tool in config[:-2]:
        tool_list.append(tool["name"])
    tool_change_list += random.sample(tool_list, ceil(len(tool_list)/2))
    tool_change_list = list(set(tool_change_list))
    # 修改config
    for tool in config[:-2]:
        if tool["name"] in tool_change_list:
            prob = random.random()
            # 新增必要参数
            if prob > 0.5 or len(list(tool["parameters"]["properties"].keys())) < 2:
                match_dict[tool["name"]] = {}
                param_name = random_name(1, 5)
                match_dict[tool["name"]]["required"] = param_name
                used = random_name(1, 3)
                match_dict[tool["name"]]["yes"] = used
                re_param = required_param.copy()
                re_param["description"] = re_param["description"].replace("\"yes\"", f"\"{used}\"")
                tool["parameters"]["properties"][param_name] = re_param
                tool["required"].append(param_name)
            # 参数意义交换shift
            else:
                param_list = []
                match_dict[tool["name"]] = {}
                trans_dict[tool["name"]] = {}
                new_properties = {}
                for param_key in tool["parameters"]["properties"].keys():
                    param_list.append(param_key)
                if tool["name"] == function:
                    loc = {}
                    for index, param in enumerate(param_list):
                        if param in input:
                            loc[param] = index
                    loc_shift = {}
                    while True:
                        random.shuffle(param_list)
                        for index, param in enumerate(param_list):
                            if param in input:
                                loc_shift[param] = index
                        if compare_dicts(loc, loc_shift) == 0:
                            break
                else:
                    random.shuffle(param_list)
                index = 0
                for param_key, param_value in tool["parameters"]["properties"].items():
                    name = param_list[index]
                    match_dict[tool["name"]][param_key] = f"<<<{index}>>>"
                    trans_dict[tool["name"]][f"<<<{index}>>>"] = name
                    new_properties[name] = param_value
                    index += 1
                tool["parameters"]["properties"] = new_properties
                for index, re_param in enumerate(tool["required"]):
                    tool["required"][index] = match_dict[tool["name"]][re_param]
                for index, re_param in enumerate(tool["required"]):
                    tool["required"][index] = trans_dict[tool["name"]][re_param]
    return config, match_dict, trans_dict
