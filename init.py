import json
class Item(object):
    _dict = {"vat":{}}#TODO: DB this data for easy searching...
    def keys(self):
        a=[]
        b=[]
        for part in self.dict.keys():
            a.append(part)
        for part in self.number.keys():
            b.append(part) 
        a.append({"number":b})#add a directory to the other format of data "numbers only for auto processing"
        return a
    def __init__(self,*arg,**kvar):#d={},n={}
        self.active=False
        #build with defults
        if "d" not in kvar.keys():
            kvar["d"]={}
        else:
            kvar["d"]=kvar["d"]
        if "n" not in kvar.keys():
            kvar["n"]={}
        else:
            kvar["n"]=kvar["n"]
        #end
        self.dict=kvar["d"]
        self.number=kvar["n"]
        self.objRef=arg[0]
        
    def __getitem__(self, index):#only complex for robust results
        if type(index)==type([]):#pull a dictnary refrance
            if len(index)>1:
                if index[0] in self.keys():#if the item was linked to a root item
                    worker=getattr(self, index[0])#pull the root item
                    if worker!=None:
                        for e in worker.items():
                            if e[0] == index[1]:
                                #print "from %s comes %s holding %s"%(index[0],worker,dir(worker))
                                return e[1]#now that we have the bace item we have acess to its values fail sillently
            else:
                raise Exception("format bug, index recived an array with not enough items to process. Recived:",index) 
        else:
            if index in self.number.keys():#less likely first
                return self.number[index]
            elif index in self.dict.keys():
                return self.dict[index]
            else:
                print (self.dict.keys(),self.number.keys())
                try:
                    raise ValueError(self.dict["objRef"] ,"invalid index %s"%(index))
                except:
                    return None
    def __new__(cls,*arg,**karg):
        if len(arg)==0:
            try:
                raise Exception('*arg len==0','no Item family refrence given')
            except Exception as inst:
                x, y = inst.args     # unpack args
                print "instance is now unstable \n%s\n\t%s"%(x,y)
        else:
            #print "\n\nbuilding {{%s}}"%(str(arg[0]))
            if arg[0] not in Item._dict["vat"].keys():
                
                Item._dict["vat"][arg[0]]=[]#this is a list of items added together under a given vat ID
            else:
                pass#TODO: maby use this to look at the list and compare others to it #TODO: condence listings
        #minamul code for getitem
        if 'key' in Item._dict:
            return Item._dict['key']
        else:
            return super(Item, cls).__new__(cls)
    def __add__(self,object):#TODO: object mearge with OXAL (infnate recurchion loop evolving. strip loop to return path)
        dic={}
        num={}
        for k,v in object.dict.iteritems():#TODO: condence
            if k not in dic.keys():
                dic[k]=[]
            if type(v)==type([]):
                for i in v:
                    dic[k].append(i)
            else:
                dic[k].append(v)
        for k,v in self.dict.iteritems():
            if k not in dic.keys():
                dic[k]=[]
            if type(v)==type([]):
                for i in v:
                    dic[k].append(i)
            else:
                dic[k].append(v)
        for k,v in object.number.iteritems():
            if k not in num.keys():
                num[k]=[]
            if type(v)==type([]):
                for i in v:
                    num[k].append(i)
            else:
                num[k].append(v)
        for k,v in self.number.iteritems():
            if k not in num.keys():
                num[k]=[]
            if type(v)==type([]):
                for i in v:
                    num[k].append(i)
            else:
                num[k].append(v)
        Item._dict["vat"][self.objRef].append(object)#for spliting parts
        Item._dict["vat"][self.objRef].append(self)
        new=Item(object.objRef,d=dic,n=num)
        
        for k,v in dic.iteritems():#__init__ bug workaround
            new.__setattr__(k,v)
        for k,v in num.iteritems():
            new.__setattr__(k,v)
        return new
    def sort(self,value):
        vals=[]
        for e in value:
            try:
                vals.append(float(e))
            except ValueError:
                pass#TODO:LOOK OUT!!! unhandled error
        m=min(vals)
        a=sum(vals)/len(vals)
        ma=max(vals)
        return (m,a,ma)#return Object?
    def __setattr__(self, name, value):
        super(Item, self).__setattr__(name, value)#support for python iner workings this causes problems 
        e=getattr(self,"number",None)
        e2=getattr(self,"dict",None)
        if e !=None and e2!=None:# and type(e2) != int:
            val=value#val is the baceline type
            if type(value)==type([]):#if array take first element
                if len(value)>0:#legal operation?
                    val=value[0]#TODO: find most regular data type insted of first add filter swiches 
                else:
                    pass #rase error on empty array?
            staticNum=None  
            #TODO: handle URLs and run compaireason auto download images
            if type(val)==type({}):#TODO:should this be a ebay api data type insted of conveting it to a dic or should i fork ebay sdk
                #print val.keys()
                if "CategoryID" in val.keys():
                    self.dict[name]=val["CategoryName"]+"___"+val["CategoryID"]
                    val=value=None
                    return
            if type(val)==type("") and val.isdigit():#if array type is int#evil hit count not recived as int...TODO: commit a fix to git hub
                a=[]
                if type(value)==type([]):#TODO:This is done a lot, how can I make this generic?
                    for e in value:
                        a.append(float(e))
                else:
                    a.append(float(value))
                val=a[0]
                value=a
            if type(val) == int or type(val) == float :
                staticNum=value#auto sort numeric values
            if type(val)==type(datetime.datetime.utcfromtimestamp(0)):#TODO: handle Clock instances int he Clock class
                times=[]
                if type(value)==type([]):
                    for t in value:
                        if type(t)==type(datetime.datetime.utcfromtimestamp(0)):#TODO: find the source of the bug that requires this line as a patch
                            times.append(int(Clock(t)))
                else:
                    times=[int(Clock(value))]
                value=staticNum=times#when int(is called clock returns delta epoch in sec)
            if staticNum!=None:
                self.number[name]=staticNum
                if type(staticNum)==type([]):
                    self.number[name+"__sorted"]=self.sort(staticNum)#because this fires on even small items there is no history of items summed so we need to keep the values in raw form so that they can be processed as a blob... messy
            self.dict[name]=value#list without root access of the object (abstract from classes iner workings)
    def __dir__(self):
        return self.dict.keys()
    def __str__(self):
        return str(self.dict)
    def __repr__(self):
        pice={}
        for k,v in self.dict.iteritems():
            pice[k]=str(v)
        return json.dumps(pice)
