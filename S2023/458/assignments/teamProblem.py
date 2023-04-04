# Find a subset of vertices that are independent that has a maximum total weight.

# if v(i) is adjacent to v(j) then v(i) is adjacent to v(i+1), v(i+2), ... , v(j-1)
# ex:
# set [4, 7, 10, 2, 19, 14, 3, 12, 15, 7, 1]

# adjacencies (of indices) [0, 2], [2, 4], [4, 6], [6, 8], [8, 10]

# set[2] 10, set[5] 14, set[8], 15

# weight = 29

s =  [4, 7, 10, 2, 19, 14, 3, 12, 15, 7, 1]
solSet = [0] * len(s)
solSet[0], solSet[1] = s[0], s[1]

for i in range(2, len(s)):
    solSet[i] = max(solSet[i-1], solSet[i-2] + s[i])

print(solSet)

#first two elements will always have their own respective weights
#for each element, k, the max weight is the max of its weight plus the previous independent set (k-i) or the previous max ( max(s[k-1], s[k] + s[k-i]))