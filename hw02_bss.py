# 파일명 number_영어이니셜.py
# 1부터 100까지 중에 숫자를 입력하세요
# 입력받아서 숫자가 크면 "숫자가 커요"
# 숫자가 작으면 "숫자가 작아요"
# 숫자가 같으면 "숫자가 같아요"
# 비교할 숫자는 30, 변수명 num1

num1 : int = 30

num2 = input("숫자를 입력하세요")
if(not num2.isdigit()) :
    print("1부터 100까지 중에 숫자를 입력하세요")
else :
    num2_cast : int = int(num2)
    if(num2_cast < 1 or num2_cast > 100) : 
        print("1부터 100까지 중에 숫자를 입력하세요")
    else :
        if(num2_cast > num1) :
            print("숫자가 커요")
        elif(num2_cast == num1) :
            print("숫자가 같아요")
        else : 
            print("숫자가 작아요")
