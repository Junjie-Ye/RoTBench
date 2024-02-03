import json
import random
from Code.Data_Process import transformer
import argparse
import os


def mode_control(mode):
    if "tool" in mode:
        target_control = "tool"
    else:
        target_control = "param"
    tool_control, param_control = 0, 0
    if mode == "tool_slight":
        tool_control = 1
    elif mode == "tool_medium":
        tool_control = 2
    elif mode == "tool_heavy":
        tool_control = 3
    elif mode == "uni_tool":
        tool_control = random.choice([1, 2, 3])
    elif mode == "param_slight":
        param_control = 1
    elif mode == "param_medium":
        param_control = 2
    elif mode == "param_heavy":
        param_control = 3
    elif mode == "uni_param":
        param_control = random.choice([1, 2, 3])
    return tool_control, param_control, target_control


def conversations_process(conversations, match_dict, trans_dict, sys_doc, target):
    for conv in conversations:
        if conv["from"] == "system":
            conv["value"] = sys_doc
        if conv["from"] == "assistant":
            answer_list = conv["value"]
            for idx, answer in enumerate(answer_list):
                if target == "tool":
                    for tool, name in match_dict.items():
                        if answer.find(f"Action: {tool}\n") != -1:
                            answer_list[idx] = answer.replace(f"Action: {tool}\n", f"Action: {name}\n")
                    for index, name in trans_dict.items():
                        if answer.find(f"Action: {index}\n") != -1:
                            answer_list[idx] = answer.replace(f"Action: {index}\n", f"Action: {name}\n")
                if target == "param":
                    function = answer[answer.find("Action:") + 8:answer.find("Action Input:") - 1]
                    if function == "ask_to_user" or function == "finish":
                        continue
                    action_input = answer[answer.find("Action Input:"):]
                    if function in match_dict.keys():
                        if "required" in match_dict[function].keys() and "yes" in match_dict[function].keys():
                            if action_input[-2] == "{":
                                action_input = action_input[:-1] + "\"{name}\": \"{yes}\"".format(name=match_dict[function]["required"], yes=match_dict[function]["yes"]) + action_input[-1:]
                            else:
                                action_input = action_input[:-1] + ", \"{name}\": \"{yes}\"".format(name=match_dict[function]["required"], yes=match_dict[function]["yes"]) + action_input[-1:]
                        else:
                            for param, index in match_dict[function].items():
                                if action_input.find(f"\"{param}\"") != -1:
                                    action_input = action_input.replace(f"\"{param}\":", f"\"{index}\":")
                            for index, name in trans_dict[function].items():
                                if action_input.find(f"\"{index}\"") != -1:
                                    action_input = action_input.replace(f"\"{index}\":", f"\"{name}\":")
                    answer_list[idx] = answer[:answer.find("Action Input:")] + action_input
        if conv["from"] == "function":
            if target == "tool":
                for tool, name in match_dict.items():
                    if conv["value"].find(f"{tool}") != -1:
                        conv["value"] = conv["value"].replace(f"{tool}", f"{name}")
                for index, name in trans_dict.items():
                    if conv["value"].find(f"{index}") != -1:
                        conv["value"] = conv["value"].replace(f"{index}", f"{name}")
            if target == "param":
                function = ""
                for tool in match_dict.keys():
                    if conv["value"].find(f"{tool}") != -1:
                        function = tool
                if function == "":
                    continue
                if "required" in match_dict[function].keys() and "yes" in match_dict[function].keys():
                    continue
                else:
                    for param, index in match_dict[function].items():
                        if conv["value"].find(f"\'{param}\'") != -1:
                            conv["value"] = conv["value"].replace(f"\'{param}\'", f"\'{index}\'")
                    for index, name in trans_dict[function].items():
                        if conv["value"].find(f"\'{index}\'") != -1:
                            conv["value"] = conv["value"].replace(f"\'{index}\'", f"\'{name}\'")
        if conv["from"] == "user":
            if target == "tool":
                for tool, name in match_dict.items():
                    if conv["value"].find(f"{tool}\n") != -1:
                        conv["value"] = conv["value"].replace(f"{tool}\n", f"{name}\n")
                for index, name in trans_dict.items():
                    if conv["value"].find(f"{index}\n") != -1:
                        conv["value"] = conv["value"].replace(f"{index}\n", f"{name}\n")
    return conversations


def data_transform_process(origin_file, mode, output_file):
    # origin_file
    with open(origin_file, encoding="utf-8") as f:
        data = json.load(f)
    for d in data:
        if d["id"][5] == "1":
            assistant = d["conversations"][2]["value"]
        elif d["id"][5] == "3":
            assistant = d["conversations"][6]["value"]
        action = assistant[assistant.find("Action:") + 8: assistant.find("Action Input:") - 1]
        action_input = json.loads(assistant[assistant.find("Action Input:") + 14:])
        prompt = d["conversations"][0]["value"][:d["conversations"][0]["value"].find("[")]
        p_len = len(prompt)
        config = json.loads(d["conversations"][0]["value"][p_len:-13])

        tool_trans, param_trans, target = mode_control(mode)

        if tool_trans == 1:
            config, match_dict, trans_dict = transformer.tool_slight_transform(config, action)
        elif tool_trans == 2:
            config, match_dict, trans_dict = transformer.tool_medium_transform(config, action)
        elif tool_trans == 3:
            config, match_dict, trans_dict = transformer.tool_heavy_transform(config, action)

        if param_trans == 1:
            config, match_dict, trans_dict = transformer.param_slight_transform(config, action, action_input)
        elif param_trans == 2:
            config, match_dict, trans_dict = transformer.param_medium_transform(config, action, action_input)
        elif param_trans == 3:
            config, match_dict, trans_dict = transformer.param_heavy_transform(config, action, action_input)

        end_function = config[-1]["name"]
        sys_doc = prompt.replace("finish", end_function, 2) + json.dumps(config) + "\n\nLet's Begin!\n"

        d["conversations"] = conversations_process(d["conversations"], match_dict, trans_dict, sys_doc, target)

    # output_file
    if output_file:
        with open(output_file, "w", encoding="utf-8") as w:
            json.dump(data, w, indent=4, ensure_ascii=False)
    else:
        return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin_file", type=str)
    parser.add_argument("--output_dir", type=str)

    args = parser.parse_args()
    origin_file = args.origin_file
    output_dir = args.output_dir

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    transform_envs = ["slight", "medium", "heavy"]
    for env in transform_envs:
        file_data = data_transform_process(origin_file, f"tool_{env}", "") + data_transform_process(origin_file, f"param_{env}", "")
        with open(os.path.join(output_dir, f"{env}.json"), "w", encoding="utf-8") as w:
            json.dump(file_data, w, indent=4, ensure_ascii=False)
    uni_temp = os.path.join(output_dir, "uni_tool.json")
    data_transform_process(origin_file, "uni_tool", uni_temp)
    data_transform_process(uni_temp, "uni_param", os.path.join(output_dir, "union.json"))
    if os.path.isfile(uni_temp):
        os.remove(uni_temp)
