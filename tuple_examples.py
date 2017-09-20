#tuples

#work like lists, but can't be changed in place and usually written as series
#of items in parentheses, not brackets

#tuples are:
# 1) ordered collections of arbitrary objects
# 2) accessed by offset
# 3) of the category "immutable sequence"
# 4) fixed-length, heterogeneous, and arbitrarily nestable (e.g. they can
#    hold other compound objects such as lists, dicts, other tuples
# 5) arrays of object references

# empty tuple
t = ()

# one item tuple
print 'one-item tuple'
t = (0,)
print t[0]

# four-item tuple

print 'print 3rd item of a 4-item tuple'
t = (0, 'Nl', 1.2,3)
print t[2]
print 'fred'

#nested tuple

t= ('abc',('def','ghi'))
print 'print 2nd item of 2nd item in nested tuple'
print t[1][1]
