import random
answer = random.sample(range(1, 10), 4)
print(answer)
a = b = n = 0
while a!=4:
    a = b = n = 0
    user = list(input('輸入四個數字：'))
    #A的條件
    #B的條件
    #每個字都要判斷
    output = ','.join(user).replace(',','')
    print(f'{output}: {a}A{b}B')
print('答對了！')
