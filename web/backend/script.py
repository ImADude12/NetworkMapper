import sys
import json


# parse x:
y = json.loads(sys.argv[1])

# the result is a Python dictionary:
print(type(y[0]))
print('First param:'+y[0]['username'])