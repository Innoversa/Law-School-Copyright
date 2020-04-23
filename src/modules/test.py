from math import sqrt 

def solve(a,b,c):
    i = sqrt(b**2-4 * a * c)
    x = (-1*b + i)/(2*a)
    y = (-1*b - i)/(2*a)
    return x,y

print(solve(0,2,1))