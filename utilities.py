import math
import random
from datetime import datetime
from enums import commentList,imgUrl

def createList():

        list1=[]
        for i in range(10):
            r=random.randint(8,60)
            if r not in list1: list1.append(r)
        
        list2=[]
        for i in range(10):
            r=random.randint(10,30)
            if r not in list2: list2.append(r)

        return list1,list2

def pickCommentFromList():
    r=random.randint(0,2)
    print("list index is {}".format(r))
    comment=commentList[r]
    return comment
        



# datetime object containing current date and time
def CreateDbFileStr():
    now = datetime.now()
    
    print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%m_%d_%H%M")
    print("date and time =", dt_string)
    dt_string="pythonsqlite_"+dt_string+".db"
    return dt_string