from json import dumps
from faker import Faker
import collections
import random


a = ["male", "female"]

database = []
filename = 'data'
length   = 7000
fake     = Faker() # <--- Forgot this

for x in range(length):
    database.append(collections.OrderedDict([
        ('age', fake.random_int(2, 19)),
        ('sex', random.choice(a)),
        ('weight', fake.random_int(60, 200)),
        ('SMN', fake.random_int(0,1))
    ]))

with open('%s.json' % filename, 'w') as output:
    output.write(dumps(database, indent=4))
print ("Done.")

