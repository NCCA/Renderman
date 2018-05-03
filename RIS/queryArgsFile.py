#!/usr/bin/python
import sys,os.path
import argparse
import collections
import xml.etree.ElementTree

def processArgFile(file,output) :
  # convention is args file name name of plugin so extract 
  # PxrDiffuse.args (and will have path is dir passed )
  pluginName=file[file.rfind('/')+1:-5]
  e = xml.etree.ElementTree.parse(file).getroot()
  shaderType=e.find('shaderType/tag').attrib.get('value')
  shaderType=''.join(shaderType[0].upper()+shaderType[1:]) # First letter is capital bxdf to Bxdf
  # May also have Filter types such as LightFilter (lightFilter)
  shaderType=shaderType.replace('filter','Filter')
    
  if output == 'rib' :
    print "rib"
  elif output=='python' :
    strings=''
    strings+=( "ri.%s('%s','id',\n" %(shaderType,pluginName))
    strings+='{\n'
    for t in e.findall('param'):
      dataType=t.get('type')
      name=t.get('name')
      defaultValue=t.get('default')
      if defaultValue == None :
        defaultValue="'No Value'" # sometimes there is no default
      elif dataType=='string' :
        defaultValue="'"+defaultValue+"'" # strings need to be quoted
      else :
        defaultValue=defaultValue.replace(' ',',') # add , between values
        if dataType == 'float' : 
          defaultValue=defaultValue.replace('f','') # seems some floats us 0.0f
      strings+="\t'%s %s' : [%s], \n" %(dataType,name,defaultValue)
      #print type(t[1])
    strings+='})\n'
    print strings

  else :
    print "text"
  

def main(directory,output) :
  if os.path.isdir(directory) :
    files=os.listdir(directory)
    for file in files :
      if file.endswith('.args') :
        file='%s/%s' %(directory,file)
        processArgFile(file,output)
        print '#' * 40
  elif os.path.isfile(directory) :
        processArgFile(directory,output)
    


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
  

