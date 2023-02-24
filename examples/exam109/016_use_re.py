"""
限定符
限定符用来指定正则表达式的一个给定组件必须要出现多少次才能满足匹配。有 * 或 + 或 ? 或 {n} 或 {n,} 或 {n,m} 共6种。

正则表达式的限定符有：

字符	描述
*	匹配前面的子表达式零次或多次。例如，zo* 能匹配 "z" 以及 "zoo"。* 等价于{0,}。
+	匹配前面的子表达式一次或多次。例如，'zo+' 能匹配 "zo" 以及 "zoo"，但不能匹配 "z"。+ 等价于 {1,}。
?	匹配前面的子表达式零次或一次。例如，"do(es)?" 可以匹配 "do" 、 "does" 中的 "does" 、 "doxy" 中的 "do" 。? 等价于 {0,1}。
{n}	n 是一个非负整数。匹配确定的 n 次。例如，'o{2}' 不能匹配 "Bob" 中的 'o'，但是能匹配 "food" 中的两个 o。
{n,}	n 是一个非负整数。至少匹配n 次。例如，'o{2,}' 不能匹配 "Bob" 中的 'o'，但能匹配 "foooood" 中的所有 o。'o{1,}' 等价于 'o+'。'o{0,}' 则等价于 'o*'。
{n,m}	m 和 n 均为非负整数，其中n <= m。最少匹配 n 次且最多匹配 m 次。例如，"o{1,3}" 将匹配 "fooooood" 中的前三个 o。'o{0,1}' 等价于 'o?'。请注意在逗号和两个数之间不能有空格。
"""
"""
特殊字符
所谓特殊字符，就是一些有特殊含义的字符，如上面说的 runoo*b 中的 *，简单的说就是表示任何字符串的意思。如果要查找字符串中的 * 符号，则需要对 * 进行转义，即在其前加一个 \，runo\*ob 匹配字符串 runo*ob。

许多元字符要求在试图匹配它们时特别对待。若要匹配这些特殊字符，必须首先使字符"转义"，即，将反斜杠字符\ 放在它们前面。下表列出了正则表达式中的特殊字符：

特别字符	描述
$	匹配输入字符串的结尾位置。如果设置了 RegExp 对象的 Multiline 属性，则 $ 也匹配 '\n' 或 '\r'。要匹配 $ 字符本身，请使用 \$。
( )	标记一个子表达式的开始和结束位置。子表达式可以获取供以后使用。要匹配这些字符，请使用 \( 和 \)。小括号（）代表着匹配对应的字符串，你在小括号里面写了几个字符串，就匹配对应的这几个字符串，比如你写了（abc），它就会匹配abc这个字符串。
*	匹配前面的子表达式零次或多次。要匹配 * 字符，请使用 \*。
+	匹配前面的子表达式一次或多次。要匹配 + 字符，请使用 \+。
.	匹配除换行符 \n 之外的任何单字符。要匹配 . ，请使用 \. 。
[	标记一个中括号表达式的开始。要匹配 [，请使用 \[。代表的是一个匹配范围,比如[a-c],它就会匹配a,b,c这三个字符串,再如[0-3],它就会匹配0到3这四个字符串.
?	匹配前面的子表达式零次或一次，或指明一个非贪婪限定符。要匹配 ? 字符，请使用 \?。
\	将下一个字符标记为或特殊字符、或原义字符、或向后引用、或八进制转义符。例如， 'n' 匹配字符 'n'。'\n' 匹配换行符。序列 '\\' 匹配 "\"，而 '\(' 则匹配 "("。
^	匹配输入字符串的开始位置，除非在方括号表达式中使用，当该符号在方括号表达式中使用时，表示不接受该方括号表达式中的字符集合。要匹配 ^ 字符本身，请使用 \^。
{	标记限定符表达式的开始。要匹配 {，请使用 \{。大括号{}代表的是一个匹配长度范围,比如\s{4},就是代表匹配4个空格。
|	指明两项之间的一个选择。要匹配 |，请使用 \|。
\s  代表正则表达式中的一个空白字符（可能是空格、制表符、其他空白）
\w 匹配字母或数字或下划线或汉字 等价于 '[^A-Za-z0-9_]'。\w能不能匹配汉字要视你的操作系统和你的应用环境而定
\b 匹配单词的开始或结束
\d 匹配数字
顺便说下，正则表达式一般写法开头是^，结尾是$.
"""

import re

div_str = '<div class="name">中国</div>'
# .代表可有可无，*代表任意字符，满足类名可有变化，()提取，？
res = re.findall(r'<div class=".*">(.*?)</div>', div_str)
print(res)

abc_str = "bcdtuo"
print(re.findall('(abc|bcd|cde)', abc_str))  # 输出bcd


def test(law, text):
    data = re.match(law, text)
    if data:
        print("发现匹配：", data.group(), end=",  ")
        print("在%s发现匹配%s" % (text, law))
    else:
        print("在%s没有发现匹配%s" % (text, law))


test(".", "Mgaojgo")  # 第一个字符,输出M
test("t.o", "toooo")  # 输出too
test("t.o", "twoww")  # 输出two

# 如果hello的首字符小写，那么正则表达式需要小写的h
test("h", "hello Python")  # 输出h
# 如果hello的首字符大写，那么正则表达式需要大写的H
test("H", "Hello Python")  # H
# 大小写h都可以的情况
test("[hH]", "hello Python")  # h
test("[hH]", "Hello Python")  # H

# 匹配0到9第一种写法
test("[0123456789]Hello Python", "7Hello Python")  # 7 Hello Python
# 匹配0到9第二种写法
test("[0-9]Hello Python", "1Hello Python")  # 1Hello Python
test("[0-9][0-9]Hello Python", "10Hello Python")  # 10Hello Python
# 下面这个正则不能够匹配到数字4
test("[0-3 5-9]Hello Python", "4Hello Python")
# 能够匹配到空格
test("[0-3 5-9]Hello Python", " Hello Python")
# 不能匹配到空格
test("[0-35-9]Hello Python", " Hello Python")

# \d匹配数字，即0-9
test("嫦娥1号", "嫦娥1号发射成功")  # 嫦娥1号
test("嫦娥\\d号", "嫦娥1号发射成功")  # 嫦娥1号
test("嫦娥\\d号", "嫦娥2号发射成功")  # 嫦娥2号
test("嫦娥\\d号", "嫦娥3号发射成功")  # 嫦娥3号

# *匹配前一个字符出现0次或无限次
test("[A-Z][a-z]*", "M")  # M
test("[A-Z][a-z]*", "Mnnnnnnnn")  # Mnnnnnnnn
test("[A-Z][a-z]*", "A1111nnnn")  # M

# 需求：匹配出，变量名是否有效 name1 _name __name__
names = ["name1", "_name", "2_name", "__name__"]
for x in names:
    # +号，匹配前面的表达式一次或多次，也就是签名以多个字母或下划线开头
    test("[a-zA-Z_]+[\\w]", x)

# 需求：匹配出，0到99之间的数字, 问号代表前一个字符出现1次或0次
test("[1-9]?[0-9]", "7")  # 7,  在7发现匹配[1-9]?[0-9]
test("[1-9]?[0-9]", "79")  # 79,  在79发现匹配[1-9]?[0-9]
test("[1-9]?[0-9]", "789")  # 78,  在789发现匹配[1-9]?[0-9]
test("[1-9]?[0-9]", "6789")  # 67,  在6789发现匹配[1-9]?[0-9]

# 需求：匹配出，8到20位的密码，可以是大小写英文字母、数字、下划线
test("[a-zA-Z0-9_]{6}", "12a3g45678")  # 12a3g4  匹配出6位密码
test("[a-zA-Z0-9_]{8,20}", "1ad12f23s34455ff661ad12f23s34455ff66")  # 1ad12f23s34455ff661a
test("[a-zA-Z0-9_]{8,20}", "1ad12f23")  # 1ad12f23
test("[a-zA-Z0-9_]{8,20}", "1ad12f2")  # 未发现匹配

# 匹配出163的邮箱地址，且@符号之前有4到20位，例如hello@163.com
emails = ["f661ad1@163.com", "24899988389489@qq.com", "f661@163.com", "f661ad1fefddwe12345555@126.com"]
print("\n\n第一种")
for x in emails:
    test("[a-zA-Z0-9_]{4,20}[@][163]{3}[.com]{4}", x)

print("\n\n第二种")
for x in emails:
    test("\\w{4,20}@163.com", x)  # \w 匹配单词字符，即a-, A-Z, 0-9, _

email_list = ["xiaoWang@163.com", "xiaoWang@163.comheihei", ".com.xiaowang@qq.com"]
print("\n\n非163结尾的会出现错误")
for x in email_list:
    test("\\w{4,20}@163.com", x)  # 没有$字符串结尾匹配时会匹配到xiaoWang@163.comheihei
print("\n\n修正后")
for x in email_list:
    test("\\w{4,20}@163.com$", x)  # $字符串结尾匹配

# 需求：匹配出0-100之间的数字
test("[1-9]?\\d", "8")  # 8
# 不正确
test("[1-9]?\\d", "08")  # 0
test("[1-9]?\\d", "100")  # 10
# 修正
test("[1-9]?\\d$|100", "08")  # 不匹配
test("[1-9]?\\d$|100", "100")  # 100
test("[1-9]?\\d$|100", "99")  # 99
test("[1-9]?\\d\\d$|1000", "900")  # 900

"""
$   : 匹配结尾位置
（）: 标记一个子表达式的开始和结束
\w  : 匹配字母，数字，下划线， 等价于[A-Za-z0-9_]
"""
# 需求：匹配出163、126、qq邮箱
email_list = ["xiaohong@163.com", "xiaoWang@126.com", "xiaoWang@163.comheihei", ".com.xiaowang@qq.com"]
for x in email_list:
    test(r"\w{4,20}@(163|126|qq).com$", x)

# 不是以4、7结尾的手机号码(11位)
phone = ["cc18217389576", "18217389677", "18217389684", "111111118738921680", "18289680177", "10086"]
for x in phone:
    test(r"1\d{9}[0-35-68-9]", x)
# test(r"1\d{9}[47]",x)  # 以4、7结尾

# 需求：匹配出<html>hh</html>
test("<[a-zA-Z]*>\\w*</[a-zA-Z]*>", "<html>hh</html>")
# test("<[a-zA-Z]*>\\w*</[a-zA-Z]*>","")
# 遇到非正常HTML时出错
test("<[a-zA-Z]*>\\w*</[a-zA-Z]*>", "<htmlssssdf>hh</htmlssssdf>")
# 正确的理解思路：如果在第一对<>中是什么，按理说在后面的那对<>中就应该是什么
# 通过引用分组中匹配到的数据即可
# \1是引用（）分组的数据 第几组数字就是几
test("<([a-zA-Z]*)>\\w*</\\1><([a-zA-Z]*)>\\w*</\\2>", "<html>hh</html><htmlssssdf>hh</htmlssssdf>")
test("<(\\w*)><(\\w*)></\\2></\\1>", "<a><i></i></a>")
# 分组重命名 注意：(?P<name>)和(?P=name)中的字母p大写
test("<(?P<name>\\w*)><(?P<na>\\w*)></(?P=na)></(?P=name)>", "<a><i></i></a>")

# 匹配一行文字中的所有开头的字母内容
# \b 是正则表达式规定的一个特殊代码（好吧，某些人叫它元字符，metacharacter），
# 代表着单词的开头或结尾，也就是单词的分界处。虽然通常英文的单词是由空格，
# 标点符号或者换行来分隔的，但是 \b 并不匹配这些单词分隔字符中的任何一个，它只匹配一个位置。
s = "i love you not because of who you are, but because of who i am when i am with you"
print(re.findall(r'\b\w', s))

ss = "It's a nice day nicenice today."
print(re.findall(r"\bnice\b", ss))  # nice
print(re.findall(r"\w*nice\w*", ss))  # nice, nicenice
print(re.findall(r"a\b.\bnice", ss))

# 匹配数字开头的
sss = "5y i love you not because 12sd 34er 56df e4 54434"
print(re.findall(r"\b\d", sss))
test(r"\b\d", sss)

if __name__ == "__main__":
    # div_str = '<div class="name">China</div>'
    # div_res = re.findall(r'<div class=".*">(.*?)</div>', div_str)
    # print(div_res)
    pass
    print("start match ...")
    print(re.findall(r".*(text|and|te).*", "(texet_a32453nd)"))
    print(re.match(r"(text|and)", "(text|and)"))
    abc_str = "bcdtuo"
    print(re.findall('tuo|bcd|cde', abc_str))  # 输出bcd
