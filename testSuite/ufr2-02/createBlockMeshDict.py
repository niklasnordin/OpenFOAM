import sys
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
w = 0.56
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
            w = float(argv[i+1])
        elif a == "-delta":
            delta = float(argv[i+1])
        elif "-" in a:
            print("{} unknown flag. Ignoring...".format(a))  

argv = sys.argv
readFlags(argv)

bmdict = openfoam.blockMeshDict()
bmdict.vertices.add("1")
bmdict.vertices.add("2")
bmdict.vertices.add("3")

bmdict.write(0)
filename = "system/blockMeshDict"
with open( filename, "w" ) as file:
    print("writing {}".format(filename))
    bmdict.writeToFile(file, 0)
