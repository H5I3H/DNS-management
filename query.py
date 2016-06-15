#!/usr/bin/env python
import sys
f = open('/var/log/named/query.log')
fields = []
time_list = []
for line in f:
	fields.append(line.split(' ')[8])
	time_list.append("{} {}".format(line.split(' ')[0], line.split(' ')[1]))
A = 0
AAAA = 0
CNAME = 0
NS = 0
unknown = 0
for cur in fields:
	if cur == 'A':
		A = A + 1
	elif cur == 'AAAA':
		AAAA = AAAA + 1
	elif cur == 'CNAME':
		CNAME = CNAME + 1
	elif cur == 'NS':
		NS = NS + 1
	else:
		unknown = unknown + 1

print(A)
print(AAAA)
print(CNAME)
print(NS)
print(time_list[0])
print(time_list[-1])
