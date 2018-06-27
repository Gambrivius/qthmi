i = 0

# on
i |= 1<<1
i |= 1<<2
print (i)

#off
i &= ~(1<<1)
print (i)

#get
print ((i >> 2) & 1)