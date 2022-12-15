#!/usr/bin/env python3

li = ["cat", "dog", "bird"]

# def foo(x):
#     return x.upper()

m = map(lambda x: x.upper(), li)

print(list(m))

#List Comprehension

uppers = [ item.upper() for item in li ]
print(uppers)


#Generator Comprehensions
g_uppers = ( item.upper() for item in li )
print(g_uppers)
print(next(g_uppers))
print(next(g_uppers))
print(next(g_uppers))

# Dictionary Comprehensions

di = { item:item.upper() for item in li }
print(di)

# Ternaries

x = 5 if True else 7
print(x)
x = 5 if False else 7
print(x)
