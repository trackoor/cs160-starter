# error: 4:10
# a for loop needs a str or a list type [T]; [] has type <Empty>
x: int = 0
for x in []:
    print(x)
