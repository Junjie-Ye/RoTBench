# from serpapi import GoogleSearch
import serpapi


def apps_related_searches(q: str, api_key: str = "6d1b8e862feb920f015695cfadf336d0f0aeaabc48b4e390578567d9712001cb"):
    params = {
        "engine": "google_play",
        "store": "apps",
        "q": q,
        "api_key": api_key
    }

    # search = GoogleSearch(params)
    results = serpapi.search(**params)
    # results = search.get_dict()
    try:
        ret = results["app_highlight"]
    except:
        try:
            ret = results["organic_results"]
        except:
            ret = results

    return ret


def books_related_searches(q: str, price: int = None, api_key: str = "6d1b8e862feb920f015695cfadf336d0f0aeaabc48b4e390578567d9712001cb"):
    params = {
        "engine": "google_play_books",
        "q": q,
        "price": price,
        "api_key": api_key
    }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        ret = results["organic_results"][0]["items"][:5]
    except:
        ret = results

    return ret


def games_related_searches(q: str, api_key: str = "6d1b8e862feb920f015695cfadf336d0f0aeaabc48b4e390578567d9712001cb"):
    params = {
        "engine": "google_play_games",
        "q": q,
        "api_key": api_key
    }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        ret = results["organic_results"][0]["items"][:5]
    except:
        ret = results

    return ret


def movies_related_searches(q: str, api_key: str = "6d1b8e862feb920f015695cfadf336d0f0aeaabc48b4e390578567d9712001cb"):
    params = {
        "engine": "google_play_movies",
        "q": q,
        "api_key": api_key
    }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        ret = results["organic_results"][0]["items"][:5]
    except:
        ret = results

    return ret


if __name__ == '__main__':
    # print(books_related_searches('Coffee'))
    print(games_related_searches('weather'))
    pass
