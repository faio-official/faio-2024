#!/usr/bin/env python3
"""FAIO 2024 C "Radioactive decay" — algorun per-test checker.

Called as: checker.py <input_path> <expected_path> <user_output_path>
Prints one JSON line: {"score": float, "verdict": str, "message": str}.

The participant estimates the half-life T0. A test passes (100) when the answer is
within 1% relative error of the jury value, otherwise 0 — identical to the original
Yandex checker (note: the original's argv order is input, user-output, answer; here
the answer is `expected_path` and the participant's number is `output_path`).
"""
import json
import sys

TOL = 0.01  # 1% relative error


def check(input_path, expected_path, output_path):
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            prediction = float(f.readline().split()[0])
    except Exception:
        return 0.0, "PE", "Could not read a number from your output."
    try:
        with open(expected_path, "r", encoding="utf-8") as f:
            target = float(f.readline().split()[0])
    except Exception:
        return 0.0, "WA", "Checker: could not read the expected answer."
    if target == 0:
        return (100.0, "OK", "Correct") if prediction == 0 else (0.0, "WA", "Incorrect.")
    percent = abs((target - prediction) / target)
    if percent < TOL:
        return 100.0, "OK", f"Within 1% (relative error {percent*100:.3f}%)."
    return 0.0, "WA", f"Relative error {percent*100:.3f}% (must be < 1%)."


def main():
    input_path, expected_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]
    score, verdict, message = check(input_path, expected_path, output_path)
    print(json.dumps({"score": float(score), "verdict": verdict, "message": message}))


if __name__ == "__main__":
    main()
