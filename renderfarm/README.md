# NCCA Renderfarm submission GUI

This tool can be used to submit rib files to the renderfarm for rendering. There are two version One for Qt4 and one for Qt5. In the NCCA labs it can be found in /public/devel/bin/submitPRMANtoFarm.py

## Pipeline

The first step is to copy all of the rib files, shaders, textures etc to the renderfarm directory.

In the following example I have a directory called **fire** which contains my project files. First we must create the directory on the remote drive in sftp else it will not work.

```
sftp tete.bournemouth.ac.uk
sftp> mkdir fire
sftp> put -r fire
```

This will now upload all the files to be rendered to tete the renderfarm server. On the server you have a directory called */render/[username]* so for example in the case above the renderfarm will have a directory called */render/jmacey/fire* for my account.

To open the GUI either download the python file an execute or use the installed lab version below
```
 /public/devel/bin/submitPRMANtoFarm.py 
```
<img src="images/gui.png" alt="alt text" width="300">

The image above shows the completed form, the user needs to fill in the working directory changed to /render/jmacey/fire (it will default to /render/[username]) which reflects the directory on the farm.

The rib file name shown is  *fire001.vdb.rib* the qube render system will replace the 001 value with the correct frame numbers based on the start / end frame dialogs.

It is important that the name is formatted for all the frame in the same way as a regular expression is used to replace this string. 

The frame padding is also very important, as this specifies the leading zeros to be replaced when the worker looks up the file name to render. In the above case padding is set to 3 if the filename was fire0001.vdb.rib the padding would be set to 4.

Once the elements are filled in the submit button can be used to submit to the farm.

