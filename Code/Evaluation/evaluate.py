import sys
import json
import argparse
import re
from ast import literal_eval


sys.stdout.reconfigure(encoding='utf-8')


def get_cata_list(answer_file):
    Text_Generation = []
    Real_Time_Search = []
    Data_Understanding = []
    Personal_Life = []
    Application_Manipulation = []
    Information_Retrieval = []
    Financial_Transactions = []
    # Record different scenarios
    with open(answer_file, encoding="utf-8") as f:
        data = json.load(f)
    for index, d in enumerate(data):
        sce = d["scenario"]
        if sce == "TG":
            Text_Generation.append(index)
            continue
        if sce == "RS":
            Real_Time_Search.append(index)
            continue
        if sce == "DU":
            Data_Understanding.append(index)
            continue
        if sce == "PL":
            Personal_Life.append(index)
            continue
        if sce == "AM":
            Application_Manipulation.append(index)
            continue
        if sce == "IR":
            Information_Retrieval.append(index)
            continue
        if sce == "FT":
            Financial_Transactions.append(index)
            continue
    cata_list = [Text_Generation, Real_Time_Search, Data_Understanding, Personal_Life, Application_Manipulation, Information_Retrieval, Financial_Transactions]
    return cata_list


def get_config(data):
    p_len = len(data["conversations"][0]["value"][:data["conversations"][0]["value"].find("[")])
    config = json.loads(data["conversations"][0]["value"][p_len:-13])
    return config


def get_answer_list(data):
    return data["conversations"][-1]["value"]


def get_raven_resultcall(data, version):
    if version == 1:
        result_call = data["result"]
        start_str = "Initial Answer: "
        end_str = "\nReflection: "
        start_idx = result_call.find(start_str) + len(start_str)
        end_idx = result_call.find(end_str)
        result_call = result_call[start_idx: end_idx]
    if version == 2:
        result_call = data["result"][6:data["result"].find("\nThought:") - 1]
        if result_call.find(";") != -1:
            result_call = result_call[:result_call.find(";")]
        if result_call.count("(") == 1:
            pass
        else:
            end_idx = result_call.find(")")
            start_idx = end_idx
            func = 0
            for char in result_call[:end_idx][::-1]:
                start_idx -= 1
                if char == "(":
                    func = 1
                if char == "=" and func:
                    break
            result_call = result_call[start_idx + 1: end_idx + 1]
    return result_call


def get_raven_action_input(action_input, test_action, config, version):
    if version == 1:
        if action_input.find("=") != -1:
            action_input = action_input.replace("(", "{").replace(")", "}").replace("=", "':")
            for idx, char in enumerate(action_input):
                if action_input[idx] == "{" and action_input[idx + 1] != "}":
                    action_input = action_input[:idx + 1] + "'" + action_input[idx + 1:]
                if idx > 0 and action_input[:idx + 1].count("'") % 2 == 0:
                    if (action_input[idx - 1] + action_input[idx] == ", ") and (action_input[idx - 1] + action_input[idx] + action_input[idx + 1] != ", '"):
                        action_input = action_input[:idx + 1] + "'" + action_input[idx + 1:]
            try:
                action_input = literal_eval(action_input)
            except SyntaxError:
                print("SyntaxError")
                return 0
        else:
            match = re.search(r'\((.*)\)', action_input)
            if match:
                input_list = [item for item in match.group(1).split(', ')]
            else:
                print("MatchError")
                return 0
            for tools in config:
                if (tools["name"]) == test_action:
                    param_config = tools["parameters"]["properties"]
                    paramlist = list(param_config)
                    break
            action_input = {}
            try:
                for idx, input in enumerate(input_list):
                    action_input[paramlist[idx]] = input
            except (UnboundLocalError, IndexError):
                print("UnboundLocalError/IndexError")
                return 0
    elif version == 2:
        action_input = action_input.replace("(", "{").replace(")", "}").replace("=", "':")
        for idx, char in enumerate(action_input):
            if action_input[idx] == "{" and action_input[idx + 1] != "}":
                action_input = action_input[:idx + 1] + "'" + action_input[idx + 1:]
            if idx > 0 and action_input[:idx + 1].count("'") % 2 == 0:
                if (action_input[idx - 1] + action_input[idx] == ", ") and (action_input[idx - 1] + action_input[idx] + action_input[idx + 1] != ", '"):
                    action_input = action_input[:idx + 1] + "'" + action_input[idx + 1:]
        try:
            action_input = literal_eval(action_input)
        except SyntaxError:
            print("SyntaxError")
            return 0
    for key in list(action_input.keys()):
        if action_input[key] == '':
            del action_input[key]
    return action_input


def get_test_value(data, config, version):
    if not version:
        test_value = data["conversations"][-1]["value"]
        test_action = test_value[test_value.find("Action:") + 8: test_value.find("Action Input:")]
        if test_action[-1] == "\n":
            test_action = test_action[:-1]
        try:
            test_action_input = json.loads(test_value[test_value.find("Action Input:") + 14:])
        except json.decoder.JSONDecodeError:
            return test_action, 0
        if isinstance(test_action_input, str):
            return test_action, 0
    else:
        test_value = get_raven_resultcall(data, version)
        test_action = test_value[:test_value.find("(")]
        test_action_input = test_value[test_value.find("("):]
        test_action_input = get_raven_action_input(test_action_input, test_action, config, version)
    return test_action, test_action_input


def ts_eval(test, answer, version=0):
    global check_list
    tool_selection = []
    for i in range(len(answer)):
        config = get_config(answer[i])
        answers = get_answer_list(answer[i])
        test_action, test_action_input = get_test_value(test[i], config, version)
        if not test_action_input:
            continue
        # Check all possible answers
        right_status = 0
        for ans in answers:
            answer_action = ans[ans.find("Action:") + 8: ans.find("Action Input:")]
            if answer_action[-1] == "\n":
                answer_action = answer_action[:-1]
            if answer_action == config[-1]["name"] and test_action == "finish":
                test_action = answer_action
            if not answer_action == test_action:
                continue
            if right_status < 1:
                right_status = 1
                # print("<Tool Selection : Right>")
                break
        if right_status >= 1:
            tool_selection.append(i)
    a_list = []
    a_list.append(len(tool_selection))
    for cata in cata_list:
        a_list.append(len(list(set(cata) & set(tool_selection))))
    check_list.append(a_list)


def pi_eval(test, answer, version=0):
    global check_list
    parameter_identification = []
    for i in range(len(answer)):
        config = get_config(answer[i])
        answers = get_answer_list(answer[i])
        test_action, test_action_input = get_test_value(test[i], config, version)
        if not test_action_input:
            continue
        # Check all possible answers
        right_status = 0
        for ans in answers:
            answer_action = ans[ans.find("Action:") + 8: ans.find("Action Input:")]
            if answer_action[-1] == "\n":
                answer_action = answer_action[:-1]
            answer_action_input = json.loads(ans[ans.find("Action Input:") + 14:])
            if answer_action == config[-1]["name"] and test_action == "finish":
                test_action = answer_action
            if not answer_action == test_action:
                continue
            if right_status < 1:
                right_status = 1
            if not answer_action_input.keys() == test_action_input.keys():
                continue
            if right_status < 2:
                right_status = 2
                # print("<Parameter Identification : Right>")
                break
        if right_status >= 2:
            parameter_identification.append(i)
    a_list = []
    a_list.append(len(parameter_identification))
    for cata in cata_list:
        a_list.append(len(list(set(cata) & set(parameter_identification))))
    check_list.append(a_list)


def cf_eval(test, answer, version=0):
    global check_list
    content_filling = []
    for i in range(len(answer)):
        config = get_config(answer[i])
        answers = get_answer_list(answer[i])
        test_action, test_action_input = get_test_value(test[i], config, version)
        if not test_action_input:
            continue
        # Check all possible answers
        right_status = 0
        for ans in answers:
            answer_action = ans[ans.find("Action:") + 8: ans.find("Action Input:")]
            if answer_action[-1] == "\n":
                answer_action = answer_action[:-1]
            answer_action_input = json.loads(ans[ans.find("Action Input:") + 14:])
            if answer_action == config[-1]["name"] and test_action == "finish":
                test_action = answer_action
            if not answer_action == test_action:
                continue
            if right_status < 1:
                right_status = 1
            if not answer_action_input.keys() == test_action_input.keys():
                continue
            if right_status < 2:
                right_status = 2
            if answer_action == config[-1]["name"]:
                answer_action = "finish"
            if answer_action == config[-2]["name"]:
                answer_action = "ask_to_user"
            del_key = []
            for key, value in answer_action_input.items():
                if value == "None":
                    del_key.append(key)
            for key in del_key:
                del answer_action_input[key]
                del test_action_input[key]
            if not answer_action_input == test_action_input and answer_action != "finish" and answer_action != "ask_to_user":
                continue
            if right_status < 3:
                right_status = 3
                # print("<Content Filling : Right>")
                break
        if right_status >= 3:
            content_filling.append(i)
    a_list = []
    a_list.append(len(content_filling))
    for cata in cata_list:
        a_list.append(len(list(set(cata) & set(content_filling))))
    check_list.append(a_list)


def general_eval(test_data, answer_data):
    ts_eval(test_data, answer_data)
    pi_eval(test_data, answer_data)
    cf_eval(test_data, answer_data)


def raven_eval(test_data, answer_data, version):
    ts_eval(test_data, answer_data, version)
    pi_eval(test_data, answer_data, version)
    cf_eval(test_data, answer_data, version)


def show_stats(check_list, max_len):
    print("Overall:")
    print("Tool Selection: " + "{:.2f}".format(check_list[0][0] / max_len * 100))
    print("Parameter Identification: " + "{:.2f}".format(check_list[1][0] / max_len * 100))
    print("Content Filling: " + "{:.2f}".format(check_list[2][0] / max_len * 100))

    # All Scenarios
    scenarios = ["Text Generation", "Real-Time Search", "Data Understanding", "Personal Life", "Application Manipulation", "Information Retrieval", "Financial Transactions"]
    for id, sce in enumerate(scenarios):
        print(f"-----Acc_{sce}-----")
        div = max_len / 7
        print("Tool Selection: " + "{:.2f}".format(check_list[0][id + 1] / div * 100))
        print("Parameter Identification: " + "{:.2f}".format(check_list[1][id + 1] / div * 100))
        print("Content Filling: " + "{:.2f}".format(check_list[2][id + 1] / div * 100))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_file", type=str)
    parser.add_argument("--answer_file", type=str)
    parser.add_argument("--version", type=int)

    args = parser.parse_args()
    test_file = args.test_file
    answer_file = args.answer_file
    version = args.version

    cata_list = get_cata_list(answer_file)
    check_list = []

    with open(test_file, encoding="utf-8") as f:
        test_data = json.load(f)
    with open(answer_file, encoding="utf-8") as f:
        answer_data = json.load(f)
    max_len = len(answer_data)
    if version:
        raven_eval(test_data, answer_data, version)
    else:
        general_eval(test_data, answer_data)
    show_stats(check_list, max_len)
