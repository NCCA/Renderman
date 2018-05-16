# Interactive Re-Rendering with Renderman

This demo demonstrates a workflow for re-rendering with renderman. 

The file rerender.py will read and render the file scene.py which in turn generates a file called bake.rib.

This is then executed in the interactive renderer within IT and waits for the file edits.py to be changed and will issue edits (make sure there are no errors in the python code else this will crash)

