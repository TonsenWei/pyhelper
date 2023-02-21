# 24、字典根据键从小到大排序dict={"name":"zs","age":18,"city":"深圳","tel":"1362626627"}
def test():
    dic = {"name": "zs", "age": 18, "city": "深圳", "tel": "1362626627"}
    li = sorted(dic.items(), key=lambda i: i[0])
    print('根据key排序：', li)  # 根据key排序： [('age', 18), ('city', '深圳'), ('name', 'zs'), ('tel', '1362626627')]
    print('根据key排序：' + str(li))  # 根据key排序：[('age', 18), ('city', '深圳'), ('name', 'zs'), ('tel', '1362626627')]

    new_dic = dict(li)
    print(new_dic)  # {'age': 18, 'city': '深圳', 'name': 'zs', 'tel': '1362626627'}

    dic_value = {"name": 20, "age": 18, "city": 30, "tel": 15}
    li_value = sorted(dic_value.items(), key=lambda i: i[1])
    print('根据value排序：' + str(li_value))  # 根据value排序：[('tel', 15), ('age', 18), ('name', 20), ('city', 30)]


def printDict():
    case_selected = {}
    case_selected.setdefault(9, [1]).append(2)
    case_selected.setdefault(2, []).append(2)
    case_selected.setdefault(5, []).append(2)
    case_selected.setdefault(1, []).append(2)
    print(case_selected)
    res = sorted(case_selected.items(), key=lambda x: x[0])
    print(res)
    # print(dict(res))
    for key in res:
        print(f"{key} = {res[key]}")
    # words = ["apple", "banana", "airline", "bank", "panda"]
    # by_letters = {}
    # for word in words:
    #     by_letters.setdefault(word[0], []).append(word)
    # print(by_letters)


if __name__ == "__main__":
    # printDict()
    print(tuple((1, 5))[0])
