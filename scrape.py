import httpx
import json


def fetch_api_data(payload) -> list:
    URL = "https://cs-search-api-prod.collegeplanning-prod.collegeboard.org/colleges"

    response = httpx.post(URL, json=payload)
    json_content = response.json()
    return json_content["data"]


def load_data_full() -> list:
    result = fetch_api_data(
        {
            "eventType": "search",
            "eventData": {
                "config": {"size": 4434, "from": 0, "highlight": "name"},
                "criteria": {"rmsInputField": "", "rmsInputValue": ""},
            },
        }
    )

    return result


def load_data_paged() -> list:
    result = []

    # 45 batches of 100 should be give us the 44xx items as a result
    for i in range(45):
        batch_size = 100
        offset = i * batch_size
        batch = fetch_api_data(
            {
                "eventType": "search",
                "eventData": {
                    "config": {"size": batch_size, "from": offset, "highlight": "name"},
                    "criteria": {"rmsInputField": "", "rmsInputValue": ""},
                },
            }
        )
        result += batch
        print(f"...added batch of {batch_size} items")

    return result


def store_data(filename: str, content: str):
    """
    Rewrites the filename with the content, expects a directory called data/ to exist
    """

    with open(filename, "w") as file:
        file.write(content)


if __name__ == "__main__":
    result = load_data_full()
    # result = load_data_paged()
    # print(len(result))
    # print(result[0])

    school_names = sorted([item["name"] for item in result])
    school_names_content = "\n".join(school_names)
    store_data("data/schools.txt", school_names_content)

    school_name_id_map = sorted(
        [{"id": item["orgId"], "name": item["name"]} for item in result],
        key=lambda x: x["name"],
    )
    school_name_id_content = "\n".join(
        [f"{item["name"]},{item["id"]}" for item in school_name_id_map]
    )
    store_data("data/schools.csv", school_name_id_content)

    school_data = [(item["orgId"], item) for item in result]
    for school_id, school_item in school_data:
        school_blob = json.dumps(school_item)
        store_data(f"data/{school_id}.json", school_blob)


# result size => 4434
# result sample item / first item => {
#     "orgId": "913",
#     "name": "California State University: Dominguez Hills",
#     "city": "Carson",
#     "state": "CA",
#     "zipCode": "90747",
#     "stateName": "California",
#     "country": "US",
#     "countryName": "United States of America",
#     "schoolSetting": "suburban",
#     "schoolTypeByDesignation": "public",
#     "schoolTypeByYears": 4,
#     "schoolSize": "large",
#     "averageNetPrice": 4500,
#     "graduationRate": 53,
#     "satOrAct": None,
#     "rmsFitness": None,
#     "rsatMathScore25thPercentile": 370,
#     "rsatMathScore75thPercentile": 450,
#     "rsatEbrwScore25thPercentile": 400,
#     "rsatEbrwScore75thPercentile": 480,
#     "satCompositeScore25thPercentile": 790,
#     "satCompositeScore75thPercentile": 930,
#     "actCompositeScore25thPercentile": 15,
#     "actCompositeScore75thPercentile": 15,
#     "apPlacementAwarded": True,
#     "apCreditAwarded": True,
#     "apInstPolicyUrl": "https://catalog.csudh.edu/general-information/baccalaureate-degrees-undergraduate-studies/",
#     "apInstPolicyDescription": "The University grants credit toward the undergraduate degree for the successful passage of the examinations of the Advanced Placement Program (AP). Students who present scores of 3, 4 or 5 on one or more AP examination will be awarded university credit. Students who have taken AP Examinations should request that official scores be sent to the Office of Admissions.",
#     "vocationalSchool": False,
#     "vanityUri": "california-state-university-dominguez-hills",
#     "redirectUris": [],
#     "socialMedia": {
#         "youtube": [],
#         "twitter": [],
#         "other": [],
#         "facebook": [],
#         "instagram": [],
#         "linkedin": [],
#     },
# }
