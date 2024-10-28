# 과제3. (ex03-9.py)
# 숫자1과 숫자 2를 받아서 덧셈하는 계산기 프로그램
# 함수형태로 만들기. 
# 0을 입력하면 종료. while문

"""
input값 유효성 확인 및 계산진행 확인.
str/int 여부 및 0 판별
"""
def is_num(param: str) -> bool :
    if(not param.isdigit()) : return False
    elif(int(param) == 0) : return False
    else : return True

"""
반복 input
"""
def input_num(cnt: int) -> bool | int :
    num = input(f"숫자 {cnt}를 입력하세요")
    if(not is_num(num)) : return False
    else : return num

"""
While & break로 진행관리
"""
while (True) :
    num1 = input_num(1)
    if(num1 == False) : break

    num2 = input_num(2)
    if(num2 == False) : break

    print(f"{int(num1) + int(num2)}")