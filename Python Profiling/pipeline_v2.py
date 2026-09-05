import time
import random
import math
import numpy as np
random.seed(42)

def generate_data(n=5_000_000):
    data = []

    for i in range(n):
        data.append({
            "id": i,
            "price": random.uniform(10, 1000),
            "quantity": random.randint(1, 20),
            "category": random.choice(["A", "B", "C", "D"]),
        })

    return data


def calculate_scores(prices, quantities):
    """
    Vectorized score calculation using NumPy.
    """

    base = prices * quantities

    i = np.arange(100)

    scores = np.sqrt(base[:, None] + i).sum(axis=1)

    return scores


def transform_data(data):

    result = []

    batch_size = 5_000

    for start in range(0, len(data), batch_size):

        batch = data[start:start + batch_size]

        prices = np.array(
            [row["price"] for row in batch],
            dtype=np.float64
        )

        quantities = np.array(
            [row["quantity"] for row in batch],
            dtype=np.float64
        )

        scores = calculate_scores(prices, quantities)

        for row, score in zip(batch, scores):

            amount = row["price"] * row["quantity"]

            if amount > 5000:
                level = "HIGH"

            elif amount > 2000:
                level = "MEDIUM"

            else:
                level = "LOW"

            result.append({
                "id": row["id"],
                "category": row["category"],
                "amount": amount,
                "score": float(score),
                "level": level
            })

    return result


def aggregate_data(data):

    result = {}

    for row in data:

        category = row["category"]

        if category not in result:
            result[category] = {
                "count": 0,
                "amount": 0,
                "score": 0
            }

        result[category]["count"] += 1
        result[category]["amount"] += row["amount"]
        result[category]["score"] += row["score"]

    return result


def etl_pipeline():

    print("Generating data...")
    data = generate_data()

    print("Transforming data...")
    transformed = transform_data(data)

    print("Aggregating data...")
    result = aggregate_data(transformed)

    print("\nResult:")

    for category, values in result.items():
        print(category, values)


if __name__ == "__main__":

    start = time.time()

    etl_pipeline()

    print(f"\nExecution time: {time.time() - start:.2f} seconds")

    print("\nPipeline finished.")