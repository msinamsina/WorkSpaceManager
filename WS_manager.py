# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 13:31:48 2020

@author: Mohammad Sina Allahkaram (--MSA--)
"""

"""
TODO:
    checking the data types when new space is creating. 
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
    
    #########################
    #   Private functions   #
    #########################
    def __save(self):
        with open(self.__WS_fileName,'w') as f:
            json.dump(self.__global_WS,f)
            
    def __update(self):
        tmp={self.__name:self.__local_WS}
        self.__global_WS.update(tmp)
        self.__save()
            
    def __show(self , d, level=0):
        for k in d:
            print(level*'  |  '+"  |")
            if isinstance(d[k],dict):
                print(level*'  |  '+"  |___{} -->  ({})".format(k, type(d[k])) )
                self.__show(d[k],level+1)
            else:
                print(level*'  |  '+"  |___{} --> {} ({})".format(k,d[k], type(d[k])) )
        if level == 0:
            print("\n")
        
    def __load(self):
        with open(self.__WS_fileName) as f:
            self.__global_WS.update(json.load(f))
    
    def __read_ws_file(self):     
        if os.path.exists(self.__WS_fileName):    
            self.__load()
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
    
    #########################
    #   Public functions    #
    #########################
    def set_ws(self,Name):
        self.__name = Name
        self.__read_ws_file()
    
    def delete_ws(self,Name):
        answer=input("Are you sure you want to delete {} workspace? [Y,n]\n".format(Name))
        if answer in self.yesForms:
            del self.__global_WS[Name]
            self.__save()
   
    def show_all(self):
        for name in self.__global_WS:
            print(name)
            self.__show(self.__global_WS[name])
            
    def show(self):
        print(self.__name)
        self.__show(self.__local_WS)
              
    # def set_filds(self,kwargs ,update=True ):
    #     self.__local_WS.update(kwargs)
    #     if update:
    #         self.__update()
    
    # def fill_ws_like(self,Name):
    #     data=self.__global_WS[Name]
    #     print(data)
    #     self.set_filds(data)
                
    def update_ws(self,name=None,updatelist=None):
        if name is None:
            name = self.__name
        if updatelist is None:
            updatelist = self.__global_WS['sample']
        for i in updatelist:
            a=input("({}) -- please enter {} path sample--> '{}' :\n".format(self.__name,i,self.__global_WS[name][i]))
            try:
                self.__local_WS[i]=eval(a)
            except :
                self.__local_WS[i]=a
        self.__update()
        
    def creat_sample(self,template={}):
        a=''
        tmp=template.copy()
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
        self.update_ws('sample')
        
    def update_sample(self):
        tmp1 = self.__global_WS['sample'].copy()
        self.creat_sample(template=self.__global_WS['sample'])
        tmp2 = self.__global_WS['sample']
        
        for name in self.__global_WS:
            if name !="sample":
                self.update_ws("sample",updatelist=list(set(tmp2.keys())-set(tmp1.keys())))
    
if __name__ =="__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('fileName', help="Path to Work space file", type=str)
    parser.add_argument("name", help="work space name.", type=str)
    parser.add_argument("-S", "--showAll", help="shows All details of spaces in workspace.",action="store_true")
    parser.add_argument("-s", "--show", help="Shows space details.",action="store_true")
    parser.add_argument("-u", "--update", help="updates the filds of space.",action="store_true")
    parser.add_argument("-U", "--updateSample", help="updates the filds of sample space.",action="store_true")
    parser.add_argument("-d", "--delete", help="deletes the space.",action="store_true")
    
    args = parser.parse_args()
    
    ws_ins= WS_Manager(args.fileName,args.name)
    
    if args.delete:
        ws_ins.delete_ws(args.name)
    if args.showAll:
        ws_ins.show_all()
    if args.show:
        ws_ins.show()
    if args.update:
        ws_ins.update_ws()
    if args.updateSample:
        ws_ins.update_sample()
