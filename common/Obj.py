import prman


class Obj:

    # ctor to assign values
    def __init__(self, file):
        self.verts = []
        self.norm = []
        self.text = []
        self.face = []

        print("opening : " + file)
        # open the file
        ip = open(file, "r")
        # grab the data as lines
        data = ip.readlines()
        # for each line check for one of our tokens
        for line in data:
            # we assume that our Tokens are always the first element of the line (which IIRC the rispec specifies)
            # so we split each line and look at the first element
            tokens = line.split()
            # make sure we have a token to check against
            if len(tokens) > 0:
                if tokens[0] == "v":
                    # print 'found vert'
                    # create a tuple of the vertex point values
                    vert = [float(tokens[1]), float(tokens[2]), float(tokens[3])]
                    # then add it to our list
                    self.verts += [vert]
                elif tokens[0] == "vn":
                    # print 'found normal'
                    # create a tuple of the normal values
                    normal = [float(tokens[1]), float(tokens[2]), float(tokens[3])]
                    # then add it to our list
                    self.norm += [normal]
                elif tokens[0] == "vt":
                    # print 'found texture'
                    # create a tuple of the texture values
                    # *****************************************************************
                    tx = [float(tokens[1]), float(tokens[2])]
                    #
                    # *****************************************************************
                    # then add it to our list
                    self.text += [tx]
                # now we have a face value
                elif tokens[0] == "f":
                    # add the face to the list and we will process it later (see below)
                    self.face += [line]

        # close the file
        ip.close()

    def getExtents(self):
        xmin = self.verts[min((n, i) for i, n in enumerate(self.verts))[1]][0]
        xmax = self.verts[max((n, i) for i, n in enumerate(self.verts))[1]][0]
        ymin = self.verts[min((n, i) for i, n in enumerate(self.verts))[1]][1]
        ymax = self.verts[max((n, i) for i, n in enumerate(self.verts))[1]][1]
        zmin = self.verts[min((n, i) for i, n in enumerate(self.verts))[1]][2]
        zmax = self.verts[max((n, i) for i, n in enumerate(self.verts))[1]][2]

        print(xmin, xmax, ymin, ymax, zmin, zmax)

        return xmin, xmax, ymin, ymax, zmin, zmax

    def Polygon(self, ri):
        for f in self.face:
            # create some empty data structures to be filled as we go
            vertices = []
            normals = []
            points = []
            tx = []
            fd = f.split()
            # the face is in the structure shown below Vert / TX / Norm we are gaurenteed to have a
            # Vert but the others may not be there
            # 1/1/1 3/2/2 4/3/3 2/4/4
            for perface in fd[1:]:
                index = perface.split("/")
                if len(index) == 3:
                    # get the point array index
                    pind = int(index[0]) - 1
                    points.append(self.verts[pind][0])
                    points.append(self.verts[pind][1])
                    points.append(self.verts[pind][2])
                    # check for textures and add if there
                    if index[1] != "":
                        tind = int(index[1]) - 1
                        tx.append(self.text[tind][0])
                        tx.append(self.text[tind][1])
                    # check for normals and check they are there
                    if index[2] != "":
                        nind = int(index[2]) - 1
                        normals.append(self.norm[nind][0])
                        normals.append(self.norm[nind][1])
                        normals.append(self.norm[nind][2])
                elif len(index) == 1:
                    # get the point array index
                    pind = int(index[0]) - 1
                    points.append(self.verts[pind][0])
                    points.append(self.verts[pind][1])
                    points.append(self.verts[pind][2])
                elif len(index) == 2:
                    # get the point array index
                    pind = int(index[0]) - 1
                    points.append(self.verts[pind][0])
                    points.append(self.verts[pind][1])
                    points.append(self.verts[pind][2])
                    # check for textures and add if there
                    if index[1] != "":
                        tind = int(index[1]) - 1
                        tx.append(self.text[tind][0])
                        tx.append(self.text[tind][1])

            # create a dictionary to store the polygon data, we always have a point so we can add
            # this directly
            PolyData = {ri.P: points}
            # now see if we have any texture co-ordinates and add them to the dictionary if we do
            if len(tx) != 0:
                PolyData[ri.ST] = tx
            # check for normals and add them to the dictionary as well
            if len(normals) != 0:
                PolyData[ri.N] = normals
            # finally we generate the Polygon from the data
            ri.Polygon(PolyData)  # {ri.P:points,ri.N:normals,ri.ST:tx})

    def PointsPolygon(self, ri):
        npolys = []
        vertices = []
        normals = []
        for f in self.face:
            # create some empty data structures to be filled as we go
            fd = f.split()
            # the face is in the structure shown below Vert / TX / Norm we are gaurenteed to have a
            # Vert but the others may not be there
            # 1/1/1 3/2/2 4/3/3 2/4/4
            npolys.append(len(fd) - 1)
            for perface in fd[1:]:
                index = perface.split("/")
                # get the point array index
                vertices.append(int(index[0]) - 1)
        v = []
        # the verts are in a list of lists at the moment so we extract them
        # into a single list for prman
        for i in range(0, len(self.verts)):
            for x in range(0, len(self.verts[i])):
                v.append(self.verts[i][x])

        ri.PointsPolygons(npolys, vertices, {ri.P: v})

    def SubDivisionMesh(self, ri):
        npolys = []
        vertices = []
        normals = []
        for f in self.face:
            # create some empty data structures to be filled as we go
            fd = f.split()
            # the face is in the structure shown below Vert / TX / Norm we are gaurenteed to have a
            # Vert but the others may not be there
            # 1/1/1 3/2/2 4/3/3 2/4/4
            npolys.append(len(fd) - 1)
            for perface in fd[1:]:
                index = perface.split("/")
                # get the point array index
                vertices.append(int(index[0]) - 1)
        v = []
        # the verts are in a list of lists at the moment so we extract them
        # into a single list for prman
        for i in range(0, len(self.verts)):
            for x in range(0, len(self.verts[i])):
                v.append(self.verts[i][x])

        ri.SubdivisionMesh("loop", npolys, vertices, [ri.CREASE], [2, 1], [3, 0], [20], {ri.P: v})
