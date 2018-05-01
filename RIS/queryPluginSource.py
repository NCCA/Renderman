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
    'k_RixSCString' : 'string'

}

def processPlugin(path,file) :
  #inputFile=open('%s/%s',%(path,file))
  with open('%s/%s' %(path,file), "r") as inputFile:
    for line in inputFile :
      line=line.strip() # remove whitespace
      if line.startswith('class') :
        className=line.split(' ')
        print '*******************************************************'
        print 'pattern :- ',className[1]
        print '*******************************************************'
      elif line.startswith('RixSCParamInfo(')   :
        start=line.find('(')
        line=line[start+1:-2]
        tokens=line.split(',')
        if len(tokens) > 1  and tokens[0][1:-1] !='' :
          parameter = tokens[0][1:-1]
          dataType=parameterTypes.get(tokens[1].strip())
          direction=''
          if len(tokens) == 3 :
            direction=':- output'
          print '%s %s %s' %(dataType,parameter,direction)

def main(directory) :
  files=os.listdir(directory)
  for file in files :
    if file.endswith('.cpp') :
      processPlugin(directory,file)



if __name__ == '__main__':
  description=''''Read Renderman .cpp plugin files and report on params, by default it will scan the directory passed for .cpp files and process them one at a time''' 
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('directory',help='directory to use',action='store',default='.')
  args = parser.parse_args()

  main(args.directory)
  

