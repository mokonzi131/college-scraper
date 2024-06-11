import dataclasses
import json
import httpx


@dataclasses.dataclass(frozen=True)
class Data:
    id: int = dataclasses.field()
    name: str = dataclasses.field(default="")
    values: list[float] = dataclasses.field(default_factory=list)


# 1. the basics of the http client you'd like to use (how to POST, how to set headers)
def http_client_sample():
    response = httpx.get(
        "https://httpbin.org/get",
        params={"P1": "hello", "P2": "world"},
        headers={"user-agent": "me/0.1"},
    )
    print(f"Response: {response.status_code} = {response.json()}")

    response = httpx.post(
        "https://httpbin.org/post",
        params={"P1": "hi"},
        data={"KEY": "value", "LST": ["a", "b", "c"]},
    )
    print(f"Response: {response.status_code} = {response.json()}")


# 1. some JSON lib for parsing
def json_sample():
    data = [
        Data(0, "A", [1.1, 2.2]),
        Data(1, "B", [2.2, 4.4]),
        Data(2, "C", [5.5, 6.6]),
    ]

    print(data)
    print([dataclasses.asdict(d) for d in data])


# 1. how you might persist JSON blobs (either using something like sqlite or just storing on the file system)
def persistence_sample():
    id = 0
    data = {"id": 0, "name": "A", "reading": 1.23}
    blob = json.dumps(data)

    with open(f"data/{id}.json", "w") as file:
        file.write(blob)


if __name__ == "__main__":
    http_client_sample()
    json_sample()
    persistence_sample()
