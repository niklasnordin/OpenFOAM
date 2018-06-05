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

d = 0.04
h1 = 0.392
l1 = 0.4
l2 = 1.36
width = 0.56
delta = 0.001

def usage(scriptname):
    print("usage:")
    print("\t {} -d <D> -h1 <H1> -l1 <L1> -l2 <L2> -w <W> -delta <delta>".format(scriptname))
    print("\t for every parameter not given the default values are:")
    print("\t override the default value by supplying the new value.")
    print("\t D = diameter of square cylinder. (0.04)")
    print("\t H1 = Height of the cylinder. (0.392)")
    print("\t L1 = Length from inlet to cylinder center. (0.4)")
    print("\t L2 = Length of computational domain. (1.36)")
    print("\t W = Width of the domain (0.56)")
    print("\t delta = cell size across the sides of the cylinder. (0.001)")

def readFlags(argv):
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
        elif "-" in a:
            print("{} unknown flag. Ignoring...".format(a))  


def calcN(L, R, d):
    n = 1 + math.log(R)/math.log((L-d)/(L-R*d));
    return int(n);

argv = sys.argv
readFlags(argv)

w = 0.5*width;
r = 0.5*d;
r0 = 0.5*d;
xe = l2-l1;

# aspect ratio for largest/smallest cells for the different blocks
g1 = 20.0;
g2 = 20.0;
g3 = 20.0;
nx1 = calcN(l1-r, g1, delta);
nx2 = int(d/delta) + 1;
nx3 = calcN(xe-r, g3, delta);
ny1 = calcN(w-r, g2, delta);
ny2 = nx2;
nz = int(0.3*h1/delta) + 1;
bmdict = openfoam.blockMeshDict()
#    print "    ( -$L1  $w 0 )\n";
#    print "    ( -$r   $w 0 )\n";
##    print "    (  $r   $w 0 )\n";
#   print "    (  $xe  $w 0 )\n";

bmdict.vertices.add("( {} {} {} )".format(-l1, w, 0))

bmdict.write(0)
filename = "system/blockMeshDict"
with open( filename, "w" ) as file:
    print("writing {}".format(filename))
    bmdict.writeToFile(file, 0)
