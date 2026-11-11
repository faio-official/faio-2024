import math

n = int(input())
X = []
targets = []
for i in range(n):
    y, x = map(float, input().split())
    X.append(x)
    targets.append(y)

Y = [math.log(y, 10) for y in targets]
yx = [x * y for x, y in zip(X, Y)]
x2 = [x ** 2 for x in X]

numerator = sum(yx) - sum(X) * sum(Y) / n
denominator = sum(x2) - sum(X) ** 2 / n
a = numerator / denominator

t0 = -math.log(2, 10) / a

print(t0)
