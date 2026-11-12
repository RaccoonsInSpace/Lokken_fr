user = "raccoons"
names = [("test",1),("zest",2)]
currencies = []
for name in names:
    currencies.append(f":{name[0]}: {name[1]},")

list = [",".join(currencies)]

print(*currencies)