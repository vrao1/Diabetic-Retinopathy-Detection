import re
vision_threatning='E10.31*|E10.32*|E10.33*|E11.31*|E11.32*|E11.33*|E13.31*|E13.32*|E13.33*|362.01|362.03|362.04|362.05|250.5*'

non_vision_threatning='E10.34*|E10.35*|E11.34*|E11.35*|E13.34*|E13.35*|362.02|362.06'

fd = open("sample","r")
pat=fd.readlines()
fd.close()
table = {}

def get_values_if_any(d, key):
    return d.get(key, {}).keys(  )

for i in pat:
	i = i.strip()
	arr=i.split(' ')
	li = get_values_if_any(table, arr[0])
	if(len(li)>0):
		table.setdefault(arr[0], {})[arr[1]] = table.setdefault(arr[0], {})[arr[1]] + 1 
	else:
		table.setdefault(arr[0], {})[arr[1]] = 1 
	#print i

li = get_values_if_any(table, '89')
#pattern = 'E11*|36502|2505*'
pattern = 'E11*|36502'
print li
print "=============="
for i in table.keys():
	print get_values_if_any(table, i)
print "=============="
for b in li:
	k = re.sub(r'\.','', b)
	print "--------------------" + k
	if bool(re.match(pattern,k)):
		print "YES " + k
		print "YES " + pattern

	if bool(re.match(vision_threatning,k)):
		print "matched VT " + k
	elif bool(re.match(non_vision_threatning,k)):
		print "matched NVT"
	else:
		print "NO DR" 
 
del table
