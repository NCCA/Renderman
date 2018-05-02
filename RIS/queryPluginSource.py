#!/usr/bin/python

import sys,os.path,subprocess
import argparse
import string

parameterTypes={
    'k_RixSCInvalidType' : 'Invalid Type',
    'k_RixSCAnyType' : 'any',
    'k_RixSCInteger' : 'int',
    'k_RixSCFloat' : 'float',
    'k_RixSCFloat2' : 'float2',
    'k_RixSCFloat3' : 'float3',
    'k_RixSCColor' : 'color',
    'k_RixSCPoint' : 'point',
    'k_RixSCVector' : 'vector',
    'k_RixSCNormal' : 'normal',
    'k_RixSCMatrix' : 'matrix',
    'k_RixSCString' : 'string',
    'k_RixSCStructBegin' : 'struct{',
    'k_RixSCStructEnd' : '};'

}

class plugin :
  def __init__(self,name='') :
    self.name=name
    self.param=[]
  def addParam(self,type,name,direction='input') :
    self.param.append([name,type,direction])
  def __str__(self) :
    strings=[]
    for t in self.param :
     strings.append('%s %s %s' %(t[2],t[1],t[0]))    
    return self.name+'\n' + '\n' .join(strings)
  

def processPlugin(path,file) :
  plug=plugin() # empty plug to append data to 
  with open('%s/%s' %(path,file), "r") as inputFile:
    for line in inputFile :
      line=line.strip() # remove whitespace
      if line.startswith('class') :
        className=line.split(' ')
        plug.name=className[1]
        # print '*******************************************************'
        # print 'pattern :- ',className[1]
        # print '*******************************************************'
      elif line.startswith('RixSCParamInfo(')   :
        start=line.find('(')
        # remove string from above and and elements
        line=line[start+1:-2]
        # tokenize and strip white space (using list comprehension)
        tokens=[x.strip() for x in line.split(',')]
        # we have two choices either an input which has two tokens
        if len(tokens) == 2 :
          parameter = tokens[0][1:-1] # remove quotes
          dataType=parameterTypes.get(tokens[1])
          plug.addParam(dataType,parameter)  
        elif len(tokens) == 3 and tokens[2] =='k_RixSCOutput' : # we have an output
          parameter = tokens[0][1:-1] # remove quotes
          dataType=parameterTypes.get(tokens[1])
          plug.addParam(dataType,parameter,'output')  
        elif len(tokens) == 3 and tokens[2].strip() =='k_RixSCStructBegin' : # we have an output
          parameter = tokens[0][1:-1]
          dataType=parameterTypes.get(tokens[1])
          plug.addParam(dataType,parameter,'struct')
        elif len(tokens) == 3 and tokens[2].strip() =='k_RixSCStructEnd' : # we have an output
          parameter = tokens[0][1:-1] # remove quotes
          dataType=parameterTypes.get(tokens[1])
          plug.addParam(dataType,parameter,'end struct')
            
          
        # if len(tokens) > 1  and tokens[0][1:-1] !='' :
        #   parameter = tokens[0][1:-1]
        #   dataType=parameterTypes.get(tokens[1].strip())
        #   direction=''
        #   if len(tokens) == 3 :
        #     direction=':- output'
        #   print '%s %s %s' %(dataType,parameter,direction)
    print plug
def main(directory) :
  if os.path.isdir(directory) :
    files=os.listdir(directory)
    for file in files :
      if file.endswith('.cpp') :
        processPlugin(directory,file)
  elif os.path.isfile(directory) :
        processPlugin('',directory)
    


if __name__ == '__main__':
  description=''''Read Renderman .cpp plugin files and report on params, by default it will scan the directory passed for .cpp files and process them one at a time and print out the parameters''' 
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('directory',help='directory to use can be explicit single file',action='store',default='.')


  args = parser.parse_args()

  main(args.directory)
  

