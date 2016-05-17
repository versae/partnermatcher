import asyncio
import itertools
import json
import sys

from aiohttp import web
from Levenshtein import median

from utils import get_list_response, similarity_score, get_domains, MESSAGES


async def home_view(request):
    return web.Response(body=str.encode(json.dumps(MESSAGES)))

async def names_view(request):
    names, response = get_list_response(request, "name")
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
        response = {
            "names": names,
            "average": average,
            "matrix": sorted(matrix, key=lambda x: -x["score"])
        }
    return web.Response(body=str.encode(json.dumps(response)))

async def domains_view(request):
    domains, response = get_list_response(request, "domain")
    lower = request.GET.get("lower")
    algorithm = request.GET.get("algorithm")
    if domains:
        domains = [n.strip() for n in domains]
        response = {
            "domains": domains,
            "unique": tuple(get_domains(domains)),
        }
    return web.Response(body=str.encode(json.dumps(response)))

def init(argv):
    app = web.Application()
    app.router.add_route('GET', '/', home_view)
    app.router.add_route('GET', '/names', names_view)
    app.router.add_route('GET', '/domains', domains_view)
    return app

app = init(sys.argv)
if __name__ == "__main__":
    web.run_app(app)