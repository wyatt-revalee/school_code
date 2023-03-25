#!/usr/bin/env python3

s = ['a', 'b', 'c', 'd', 'e', 'r', 'a', 'r', 'c', 'a', 'd', 'b', 'a', 'c', 'r', 'a', 'c', 'e', 'c', 'a', 'r', 'r', 'o', 'c', 'k', 'c', 'o']

# n = len(s)

# # for i in range(1, n):
# #     m[i][i] = 1

# for j in range(1, n-1):
#     for i in range(1, n-j):
#         if(s[i] == s[i+j]):

class Solution(object):
   def longestPalindrome(self, s):
      dp = [[False for i in range(len(s))] for i in range(len(s))]
      for i in range(len(s)):
         dp[i][i] = True
      print(dp)
        
      max_length = 1
      start = 0
      for l in range(2,len(s)+1):
         for i in range(len(s)-l+1):
            end = i+l
            if l==2:
               if s[i] == s[end-1]:
                  dp[i][end-1]=True
                  max_length = l
                  start = i
            else:
               if s[i] == s[end-1] and dp[i+1][end-2]:
                  dp[i][end-1]=True
                  max_length = l
                  start = i
      return s[start:start+max_length]
ob1 = Solution()
print(ob1.longestPalindrome(s))
