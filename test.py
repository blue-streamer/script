import math
val=3000
sum=0
ratio=0.98
for year in range(10):
    sum += val * math.pow(ratio, year)

print(sum)
payback=val*10*math.pow(ratio, 20)
print(payback)
