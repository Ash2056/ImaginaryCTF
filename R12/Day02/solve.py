from base import *
from secretpy import *
x = dumpPub(API.get(1))
submit(Rot47().decrypt(x.attachments))
