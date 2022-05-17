#!/usr/bin/python
import argparse
import collections
import os.path
import sys
import xml.etree.ElementTree


def processArgFile(file, output):
    # convention is args file name name of plugin so extract
    # PxrDiffuse.args (and will have path is dir passed )
    pluginName = file[file.rfind("/") + 1 : -5]
    e = xml.etree.ElementTree.parse(file).getroot()
    shaderType = e.find("shaderType/tag").attrib.get("value")
    shaderType = "".join(
        shaderType[0].upper() + shaderType[1:]
    )  # First letter is capital bxdf to Bxdf
    # May also have Filter types such as LightFilter (lightFilter)
    shaderType = shaderType.replace("filter", "Filter")
    strings = ""

    if output == "rib":
        strings += '%s "%s" "id" \n' % (shaderType, pluginName)
        for t in e.findall("param"):
            dataType = t.get("type")
            name = t.get("name")
            defaultValue = t.get("default")
            if defaultValue == None:
                defaultValue = "'No Value'"  # sometimes there is no default
            elif dataType == "string":
                defaultValue = "'" + defaultValue + "'"  # strings need to be quoted
            elif dataType == "float":
                defaultValue = defaultValue.replace(
                    "f", ""
                )  # seems some floats us 0.0f
            strings += '\t"%s %s"  [%s] \n' % (dataType, name, defaultValue)
        page = e.findall("page")

        for p in page:
            for t in p.findall("param"):
                dataType = t.get("type")
                name = t.get("name")
                defaultValue = t.get("default")
                if defaultValue == None:
                    defaultValue = "'No Value'"  # sometimes there is no default
                elif dataType == "string":
                    defaultValue = "'" + defaultValue + "'"  # strings need to be quoted
                elif dataType == "float":
                    defaultValue = defaultValue.replace(
                        "f", ""
                    )  # seems some floats us 0.0f
                strings += '\t"%s %s"  [%s] \n' % (dataType, name, defaultValue)

    elif output == "python":
        strings += "ri.%s('%s','id',\n" % (shaderType, pluginName)
        strings += "{\n"
        for t in e.findall("param"):
            dataType = t.get("type")
            name = t.get("name")
            defaultValue = t.get("default")
            if defaultValue == None:
                defaultValue = "'No Value'"  # sometimes there is no default
            elif dataType == "string":
                defaultValue = "'" + defaultValue + "'"  # strings need to be quoted
            else:
                defaultValue = defaultValue.replace(" ", ",")  # add , between values
                if dataType == "float":
                    defaultValue = defaultValue.replace(
                        "f", ""
                    )  # seems some floats us 0.0f
            strings += "\t'%s %s' : [%s], \n" % (dataType, name, defaultValue)
        page = e.findall("page")

        for p in page:
            for t in p.findall("param"):
                dataType = t.get("type")
                name = t.get("name")
                defaultValue = t.get("default")
                if defaultValue == None:
                    defaultValue = "'No Value'"  # sometimes there is no default
                elif dataType == "string":
                    defaultValue = "'" + defaultValue + "'"  # strings need to be quoted
                else:
                    defaultValue = defaultValue.replace(
                        " ", ","
                    )  # add , between values
                    if dataType == "float":
                        defaultValue = defaultValue.replace(
                            "f", ""
                        )  # seems some floats us 0.0f
                strings += "\t'%s %s' : [%s], \n" % (dataType, name, defaultValue)

        strings += "})\n"
    else:

        strings += "%s %s\n" % (shaderType, pluginName)
        for t in e.findall("param"):
            dataType = t.get("type")
            name = t.get("name")
            defaultValue = t.get("default")
            strings += "%s %s %s \n" % (dataType, name, defaultValue)
        page = e.findall("page")
        for p in page:
            for t in p.findall("param"):
                dataType = t.get("type")
                name = t.get("name")
                defaultValue = t.get("default")
                strings += "%s %s %s \n" % (dataType, name, defaultValue)
    return strings


def main(directory, output, outputFile):

    if outputFile != "":
        with open(outputFile, "w") as outFile:
            if os.path.isdir(directory):
                files = os.listdir(directory)
                for file in files:
                    if file.endswith(".args"):
                        file = "%s/%s" % (directory, file)
                        data = processArgFile(file, output)
                        if outFile is not None:
                            outFile.write(data)
                            outFile.write("#" * 40 + "\n")
            elif os.path.isfile(directory):
                data = processArgFile(directory, output)
                outFile.write(data)
    else:
        if os.path.isdir(directory):
            files = os.listdir(directory)
            for file in files:
                if file.endswith(".args"):
                    file = "%s/%s" % (directory, file)
                    print(processArgFile(file, output))
                    print("#" * 40)
        elif os.path.isfile(directory):
            print(processArgFile(directory, output))


if __name__ == "__main__":
    description = """'Read Renderman .cpp plugin files and report on params, by default it will scan the directory passed for .cpp files and process them one at a time and print out the parameters"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "directory",
        help="directory to use can be explicit single file",
        action="store",
        default=".",
    )
    parser.add_argument(
        "--rib", "-r", action="count", help="render to rib not framebuffer"
    )
    parser.add_argument(
        "--py", "-p", action="count", help="render to rib not framebuffer"
    )
    parser.add_argument(
        "--file",
        "-f",
        nargs="?",
        const="",
        default="",
        type=str,
        help="dump output to file not stdout",
    )

    output = ""
    args = parser.parse_args()
    if args.rib:
        output = "rib"
    if args.py:
        output = "python"
    outputFile = ""
    if args.file != "":
        outputFile = args.file

    main(args.directory, output, outputFile)
