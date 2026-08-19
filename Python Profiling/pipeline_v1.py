import time
import random
import math


def generate_data(n=10_000_000):
    data = []

    for i in range(n):
        data.append({
            "id": i,
            "price": random.uniform(10, 1000),
            "quantity": random.randint(1, 20),
            "category": random.choice(["A", "B", "C", "D"]),
        })

    return data


def calculate_score(row):
    price = row["price"]
    quantity = row["quantity"]

    result = 0

    for i in range(100):
        result += math.sqrt(price * quantity + i)

    return result


def transform_data(data):

    result = []

    for row in data:

        # محاسبه مبلغ
        amount = row["price"] * row["quantity"]

        # محاسبه مصنوعی و سنگین
        score = calculate_score(row)

        # چند شرط پردازشی
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
            "score": score,
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

    # برای اینکه بتوانیم Process را با py-spy مانیتور کنیم
    print("\nPipeline finished.")