import asyncio
import itertools
import json
import sys

from aiohttp import web
from Levenshtein import distance, jaro, jaro_winkler, median, ratio


async def home(request):
    if "name" in request.GET:
        names = request.GET.getall("name")
    elif "names" in request.GET:
        names = request.GET.get("names").split(",")
    else:
        names = None
        response = {"message": ("Please, send some names to compare. Ej: "
                                "?name=oneligin&name=OneLogin%20Inc.")}
    lower = request.GET.get("lower")
    algorithm = request.GET.get("algorithm")
    if names:
        names = [n.strip() for n in names]
        matrix = []
        for pair in itertools.combinations(names, 2):
            score = await similarity_score(*pair, algorithm=algorithm,
                                           lower=lower)
            matrix.append({"pair": pair, "score": score})
        average = median(names)
        response = {"names": names, "average": average, "matrix": matrix}
    return web.Response(body=str.encode(json.dumps(response)))

async def similarity_score(name1, name2, algorithm=None, lower=False):
    if lower:
        str1, str2 = name1.lower(), name2.lower()
    else:
        str1, str2 = name1, name2
    if algorithm == "levenshtein":
        distance_func = distance
    elif algorithm == "jaro":
        distance_func = jaro
    elif algorithm == "ratio":
        distance_func = ratio
    else:
        distance_func = jaro_winkler
    print(distance_func)
    return distance_func(str1, str2)

def init(argv):
    app = web.Application()
    app.router.add_route('GET', '/', home)
    return app

app = init(sys.argv)
if __name__ == "__main__":
    web.run_app(app)