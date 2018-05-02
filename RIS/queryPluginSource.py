#!/usr/bin/python
''' Parse a renderman plugin source file and print useful info! '''
import sys,os.path
import argparse
import collections

''' 
these are the types the param can be taken from RixSCType in $RMANTREE/include/RixShading.h we use the dictionary to convert to prman types
'''
typeparam = collections.namedtuple('typeparam', 'datatype, default')

parameterTypes={
    'k_RixSCInvalidType' : typeparam('Invalid Type','0'),
    'k_RixSCAnyType' : typeparam('any','0'),
    'k_RixSCInteger' : typeparam('int','0'),
    'k_RixSCFloat' : typeparam('float','0.0'),
    'k_RixSCFloat2' : typeparam('float2','0.0,0.0'),
    'k_RixSCFloat3' : typeparam('float3','0.0,0.0,0.0'),
    'k_RixSCColor' : typeparam('color','1.0,1.0,1.0'),
    'k_RixSCPoint' : typeparam('point','0.0,0.0,0.0'),
    'k_RixSCVector' : typeparam('vector','0.0,1.0,0.0'),
    'k_RixSCNormal' : typeparam('normal','0.0,1.0,0.0'),
    'k_RixSCMatrix' : typeparam('matrix','0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0'),
    'k_RixSCString' : typeparam('string','default'),
    'k_RixSCStructBegin' : typeparam('struct{',''),
    'k_RixSCStructEnd' : typeparam('};','')
}


''' plugin major types (i.e. what the class inherits from), we use this when writing out
in either rib or python to write the actual base string '''

plugTypes={
  'RixPattern' : 'Pattern',
  'RixBxdf' : 'Bxdf',
  'RixDisplacement' : 'Displacement',
  'RixLight' : 'Light',
  'RixLightFilter' : 'LightFilter',
  'RixVolume' : 'Volume',
  'RixLighting' : 'Lighting',
  'RixProjection' : 'Projection',
  'RixDeepTexture' : 'DeepTexture' 
}


'''
simple structure to hold the plugin data, as we parse in sequence we use a list to hold the params, this is useful as it may contain structs which are declared in order with a begin / end
'''
class plugin :
  def __init__(self,name='') :
    self.name=name
    self.param=[]
    self.plugType=''

  def addParam(self,type,name,direction='input') :
    self.param.append([name,type,direction])
  def __str__(self) :
    strings=[]
    for t in self.param :
     strings.append('%s %s %s' %(t[2],t[1],t[0]))    
    return self.name+'\n' + '\n' .join(strings)
  def toPython(self) :
    strings=''
    strings+=( "ri.%s('%s','id',\n" %(plugTypes[self.plugType],self.name))
    strings+='{\n'
    for t in self.param :
      if t[1] is not None and t[2] =='input' :
        strings+="\t'uniform %s %s' : [%s], \n" %(t[1].datatype,t[0],t[1].default)
      #print type(t[1])
    strings+='})\n'
    return strings
  def toRib(self) :
    strings=''
    strings+=( '%s "%s" "id" \n' %(plugTypes[self.plugType],self.name))
    for t in self.param :
      if t[1] is not None and t[2] =='input' :
        strings+='\t"uniform %s %s"  [%s] \n' %(t[1].datatype,t[0],t[1].default.replace(',',' '))
      #print type(t[1])
    return strings

def processPlugin(file,output) :
  plug=plugin() # empty plug to append data to 
  with open(file, "r") as inputFile:
    for line in inputFile :
      line=line.strip() # remove whitespace
      if line.startswith('class') :
        className=line.split(' ')
        plug.name=className[1]
        try :
          plug.plugType=className[4]
        except IndexError :
          plug.plugType='unknown'
      # this is the data we need to process it
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
                      
    if output=='python' :
      print plug.toPython()
    elif output=='rib' :
      print plug.toRib()
    else :
      print plug
def main(directory,output) :
  if os.path.isdir(directory) :
    files=os.listdir(directory)
    for file in files :
      if file.endswith('.cpp') :
        file='%s/%s' %(directory,file)
        print '*' * 40
        processPlugin(file,output)
        print '*' * 40
  elif os.path.isfile(directory) :
        processPlugin(directory,output)
    


if __name__ == '__main__':
  description=''''Read Renderman .cpp plugin files and report on params, by default it will scan the directory passed for .cpp files and process them one at a time and print out the parameters''' 
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('directory',help='directory to use can be explicit single file',action='store',default='.')
  parser.add_argument('--rib', '-r' , action='count',help='render to rib not framebuffer')
  parser.add_argument('--py', '-p' , action='count',help='render to rib not framebuffer')

  output=''
  args = parser.parse_args()
  if args.rib  :
    output='rib'
  if args.py :
    output='python'
  main(args.directory,output)
  

