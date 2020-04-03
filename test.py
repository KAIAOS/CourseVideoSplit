
# from aip import AipSpeech
# client = AipSpeech('18916980', 'LDonbbm6l4VCnwRAdeKPhAUM', 'eVkEfdKyIp2BFyZL9aWvZmVxPav6qGF0')
# with open('output1.wav', 'rb') as fp:
#     sound = fp.read()
# d = client.asr(sound , 'wav', 16000)
# result = d['result'][0]
# print(result)


string1 = '国大字MOOC求n个元素中的最大值'
string2 = '国大字MOOC求n个无素中的最大值米用文字描述则如下步蝶所示给n个元系a~a输人数值把第一个元素a赋给用于保存最大值元素的变量x:把表示下标的变量赋初值2如果in则向下执行，否则输出最大值x后结束算法如果ax则将a赋给x将卜杯增工以指示下一个元转向第4步续执行'
a = 'ab'
b = 'abc'
print(a not in b)
print(string1 not in string2)
import difflib
def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()
s1='国大字NOOCtor:1Sm.+十1tor=IJSn+力一十十兴奶十l'
s2='国大字NOOCtor:1Sm:+十1or:Ism:+十1一十十m十l基本操作的语句频度为2n2其时旧复杂度为00.即时间复杂度为平方阶。'
print(string_similar(s1,s2[:len(s1)]))