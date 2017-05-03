#!/usr/bin/python
## As in the last example, we will need the os, sys, and qb modules:
import os, sys,re
# for mac 
#sys.path.insert(0,'/Applications/pfx/qube/api/python/')
#import qb
 
import os, sys,getpass
# load Qube's python module
if 'QBDIR' in os.environ:
	sys.path.append('%s/api/python' % os.environ['QBDIR']) 
elif os.uname()[0] == 'Darwin':
	sys.path.append('/Applications/pfx/qube/api/python') 
else:
	sys.path.append('/usr/local/pfx/qube/api/python') 

import qb
# now Qt
from PyQt4.QtCore import (QFile, QFileInfo, QPoint, QRect, QSettings, QSize,Qt, QTextStream)
from PyQt4.QtGui import QIcon, QKeySequence, QClipboard
from PyQt4.QtGui import (QLabel,QLineEdit,QAction, QApplication,QFileDialog, QMainWindow,QMessageBox, QTextEdit,QGroupBox,QGridLayout,QPushButton,QFrame,QCheckBox,QSpinBox)
##############################################################################
# Tool tip text 
##############################################################################

cwdToolTipText='The current working directory is where on the <B>farm</B> the files are stored\nThis is usually /render/[username]/[dir] but you must enter this manually to match where you have placed the files to be rendered'

jobNameToolTipText='This is the name that will appear in qube default to prman'

ribFileToolTipText='This is the name of the file to submit to the farm. If you are submitting a range of files select the first file in the range and  set the range elements in the GUI, for example if you wish to render files <B>diffuse.001.rib - diffuse.100.rib</B> choose diffuse.001.rib and set the range to start=0 end=100 and Qube will do the substitution for you.'

startFrameToolTipText='This is the start frame for a range of rib files to be rendered, this will be automatically placed into the qube job as the first frame number based on the filename above and the padding so for example if we have diffuse.00001.rib as our first frame we need to set padding to 4 and start frame to 1'

endFrameToolTipText='This is the start frame for a range of rib files to be rendered, this will be automatically placed into the qube job as the first frame number based on the filename above and the padding so for example if we have diffuse.00101.rib as our first frame we need to set padding to 4 and start frame to 101'

paddingToolTipText='This is the frame padding for example 001 to 100 would be a padding of 3 0001 to 0123 would be 4\n<B> default to 3 </b>'

##############################################################################

def createLine() :
	line = QFrame() 
	line.setFrameShape(QFrame.HLine) 
	line.setFrameShadow(QFrame.Sunken) 
	return line

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.gridGroupBox = QGroupBox("Renderman Farm Submit")
		layout = QGridLayout()
		self.setWindowTitle('NCCA Renderfarm rib file submission system')
		# Job stuff
		jobnameLabel=QLabel('Job Name') 
		jobnameLabel.setToolTip(jobNameToolTipText)
		layout.addWidget(jobnameLabel, 1, 0)
		self.jobName=QLineEdit() 
		self.jobName.setToolTip(jobNameToolTipText)
		self.jobName.setText('prman')
		layout.addWidget(self.jobName, 1, 1) # the name of the job to submit
		# working dir (is going to be /render/USERNAME)
		# first get username
		self.username=getpass.getuser()
		cwdstart='/render/'+self.username+'/' 
		cwdlabel=QLabel('Working Directory')
		cwdlabel.setToolTip(cwdToolTipText)
		layout.addWidget(cwdlabel, 2, 0)
		self.cwd=QLineEdit()
		self.cwd.setToolTip(cwdToolTipText)
		self.cwd.setText(cwdstart)
		layout.addWidget(self.cwd, 2, 1)
		## filename
		ribFilelabel=QLabel('Rib File')
		ribFilelabel.setToolTip(ribFileToolTipText)
		layout.addWidget(ribFilelabel, 3, 0)
		self.ribFile=QLineEdit()
		self.ribFile.setToolTip(ribFileToolTipText)
		layout.addWidget(self.ribFile, 3, 1)

		# add separator
		layout.addWidget(createLine(),4,0) 
		layout.addWidget(createLine(),4,1) 
		# add checkbox for ranges
		self.renderRange=QCheckBox()
		self.renderRange.setText('Render Range')
		self.renderRange.setChecked(True)
		layout.addWidget(self.renderRange,5,0)
		## add start frame spinbox
		startFrameLabel=QLabel('StartFrame')
		startFrameLabel.setToolTip(startFrameToolTipText)
		layout.addWidget(startFrameLabel,6,0)
		self.startFrame=QSpinBox()
		self.startFrame.setRange(0, 1000000) 
		self.startFrame.setToolTip(startFrameToolTipText)
		layout.addWidget(self.startFrame,6,1)
		## add end frame spinbox
		endFrameLabel=QLabel('EndFrame')
		startFrameLabel.setToolTip(endFrameToolTipText)
		layout.addWidget(endFrameLabel,7,0)
		self.endFrame=QSpinBox()
		self.endFrame.setRange(0, 1000000) 
		self.endFrame.setToolTip(endFrameToolTipText)
		layout.addWidget(self.endFrame,7,1)

		## add padding frame spinbox
		paddingLabel=QLabel('Padding')
		paddingLabel.setToolTip(paddingToolTipText)
		layout.addWidget(paddingLabel,8,0)
		self.padding=QSpinBox()
		self.padding.setRange(0, 15) 
		self.padding.setValue(3)
		self.padding.setToolTip(paddingToolTipText)
		layout.addWidget(self.padding,8,1)

		# add separator
		layout.addWidget(createLine(),9,0)
		layout.addWidget(createLine(),9,1)
		# submit button
		self.submit=QPushButton("Submit")
		self.submit.setEnabled(False)
		layout.addWidget(self.submit,10,1)
		# add stuff to layouts etc
		self.gridGroupBox.setLayout(layout)
		self.setCentralWidget(self.gridGroupBox)
		# connections and logic
		self.renderRange.stateChanged.connect(self.startFrame.setEnabled)
		self.renderRange.stateChanged.connect(self.endFrame.setEnabled)
		self.renderRange.stateChanged.connect(self.padding.setEnabled)
		self.ribFile.editingFinished.connect(self.enableButton)
		self.submit.clicked.connect(self.submitJob)
	def enableButton(self) :
		if(self.ribFile.text() != '') :
			self.submit.setEnabled(True)
		else :
			self.submit.setEnabled(False)

	def submitJob(self) :
		print 'submitting job'
		# The first few parameters are the same as the previous examples
		job = {}
		job['name'] = self.jobName.text()
		job['prototype'] = 'cmdrange'
		job['cpus'] = 1
		job['priority'] = 9999
		job['cwd']= str(self.cwd.text())

    # Below creates an empty package dictionary
		package = {}
   	# Below instructs the Qube! GUI which submission UI to use for resubmission
		package['simpleCmdType'] = 'cmdrange'
		if self.renderRange.isChecked() == True :
  		# doing a range
			# todo add sanity check for range
			package['range'] = '%d-%d' %(self.startFrame.value(),self.endFrame.value())
			renderString='$RMANTREE/bin/render '
			renderString=renderString+self.cwd.text()+'/'
			# todo add sanity check and instructions on file formats
			file=self.ribFile.text()
			# some regex magic!
			newstring=str(file)
			fileName=re.sub(r'(\d+)','QB_FRAME_NUMBER',newstring,1)
			renderString=renderString+fileName
			print renderString
			package['cmdline'] = str(renderString)
			package['padding']=self.padding.value()
		else :
  		# single file
			print "single"


		# Below sets the job's package to the package dictionary we just created
		job['package'] = package
		job['env']={'RMANTREE' : '/opt/software/pixar/RenderManProServer-20.10/'}
		# Using the given range, we will create an agenda list using qb.genframes
		agenda = qb.genframes(package['range'])

		# Now that we have a properly formatted agenda, assign it to the job
		job['agenda'] = agenda 
			

		listOfJobsToSubmit = []
		listOfJobsToSubmit.append(job)

		# As before, we create a list of 1 job, then submit the list.  Again, we
		# could submit just the single job w/o the list, but submitting a list is
		# good form.
		print 'Submit before'
		listOfSubmittedJobs = qb.submit(listOfJobsToSubmit)
		print 'after submit'
		for job in listOfSubmittedJobs:
			print job['id']




		print job,package
 
# Below runs the "main" function
if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.resize(400,800)
	mainWin.show()
	sys.exit(app.exec_())    
