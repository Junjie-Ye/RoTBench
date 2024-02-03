import requests


def get_response(url, headers, **kargs):
    response = requests.get(url, headers=headers, params=kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation

def get_response_post(url, headers, **kargs):
    response = requests.get(url, headers=headers, data=kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation

def inferkit_text_gen(
    length: int,
    prompt: str,
    topP: float=0.9,
    temperature: float=1.0,
):
    url = "https://api.inferkit.com/v1/models/standard/generate"

    params = {
        "prompt": {'text':prompt},
        "length": length,
        "topP": topP,
        "temperature": temperature,
    }

    headers = {
    }
    return get_response(url, headers, **params)

def cohere_text_gen(
    prompt: str,
    num_generations:int=1,
    max_tokens: int=None,
    truncate: str='END',
    k: int=500,
    p: float=0.75,
    temperature: float=0.75,
    return_likelihoods: str='NONE',
    presence_penalty: float=0.0,
):
    url = "https://api.cohere.ai/v1/generate"

    params = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "p": p,
        "k": k,
        'truncate':truncate,
        'temperature':temperature,
        'return_likelihoods':return_likelihoods,
        'presence_penalty':presence_penalty,
        'num_generations':num_generations
    }

    headers = {
        'accept':'application/json',
        'content-type': 'application/json'
    }
    return get_response_post(url, headers, **params)

if __name__ == "__main__":
    # print(get_daily_calory_requirement(25, "male", 180, 70, "level_1"))
    # print(get_calories_burned("bi_1", 25, 75))
    # print(get_bmi(25, 180,75))
    # print(get_macro_nutrients_amount(25, "male", 180, 70, 5, "extremelose"))
    # print(get_body_fat_percentage(25, "male", 178, 70, 50, 96, 92))
    # print(get_ideal_weight("male", 180))
    # print(get_food_info("SR25_1_1"))
    # print(get_foodtable_ids("Fo1_2"))
    # print(get_subtable_names("Su10"))
    # print(get_maintable_names())
    # print(get_acitcity_met_values(1))
    pass
