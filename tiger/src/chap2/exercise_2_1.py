import re

# exercise 2.1.a
re.search("(a|c)*a(a|b|c)*")
# it works!

# exercise 2.1.b
re.search("((b|c)|a(b|c)*a)*")
#it works!

# exercise 2.1.c
re.search("(0|1)*100")
# it works!

# exercise 2.1.d
re.search("(0|1)*1(0|1)1(0|1)1(0|1)")

# exercise 2.1.e
# without baa
re.search("")

#             c, b
#         __________
#        |         |
#        v    b    |    a      c
#      start ----> 1  ----> 2 __
#      ^^ |         ^       |  |
#      ||_|         |_______|  |
#      |  a,c         b        |
#      |_______________________|


#              a,c
#            +---+
#            |   |
#            v   |
#   start -> 1 --+-<-----+
#            |           |
#            | b         |
#            v           | c
#            2 <--+      |
#            | a  |      |
#            v    | b    |
#            3----+      |
#            |           |
#            +-----------+


# exercise 2.3 a

# non accepting
# 0110 6

# accepting
# 0111 7
# 1111 15
# 0011 3
# 0000 0
# 1000 8
# 0100 4

# probably numbers different than 6