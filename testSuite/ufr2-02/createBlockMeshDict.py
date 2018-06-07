import sys
import math
import openfoam

# Generate the cylinder blockMeshDict file for the von Karman LES case
#              16          17         18          19
#  y ^        0 - - - - - 1- - - - - 2 - - - - - 3
#    |        |           |          |           |  
#    --> x    |     0     |    1     |   2       |     ny1
#             |20         |21        |22         |23
#             4 - - - - - 5 - - - - -6 - - - - - 7
#             |           |          |           |  
#             |    3      |          |   4       |     ny2
#             |24         |25        |26         |27
#             8 - - - - - 9 - - - - 10 - - - - -11
#             |           |          |           |  
#             |    5      |   6      |   7       |     ny1
#             |28         |29        |30         |31
#             12 - - - - 13 - - - - 14 - - - - - 15
#                                                   
#                 nx1       nx2=ny2       nx3

ar = 20
d = 0.04
h1 = 0.392
l1 = 0.4
l2 = 1.36
width = 0.56
delta = 0.001
twoD = False

def usage(scriptname):
    print("usage:")
    print("\t {} -d <D> -h1 <H1> -l1 <L1> -l2 <L2> -w <W> -delta <delta> -ar <ar> -2d".format(scriptname))
    print("\t for every parameter not given the default values are:")
    print("\t override the default value by supplying the new value.")
    print("\t D = diameter of square cylinder. (0.04)")
    print("\t H1 = Height of the cylinder. (0.392)")
    print("\t L1 = Length from inlet to cylinder center. (0.4)")
    print("\t L2 = Length of computational domain. (1.36)")
    print("\t W = Width of the domain (0.56)")
    print("\t delta = cell size across the sides of the cylinder. (0.001)")
    print("\t ar = max/min cell size aspect ratio. (20.0)")
    print("\t -2d sets just one layer in z direction")

def readFlags(argv):
    global d, h1, l1, l2, width, delta, ar, twoD
    for i,a in enumerate(argv):
        if a == "-h":
            usage(argv[0])
            exit(2)
        elif a == "-d":
            d = float(argv[i+1])
        elif a == "-h1":
            h1 = float(argv[i+1])
        elif a == "-l1":
            l1 = float(argv[i+1])
        elif a == "-l2":
            l2 = float(argv[i+1])
        elif a == "-w":
            width = float(argv[i+1])
        elif a == "-delta":
            delta = float(argv[i+1])
        elif a == "-ar":
            ar = float(argv[i+1])
        elif a == "-2d":
            twoD = True
        elif "-" in a:
            print("{} unknown flag. Ignoring...".format(a))  


def calcN(L, R, d):
    n = 1 + math.log(R)/math.log((L-d)/(L-R*d));
    return int(n);

argv = sys.argv
readFlags(argv)

w = 0.5*width;
r = 0.5*d;
xe = l2-l1;
if twoD:
    h1 = 0.001

# aspect ratio for largest/smallest cells for the different blocks
g1 = ar;
g2 = ar;
g3 = ar;
nx1 = calcN(l1-r, g1, delta);
nx2 = int(d/delta) + 1;
nx3 = calcN(xe-r, g3, delta);
ny1 = calcN(w-r, g2, delta);
ny2 = nx2;
nz = 1
if not twoD:
    nz = int(0.3*h1/delta) + 1;
bmdict = openfoam.blockMeshDict()

for z in [ 0, h1 ]:
    for y in [ w, r, -r, -w ]:
        for x in [ -l1, -r, r, xe ]:
            bmdict.vertices.add("( {} {} {} )".format( x, y, z))

bmdict.blocks.add("hex ( 4 5 1 0 20 21 17 16 ) ( {} {} {} ) simpleGrading ( {} {} {} )".format(nx1, ny1, nz, 1.0/g1, g2, 1.0))
bmdict.blocks.add("hex ( 5 6 2 1 21 22 18 17 ) ( {} {} {} ) simpleGrading ( {} {} {} )".format(nx2, ny1, nz, 1.0, g2, 1.0))
bmdict.blocks.add("hex ( 6 7 3 2 22 23 19 18 ) ( {} {} {} ) simpleGrading ( {} {} {} )".format(nx3, ny1, nz, g3, g2, 1.0))

bmdict.blocks.add("hex ( 8 9 5 4 24 25 21 20 ) ( {} {} {} ) simpleGrading ( {} {} {} )".format(nx1, ny2, nz, 1.0/g1, 1.0, 1.0))
bmdict.blocks.add("hex ( 10 11 7 6 26 27 23 22 ) ( {} {} {} ) simpleGrading ( {} {} {} )".format(nx3, ny2, nz, g3, 1.0, 1.0))

bmdict.blocks.add("hex ( 12 13 9 8 28 29 25 24 ) ( {} {} {} ) simpleGrading ( {} {} {} )".format(nx1, ny1, nz, 1.0/g1, 1.0/g2, 1.0))
bmdict.blocks.add("hex ( 13 14 10 9 29 30 26 25 ) ( {} {} {} ) simpleGrading ( {} {} {} )".format(nx2, ny1, nz, 1.0, 1.0/g2, 1.0))
bmdict.blocks.add("hex ( 14 15 11 10 30 31 27 26 ) ( {} {} {} ) simpleGrading ( {} {} {} )".format(nx3, ny1, nz, g3, 1.0/g2, 1.0))

wall1PatchList = openfoam.list( "wall walls", endWithSemicolon=False )
wall1PatchList.add("(5 21 22 6)")
wall1PatchList.add("(6 22 26 10)")
wall1PatchList.add("(10 26 25 9)")
wall1PatchList.add("(9 25 21 5)")
bmdict.patches.add( wall1PatchList )

inletPatchList = openfoam.list( "patch inlet", endWithSemicolon=False)
inletPatchList.add("(4 20 16 0)")
inletPatchList.add("(8 24 20 4)")
inletPatchList.add("(12 28 24 8)")
bmdict.patches.add( inletPatchList )

outletPatchList = openfoam.list( "patch outlet", endWithSemicolon=False)
outletPatchList.add("(3 19 23 7)")
outletPatchList.add("(7 23 27 11)")
outletPatchList.add("(11 27 31 15)")
bmdict.patches.add( outletPatchList )

sideWallsList = openfoam.list( "patch sides", endWithSemicolon=False)
sideWallsList.add("(16 17 1 0)")
sideWallsList.add("(17 18 2 1)")
sideWallsList.add("(18 19 3 2)")
sideWallsList.add("(12 13 29 28)")
sideWallsList.add("(13 14 30 29)")
sideWallsList.add("(14 15 31 30)")
bmdict.patches.add( sideWallsList )

lowerUpperString = "empty lowerUpper"
if not twoD:
    lowerUpperString = "walls lowerUpper"
lowerWallsList = openfoam.list( lowerUpperString, endWithSemicolon=False )
lowerWallsList.add("(0 1 5 4)")
lowerWallsList.add("(1 2 6 5)")
lowerWallsList.add("(2 3 7 6)")
lowerWallsList.add("(4 5 9 8)")
lowerWallsList.add("(6 7 11 10)")
lowerWallsList.add("(8 9 13 12)")
lowerWallsList.add("(9 10 14 13)")
lowerWallsList.add("(10 11 15 14)")
lowerWallsList.add("(20 21 17 16)")
lowerWallsList.add("(21 22 18 17)")
lowerWallsList.add("(22 23 19 18)")
lowerWallsList.add("(24 25 21 20)")
lowerWallsList.add("(26 27 23 22)")
lowerWallsList.add("(28 29 25 24)")
lowerWallsList.add("(29 30 26 25)")
lowerWallsList.add("(30 31 27 26)")
bmdict.patches.add( lowerWallsList )

#bmdict.write(0)
filename = "system/blockMeshDict"
with open( filename, "w" ) as file:
    print("writing {}".format(filename))
    bmdict.writeToFile(file, 0)
