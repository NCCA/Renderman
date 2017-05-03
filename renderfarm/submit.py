#!/usr/bin/python
# As in the last example, we will need the os, sys, and qb modules:
import os, sys
# for mac 
sys.path.insert(0,'/Applications/pfx/qube/api/python/')
import qb
 
# Below is the main function to run in this script
def main():
    os.environ['RMANTREE']='/opt/software/pixar/RenderManProServer-20.10'
    # The first few parameters are the same as the previous examples
    job = {}
    job['name'] = 'jon prman'
    job['prototype'] = 'cmdrange'
 
    job['cpus'] = 1
    job['priority'] = 9999
    job['cwd']='/render/jmacey'
     
     
    # Below creates an empty package dictionary
    package = {}
     
    # Below instructs the Qube! GUI which submission UI to use for resubmission
    package['simpleCmdType'] = 'cmdrange'
     
    # Below defines the camera used for the render
     
     
     
     
    # Below defines the command to be run.  This is necessary for our API submission,
    # but will be re-generate based on user defined parameters upon resubmission.
    package['cmdline'] = '$RMANTREE/bin/render /render/jmacey/fireQB_FRAME_NUMBER.vdb.rib '
    package['padding']=3
     
    # Below defines the maya executable location
     
    # below defines the range of the job to be rendered
    package['range'] = '1-80'
    # Below defines the scenefile location
     
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
    listOfSubmittedJobs = qb.submit(listOfJobsToSubmit)
    for job in listOfSubmittedJobs:
        print job['id']
 
# Below runs the "main" function
if __name__ == "__main__":
    main()
    sys.exit(0)