import re

file = open("stuff.txt",'r')
totalwords=0
for line in file:
    print(re.findall(r"[\w']+", line))
    totalwords+=len(re.findall(r"[\w']+", line))

print(totalwords)