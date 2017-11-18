
class ListtoDict():
    '''
        在
    '''
    def __init__(self,listx,str='num'):
        self.listx=listx
        self.str=str
    @classmethod
    def up(self,dict1, dict2):
        dict1.update(dict2)
        return dict1


    @property
    def f(self):
        s = []
        listy = [{self.str: x + 1} for x in range(len(self.listx))]
        for i in range(len(self.listx)):
            dict1=self.listx[i]
            dict2=listy[i]
            dict=ListtoDict.up(dict1,dict2)
            dict=[dict]
            s+=dict
        return s

if __name__=="__main__":
    list=[{'1':2},{'w':4}]

    #要生成 [{'1':2,'str':1}{'1':2,"str":2}]
    a=ListtoDict(list,'str')
    print(a.f)
