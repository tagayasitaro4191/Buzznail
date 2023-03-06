from __future__ import unicode_literals
import requests
import youtube_dl
import torch
import numpy as np
from operator import itemgetter
ydl_opts = {}

a = torch.rand(4,3)
value, index = a.max(dim=-1)

b = [100, 200, 300, 400]

print(a)

print(value)

print(index)

value = torch.sort(value, dim=1)

print(value)

output = itemgetter(*(index+1))(b)

print(output)




