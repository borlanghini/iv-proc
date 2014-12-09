#!/usr/bin/env python
import numpy as np

error = None
fh = None
array=[]
arraynp = np.zeros((0,2))

fh = open("/home/julio/programming/python/proyectos/IV-proc/20120131_X_light1.txt",  "r")
lino = 0
for line in fh:
  if not line or line.startswith(("#", "\n", "\r")):
    continue
  line = line.rstrip()
  fields = line.split("\t")
  print fields
  array.append([float(fields[0]), float(fields[1])])

print array
arraynp = np.asarray(array)
print arraynp

print type(array)
print len(arraynp)
print np.flipud(arraynp)
