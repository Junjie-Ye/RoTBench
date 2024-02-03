import json
import argparse


# NexusRaven_v1
def version1(origin_file, raven_file):
    with open(origin_file, encoding="utf-8") as f:
        data = json.load(f)

    prompt_data = []
    for d in data:
        p_len = len(d["conversations"][0]["value"][:d["conversations"][0]["value"].find("[")])
        config = json.loads(d["conversations"][0]["value"][p_len:-13])
        query = d["conversations"][1]["value"][:-8]
        prompt_template = ""
        prompt_template += "<human>:\n"
        for function in config:
            prompt_args = []
            for arg, detail in function["parameters"]["properties"].items():
                prompt_args.append("{arg} : {type}".format(arg=arg, type=detail["type"]))
            prompt_template += "OPTION:\n<func_start>def {name}({args})<func_end>\n".format(name=function["name"], args=", ".join(prompt_args))
            prompt_template += "<docstring_start>\n\"\"\"\n{function_des}\n".format(function_des=function["description"])
            if prompt_args:
                prompt_template += "\nArgs:\n"
                for arg, detail in function["parameters"]["properties"].items():
                    prompt_template += "{arg} ({type}) : {arg_des}\n".format(arg=arg, type=detail["type"], arg_des=detail["description"])
            prompt_template += "\"\"\"\n<docstring_end>\n\n"
        prompt_template += "User Query: Question: {question}\n\n".format(question=query)
        prompt_template += "Please pick a function from the above options that best answers the user query and fill in the appropriate arguments.<human_end>"
        prompt_data.append({"id": d["id"], "prompt": prompt_template, "scenario": d["scenario"]})

    with open(raven_file, "w", encoding="utf-8") as w:
        json.dump(prompt_data, w, indent=4, ensure_ascii=False)


# NexusRaven_v2
def version2(origin_file, raven_file):
    with open(origin_file, encoding="utf-8") as f:
        data = json.load(f)

    prompt_data = []
    for d in data:
        p_len = len(d["conversations"][0]["value"][:d["conversations"][0]["value"].find("[")])
        config = json.loads(d["conversations"][0]["value"][p_len:-13])
        query = d["conversations"][1]["value"][:-8]
        prompt_template = ""
        for function in config:
            prompt_args = []
            for arg, detail in function["parameters"]["properties"].items():
                prompt_args.append("{arg} : {type}".format(arg=arg, type=detail["type"]))
            prompt_template += "Function:\ndef {name}({args}):\n".format(name=function["name"], args=", ".join(prompt_args))
            prompt_template += "\"\"\"\n{function_des}\n".format(function_des=function["description"])
            if prompt_args:
                prompt_template += "\nArgs:\n"
                for arg, detail in function["parameters"]["properties"].items():
                    if arg not in function["parameters"]["required"]:
                        prompt_template += "{arg} (Optional): {arg_des}\n".format(arg=arg, arg_des=detail["description"])
                    else:
                        prompt_template += "{arg}: {arg_des}\n".format(arg=arg, arg_des=detail["description"])
            prompt_template += "\"\"\"\n\n"
        prompt_template += "User Query: {query}<human_end>\n\n".format(query=query)
        prompt_data.append({"id": d["id"], "prompt": prompt_template, "scenario": d["scenario"]})

    with open(raven_file, "w", encoding="utf-8") as w:
        json.dump(prompt_data, w, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=int)
    parser.add_argument("--origin_file", type=str)
    parser.add_argument("--raven_file", type=str)

    args = parser.parse_args()
    version = args.version
    origin_file = args.origin_file
    raven_file = args.raven_file

    if version == 1:
        version1(origin_file, raven_file)
    if version == 2:
        version2(origin_file, raven_file)
