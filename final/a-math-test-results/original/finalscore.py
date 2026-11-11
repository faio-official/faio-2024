#!/usr/bin/python3

import json



def get_score(data):
    if "longScore" in data:
        return int(data["longScore"])
    elif "doubleScore" in data:
        return int(data["doubleScore"])
    return 0


def verdict():
    testData = json.loads(input())["tests"]
    score = 0
    for data in testData:
        if data["verdict"] == "ok":
            score = 100
    return score


print(verdict())
