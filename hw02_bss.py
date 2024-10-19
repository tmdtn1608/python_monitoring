# 파일명 number_영어이니셜.py
# 숫자 1개를 입력받아서 숫자가 크면 "숫자가 커요"
# 숫자가 작으면 "숫자가 작아요"
# 숫자가 같으면 "숫자가 같아요"
# 비교할 숫자는 30, 변수명 num1

num1 : int = 30

num2 = input("숫자를 입력하세요")
if(not num2.isdigit()) :
    print("숫자가 아니에요")
else :
    if(int(num2) > num1) :
        print("숫자가 커요")
    elif(int(num2) == num1) :
        print("숫자가 같아요")
    else : 
        print("숫자가 작아요")