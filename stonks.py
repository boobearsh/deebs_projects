# Stock Prices [List]

stock_prices = [34.68, 36.09, 34.94, 33.97, 34.68, 35.82, 43.41, 44.29, 44.65,
                53.56, 49.85, 48.71, 48.71, 49.94, 48.53, 47.03, 46.59, 48.62, 44.21, 47.21]


def price_at(i):
    return stock_prices[i-1]


def max_price(a, b):
    price_max = 0
    for i in range(a, b + 1):
        mx = max(price_max, price_at(i))
    return mx


def min_price(a, b):
    price_min = price_at(a)
    for i in range(a, b + 1):
        mn = min(price_min, price_at(i))
    return mn


print(max_price(1, 15))
print(min_price(5, 10))
print(price_at(3))
