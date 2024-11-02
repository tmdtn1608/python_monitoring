'''
- 리스트 [1, [2, 3], [4, [5, 6]]]를 [1, 2, 3, 4, 5, 6]으로 평탄화하는 함수를 작성하세요. -> recursive
- 리스트 [1, 2, 3, 4, 5]의 모든 부분 리스트를 생성하는 함수를 작성하세요.
- 두 리스트의 요소를 번갈아가며 새 리스트로 만드는 함수를 작성하세요. (예: [1,2,3], [a,b,c] → [1,a,2,b,3,c])
- 리스트에서 n번째로 큰 요소를 찾는 함수를 작성하세요.
- 리스트의 연속된 부분 리스트 중 합이 가장 큰 부분을 찾는 함수를 작성하세요. -> ????
'''

original : list = [1, [2, 3], [4, [5, 6]]]
def iterable_flatten(param : list) :
    flatten : list = []
    for i in param :
        if(type(i) == list) : 
            print('list : ', i)
            flatten.extend(iterable_flatten(i))
        elif(type(i) == int) : 
            print('int : ',i)
            flatten.append(i)
    return flatten
   
print(iterable_flatten(original))

def sub_list() : 
    original : list = [1, 2, 3, 4, 5]

def merge_list() :
    original_1 : list = [1,2,3]
    original_2 : list = ['a','b','c']
    result : list = []
    length : int = len(original_1) if len(original_1) > len(original_2) else len(original_2)
    for i in range(length) :
        try:
            result.append(original_1[i])
            result.append(original_2[i])
        except IndexError:
            pass
    return result
print(merge_list())

def high_element(idx : int) : 
    original : list = [1,3,4,6,7,9]
    if(idx -1 >= len(original)) : return
    sort_list = sorted(original, reverse=True)
    return sort_list[idx-1]

print(high_element(2))