
list1=[1, 2, 3]
list2=[4,5,6]
for i in list1:
    print i

listl=[list1, list2]

list0=[num for listt in listl for num in listt]
print list0
