import asyncio
from urllib.parse import urlparse

from Levenshtein import distance, hamming, jaro, jaro_winkler, median, ratio

MESSAGES = {
    "names": ("Send some names to compare. Ej: "
              "?name=oneligin&name=OneLogin%20Inc."),
    "domains": ("Send some domains and URLs to get the canonical one. "
                "Ej: ?domain=google.com&domain=https://www.google.com"),
}

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
    elif algorithm == "hamming":
        distance_func = hamming
    else:
        distance_func = jaro_winkler
    return distance_func(str1, str2)

def get_list_response(request, variable):
    response = None
    if variable in request.GET:
        result = request.GET.getall(variable)
    elif variable + "s" in request.GET:
        result = request.GET.get(variables + "s").split(",")
    else:
        result = None
        if variable in ["name", "names"]:
            response = {"message": MESSAGES["names"]}
        elif variable in ["domain", "domains"]:
            response = {"message": MESSAGES["domains"]}
    return result, response

def get_domains(domains):
    result = set({})
    for domain in domains:
        if domain.startswith("http"):
            domain = urlparse(domain).netloc
        if domain.startswith("www."):
            domain = domain.replace("www.", "", 1)
        domain = domain.rsplit(":", 1)[0]
        result.add(domain)
    return result