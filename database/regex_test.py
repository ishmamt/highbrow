import re

txt = "python,html, Deep LEARNING, Machine learning"
reg = "^[A-Za-z0-9 ,]*$"
x = re.search(reg, txt)
print(x)
