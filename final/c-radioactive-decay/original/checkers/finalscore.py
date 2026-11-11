#!/usr/bin/python3

import json


def get_score(data):
    if "longScore" in data:
        return int(data["longScore"])
    elif "doubleScore" in data:
        return int(data["doubleScore"])
    return 0


def verdict(tests_count: int):
    testData = json.loads(input())["tests"]
    score = 0
    for data in testData:
        if "score" in data and data["verdict"] == "ok":
            score += get_score(data["score"])
    return int(score / tests_count)

print(verdict(80))
