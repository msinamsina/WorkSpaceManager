# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 13:31:48 2020

@author: Mohammad Sina Allahkaram (--MSA--)
"""
import os
import json

class WS_Manager:
    
    def __init__(self,fileName,WS_name):
        
        self.yesForms=['','Y','y','yes','Yes','YES']
        
        self.__WS_fileName=fileName
        self.__local_WS={}
        self.__global_WS={}
        self.set_ws(WS_name)
        
    def set_ws(self,Name):
        self.__name = Name
        self.__read_ws_file()
        
    def __read_ws_file(self):
        
        if os.path.exists(self.__WS_fileName):    
            self.load()
            if self.__name in self.__global_WS:
                self.__local_WS=self.__global_WS[self.__name]
            else:
                answer=input("work space Name dosen't exist \ndo you want to creat new work space from sample? [Y,n]\n")
                if answer in self.yesForms:
                    self.creat_new_ws()
                else:
                    pass    
        else:
            answer=input("work space file'{}' dosen't exist \ndo you want to creat new file? [Y,n]\n".format(self.__WS_fileName))
            if answer in self.yesForms:
                print('please enter key and valeue of sample of Work space.')
                self.creat_sample()
                self.creat_new_ws()
                    
    def set_filds(self,kwargs ,update=True ):
        self.__local_WS.update(kwargs)
        if update:
            self.update()
    
    def fill_ws_like(self,Name):
        data=self.__global_WS[Name]
        print(data)
        self.set_filds(data)
        
    def update(self):
        tmp={self.__name:self.__local_WS}
        self.__global_WS.update(tmp)
        with open(self.__WS_fileName,'w') as f:
            json.dump(self.__global_WS,f)
        
    def load(self):
        with open(self.__WS_fileName) as f:
            self.__global_WS.update(json.load(f))
            
    def creat_sample(self):
        a=''
        tmp={}
        while True:
            a=input('please enter one key(or enter "!q" to finish!):\n')
            print(a)
            if a =='!q':
                break
            elif a == '':
                continue
            
            d=''
            while d =='':
                d=input('please enter dic coresponding to "{}" or enter "!b" to back! :\n'.format(a))
            
            if d == '!b':
                continue
            elif  d== '!q':
                break
            try:
                tmp[a]=eval(d)
            except:
                tmp[a]=d
                
        self.__global_WS['sample']=tmp 
    
    def creat_new_ws(self):
        for i in self.__global_WS['sample']:
            a=input("({}) -- please enter {} path sample--> '{}' :\n".format(self.__name,i,self.__global_WS['sample'][i]))
            try:
                self.__local_WS[i]=eval(a)
            except :
                self.__local_WS[i]=a
        self.update()
    
    def delete_ws(self,Name):
        del self.__global_WS[Name]

    def __call__(self):
        return self.__name

    def __getitem__(self,key):
        return self.__local_WS[key]
   
    
if __name__ =="__main__":
    
    ws_ins= WS_Manager("test8.ws",'SinaLinux')