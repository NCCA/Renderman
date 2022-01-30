#!/usr/bin/python
import prman
import inspect

ri = prman.Ri()  # create an instance of the RenderMan interface

file = open("members.txt", "w")

file.write("Data from dir(prman.RI()\n")
file.write("----------------------------------------------------------------------------------------\n")
data = dir(ri)
for line in data:
    file.write("ri.%s() \n" % line)
    helpText = inspect.getdoc(eval("ri.%s" % line))
    file.write("Help Text if any :- \n%s\n" % helpText)
    file.write("----------------------------------------------------------------------------------------\n")

file.close()
