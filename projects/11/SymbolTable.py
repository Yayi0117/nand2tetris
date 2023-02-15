class SymbolTable:
    #table = {name1:[type,kind,index],name2:[type,kind,index]}
    #kinds = {tpye1:number, typ2:number}


    def __init__(self) :
        self.table = {}
        self.kinds = {'local':0,'argument':0,'field':0,'static':0}
    
    def reset(self):
        self.table = {}
        self.kinds = {'local':0,'argument':0,'field':0,'static':0}
    
    def define(self,name,var_type,kind):
        index = self.kinds[kind]
        self.kinds[kind] += 1
        self.table[name] = [var_type,kind,index]

    def varCount(self,kind):
        return self.kinds[kind]

    def kindOf(self,name):
        return self.table[name][1]

    def typeof(self,name):
        return self.table[name][0]
    
    def indexOf(self,name):
        return self.table[name][2]


