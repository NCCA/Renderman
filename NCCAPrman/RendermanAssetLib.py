import os,sys
RMSTREE=os.environ.get('RMSTREE')
if RMSTREE == None :
  print 'Need to set RMSTREE to use the module'
  exit()
RMSTREE=RMSTREE+'/scripts'
sys.path.append(RMSTREE)

import rfm.rmanAssets as ra
import rfm.rmanAssetsLib as ral
from rfm.rmanAssets import RmanAsset

class Asset :
  def __init__(self,filepath) :
    Asset = RmanAsset()
    filename=filepath+'/asset.json'
    Asset.load(filename, localizeFilePaths=True)
    assetType = Asset.type()
    if assetType == "nodeGraph":
      self.rib=str(Asset.getRIB())
    elif assetType == "envMap" :
      self.rib='Light "PxrDomeLight" "domeLight" "string lightColorMap"   ["%s"]' %Asset.envMapName() 

  def getRIB(self) :
      return self.rib


class RendermanAssetLib :
  def __init__(self) :
    self.loadedAssets={}
    self.optionPaths=[]

  def loadAsset(self,name,filepath) :
    if  os.path.exists(filepath) :
      self.optionPaths.append(filepath)
      self.loadedAssets[name]=Asset(filepath)

  def setOptions(self,ri) :
    path='.:@'
    for p in self.optionPaths :
      path=path+':%s' %p
    ri.Option('searchpath', {'string texture':path})
    ri.Option('searchpath', {'string shader':path})

  def useAsset(self,ri,name) :
    asset=self.loadedAssets.get(name)
    if asset != None :
      ri.ArchiveRecord(ri.COMMENT,'loaded from Asset file')
      ri.ArchiveRecord(ri.VERBATIM,asset.getRIB() )
      ri.ArchiveRecord(ri.COMMENT,'#############################')
      

"""
def useAsset(ri,filepath) :
  Asset = RmanAsset()
  ri.Option('searchpath', {'string texture':filepath})
  ri.Option('searchpath', {'string shader':filepath})
  filename=filepath+'/asset.json'
  Asset.load(filename, localizeFilePaths=True)
  assetType = Asset.type()
  if assetType == "nodeGraph":
    rib=Asset.getRIB()
    ri.ArchiveRecord(ri.COMMENT,'loaded from Asset file')
    ri.ArchiveRecord(ri.VERBATIM,str(rib) )
    ri.ArchiveRecord(ri.COMMENT,'#############################')
"""