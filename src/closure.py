def count():
    fs = []
    def f(j):
        def g():
            return j * j
        return g
    for i in range(1, 4):
        j = i
        
        fs.append(f(j))
    return fs

def sum():
    fs = []

    for i in range(1, 4):
        j = i
        def f(j):
            return j * j
        fs.append(f(j))

    print(fs)
    return fs

f1, f2, f3 = sum()

print(f1())
print(f2())
print(f3())