import os

filename = "UKWKI"
language = "uk"
splits = 30

for i in range(1, splits+1):
    path = "{}\\{}\\data\\{}".format(filename, language, i)
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)

counter = 1
for x,y,z in os.walk(filename):
    for i in z:
        name = "{}\\{}\\data\\{}\\{}.title2id.txt".format(filename, language, counter, language)
        print(name, counter, i)
        os.rename(os.path.join(x, i), name)
        counter += 1
