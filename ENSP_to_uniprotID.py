import glob
import math
import os
import re
import time
import json
import zlib
from xml.etree import ElementTree
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from requests.adapters import HTTPAdapter, Retry


POLLING_INTERVAL = 3
API_URL = "https://rest.uniprot.org"


retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retries))


def check_response(response):
    try:
        response.raise_for_status()
    except requests.HTTPError:
        print(response.json())
        raise


def submit_id_mapping(from_db, to_db, ids):
    request = requests.post(
        f"{API_URL}/idmapping/run",
        data={"from": from_db, "to": to_db, "ids": ",".join(ids)},
    )
    check_response(request)
    return request.json()["jobId"]


def get_next_link(headers):
    re_next_link = re.compile(r'<(.+)>; rel="next"')
    if "Link" in headers:
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)


def check_id_mapping_results_ready(job_id):
    while True:
        request = session.get(f"{API_URL}/idmapping/status/{job_id}")
        check_response(request)
        j = request.json()
        if "jobStatus" in j:
            if j["jobStatus"] == "RUNNING":
                print(f"Retrying in {POLLING_INTERVAL}s")
                time.sleep(POLLING_INTERVAL)
            else:
                raise Exception(j["jobStatus"])
        else:
            return bool(j["results"] or j["failedIds"])


def get_batch(batch_response, file_format, compressed):
    batch_url = get_next_link(batch_response.headers)
    while batch_url:
        batch_response = session.get(batch_url)
        batch_response.raise_for_status()
        yield decode_results(batch_response, file_format, compressed)
        batch_url = get_next_link(batch_response.headers)


def combine_batches(all_results, batch_results, file_format):
    if file_format == "json":
        for key in ("results", "failedIds"):
            if key in batch_results and batch_results[key]:
                all_results[key] += batch_results[key]
    elif file_format == "tsv":
        return all_results + batch_results[1:]
    else:
        return all_results + batch_results
    return all_results


def get_id_mapping_results_link(job_id):
    url = f"{API_URL}/idmapping/details/{job_id}"
    request = session.get(url)
    check_response(request)
    return request.json()["redirectURL"]


def decode_results(response, file_format, compressed):
    if compressed:
        decompressed = zlib.decompress(response.content, 16 + zlib.MAX_WBITS)
        if file_format == "json":
            j = json.loads(decompressed.decode("utf-8"))
            return j
        elif file_format == "tsv":
            return [line for line in decompressed.decode("utf-8").split("\n") if line]
        elif file_format == "xlsx":
            return [decompressed]
        elif file_format == "xml":
            return [decompressed.decode("utf-8")]
        else:
            return decompressed.decode("utf-8")
    elif file_format == "json":
        return response.json()
    elif file_format == "tsv":
        return [line for line in response.text.split("\n") if line]
    elif file_format == "xlsx":
        return [response.content]
    elif file_format == "xml":
        return [response.text]
    return response.text


def get_xml_namespace(element):
    m = re.match(r"\{(.*)\}", element.tag)
    return m.groups()[0] if m else ""


def merge_xml_results(xml_results):
    merged_root = ElementTree.fromstring(xml_results[0])
    for result in xml_results[1:]:
        root = ElementTree.fromstring(result)
        for child in root.findall("{http://uniprot.org/uniprot}entry"):
            merged_root.insert(-1, child)
    ElementTree.register_namespace("", get_xml_namespace(merged_root[0]))
    return ElementTree.tostring(merged_root, encoding="utf-8", xml_declaration=True)


def print_progress_batches(batch_index, size, total):
    n_fetched = min((batch_index + 1) * size, total)
    print(f"Fetched: {n_fetched} / {total}")


def get_id_mapping_results_search(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    file_format = query["format"][0] if "format" in query else "json"
    if "size" in query:
        size = int(query["size"][0])
    else:
        size = 500
        query["size"] = size
    compressed = (
        query["compressed"][0].lower() == "true" if "compressed" in query else False
    )
    parsed = parsed._replace(query=urlencode(query, doseq=True))
    url = parsed.geturl()
    request = session.get(url)
    check_response(request)
    results = decode_results(request, file_format, compressed)
    total = int(request.headers["x-total-results"])
    print_progress_batches(0, size, total)
    for i, batch in enumerate(get_batch(request, file_format, compressed), 1):
        results = combine_batches(results, batch, file_format)
        print_progress_batches(i, size, total)
    if file_format == "xml":
        return merge_xml_results(results)
    return results


def get_id_mapping_results_stream(url):
    if "/stream/" not in url:
        url = url.replace("/results/", "/results/stream/")
    request = session.get(url)
    check_response(request)
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    file_format = query["format"][0] if "format" in query else "json"
    compressed = (
        query["compressed"][0].lower() == "true" if "compressed" in query else False
    )
    return decode_results(request, file_format, compressed)

## this is adapted from https://www.uniprot.org/help/id_mapping exmaple

# import IDs
import pandas as pd


def get_ENSP_IDs(path_to_xlsx, xlsx):
    df = pd.read_excel(path_to_xlsx + xlsx)
    ENSP_IDs = df['stringId_B']
    return(ENSP_IDs.tolist())


def get_ID_from_mapping_API(id_list):
    # get 500 IDs at a time!
    result = []
    runs_needed = math.ceil(len(id_list)/500)
    ids_left = len(id_list)

    for run in range(runs_needed):
        ids_left = ids_left-500
        if ids_left < 0: ids_left = 0

        ids_subset = id_list[run*500: len(id_list)-ids_left]

        job_id = submit_id_mapping(
            from_db="STRING", to_db="UniProtKB", ids=ids_subset
        )
        if check_id_mapping_results_ready(job_id):
            link = get_id_mapping_results_link(job_id)
            uni_entries = get_id_mapping_results_search(link)

            print("hEEEERE")
            print(len(ids_subset))

            for i in range(len(ids_subset)):
                # print(i)
                # print(uni_entries['results'][i]['to']['primaryAccession'])
                result += [uni_entries['results'][i]['to']['primaryAccession']]
    return(result)


# import interactors retrieved from strinDB via get_stringDB.py
# homeoffice path
# path = 'C:/Users/monar/Google Drive/Arbeit/homeoffice/230103_RH review/barr1+2 interactome/stringDB_data/'
# IMZ path
path = 'B:/FuL/IMZ01/Hoffmann/Personal data folders/Mona/Paper/XXX_Haider et al_Review/barr1+2 interactome/stringDB_data/'

extension = 'xlsx'
os.chdir(path)
filenames = glob.glob('*.{}'.format(extension))


# ODER
# for each xlsx sheet in dilenames
df = pd.read_excel(path + filenames[3])
ENSP_IDs = df['stringId_B']

print(get_ENSP_IDs(path,filenames[0]))

print(filenames[3])
print(get_ID_from_mapping_API(ENSP_IDs))




####

# job_id = submit_id_mapping(
#     from_db="STRING", to_db="UniProtKB", ids=["9606.ENSP00000351805", "9606.ENSP00000337383"]
# )
# if check_id_mapping_results_ready(job_id):
#     link = get_id_mapping_results_link(job_id)
#     results = get_id_mapping_results_search(link)
#     # Equivalently using the stream endpoint which is more demanding
#     # on the API and so is less stable:
#     # results = get_id_mapping_results_stream(link)



# from "STRING" to "UniProtKB_AC-ID" was not valid
# "UniProtKB" returns entire entry; thus script retrieves only ACC ID in entry
# results are nested dictionary


# print(type(results))
# # print(results['results']['from']) #does not work
#
# # this is a list
# test1 = results['results']
# print(type(test1))
# print(test1[0]['to']['primaryAccession'])
#
# # i is index of ID
# i = 0
# print(results['results'][i]['to']['primaryAccession'])
#
