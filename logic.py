import math
import csv
import pandas as pd
from collections import Counter


# =====================================================
# Combination generation
# =====================================================

def generate_combinations(data, start, path, all_possible, bar_length):
    current_sum = sum(path)
    if current_sum > bar_length:
        return

    if path:
        all_possible.append(tuple(path))

    for i in range(start, len(data)):
        if i > start and data[i] == data[i - 1]:
            continue
        generate_combinations(
            data, i + 1, path + [data[i]],
            all_possible, bar_length
        )


# =====================================================
# File loading helpers
# =====================================================

def load_requirements_from_csv(filename):
    req = []

    with open(filename, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0]:
                continue
            try:
                length = math.ceil(float(row[0]))
                qty = int(row[1]) if len(row) > 1 and row[1] else 1
                if length > 0 and qty > 0:
                    req.extend([length] * qty)
            except:
                continue

    if not req:
        raise ValueError("No valid rows found in CSV.")

    return sorted(req)


def load_requirements_from_excel(filename):
    req = []

    df = pd.read_excel(filename, header=None, engine="openpyxl")

    for _, row in df.iterrows():
        if pd.isna(row[0]):
            continue
        try:
            length = math.ceil(float(row[0]))
            qty = (
                int(row[1])
                if len(row) > 1 and not pd.isna(row[1])
                else 1
            )
            if length > 0 and qty > 0:
                req.extend([length] * qty)
        except:
            continue

    if not req:
        raise ValueError("No valid rows found in Excel.")

    return sorted(req)


# =====================================================
# Heuristic fallback
# =====================================================

def heuristic_first_fit_decreasing(cut_req, bar_length):
    bins = []
    for p in sorted(cut_req, reverse=True):
        placed = False
        for b in bins:
            if sum(b) + p <= bar_length:
                b.append(p)
                placed = True
                break
        if not placed:
            bins.append([p])
    return bins


# =====================================================
# Core optimizer
# =====================================================

def compute_all_combinations(cut_req, bar_length):
    data = sorted(cut_req)
    all_possible = []
    generate_combinations(data, 0, [], all_possible, bar_length)
    return list(dict.fromkeys(all_possible))


def optimize_cutting(cut_req, bar_length, progress_callback=None):
    """
    Returns a list of bars, each bar is a list of cut lengths
    """

    # Large problem → heuristic
    if len(cut_req) > 20:
        if progress_callback:
            progress_callback(10)
        result = heuristic_first_fit_decreasing(cut_req, bar_length)
        if progress_callback:
            progress_callback(100)
        return result

    all_possible = compute_all_combinations(cut_req, bar_length)
    if not all_possible:
        return []

    df = pd.DataFrame(all_possible)
    df["Sum"] = df.sum(axis=1)
    df = df.sort_values(by="Sum", ascending=False).reset_index(drop=True)

    remaining = cut_req.copy()
    schedule = []

    total = len(df)

    for i, row in df.iterrows():
        if progress_callback:
            progress_callback(int(100 * i / max(1, total)))

        cuts = row[:-1].dropna().tolist()
        if not cuts:
            continue

        if Counter(cuts) <= Counter(remaining):
            schedule.append(cuts)
            for c in cuts:
                remaining.remove(c)

    # Any leftovers become single bars
    for r in remaining:
        schedule.append([r])

    if progress_callback:
        progress_callback(100)

    return schedule


# =====================================================
# Utility helpers
# =====================================================

def bar_waste(bar, bar_length):
    return bar_length - sum(bar)


def total_waste(schedule, bar_length):
    return sum(bar_waste(bar, bar_length) for bar in schedule)
