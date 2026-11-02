data: [int] = None

def bubble_sort(xs: [int]):
    n: int = 0
    i: int = 0
    j: int = 0
    tmp: int = 0
    swapped: bool = True
    n = len(xs)
    while swapped:
        swapped = False
        j = 0
        while j < n - 1 - i:
            if xs[j] > xs[j + 1]:
                tmp = xs[j]
                xs[j] = xs[j + 1]
                xs[j + 1] = tmp
                swapped = True
            j = j + 1
        i = i + 1

def show(xs: [int]):
    x: int = 0
    for x in xs:
        print(x)

data = [5, -3, 8, 1, 9, 2, 7, 0, 6, 4]
bubble_sort(data)
show(data)
data = [2, 1]
bubble_sort(data)
show(data)
data = []
bubble_sort(data)
show(data)
data = [42, 42, 7]
bubble_sort(data)
show(data)
