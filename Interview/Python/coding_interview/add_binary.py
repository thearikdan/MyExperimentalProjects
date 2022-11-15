class Solution:
    def plusOne(self, a, b):
        a_bin = int(a,2)
        b_bin = int(b,2)
        res = bin(a_bin + b_bin)
        return str(res)[2:]


a = "11"
b = "1"

s = Solution()
sum = s.plusOne(a, b)
print(sum)