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
        if data["verdict"] == "ok" and "score" in data:
            score += get_score(data["score"])
    return round(score / tests_count, 0)

print(verdict(80))
