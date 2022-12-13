#!/usr/bin/env python3

import struct
import sys
import time
import os

from names import *

inodes = {}
destfile = ""
file_for_copy = sys.argv[2]

def readblock(fd, n):       #parameters: descriptor and block number
    fd.seek( 1024*n)         #assuming 1024 is the block size
    return fd.read(1024)

def readinode(fd, n, m):
    fd.seek( (1024 * n) + (256 * m) )
    return fd.read(1024)

def readbitmap(fd, index):
    fd.seek(1024 * index)
    bitmap = fd.read(32)

    inodes = struct.unpack('<Q', bitmap[:8])
    inode_count = len(bin(inodes[0]))-2
    print(inode_count)

def overwrite_file(new_file, index, firstinode):
    with open(sys.argv[4], 'r+b') as testing:
        testing.seek( (1024 * firstinode) + (256 * (index - 1) ) )
        test = struct.pack('<2H5I2H', new_file[1][0], new_file[1][1], new_file[1][2], new_file[1][3], new_file[1][4], new_file[1][5], new_file[1][6], new_file[1][7], new_file[1][8])
        testing.write(test)
        print("test:", test)

        print_new_image()

#JUST FOR TESTING
def print_new_image():
    with open(sys.argv[4], 'rb') as fd:
        sb = readblock(fd, 1)

        print(sb)


def readlld(fd, n):

    global inodes

    #Get root inode info
    nextinode = 0
    fd.seek( (1024 * n) + (nextinode) )
    pointer = fd.read(1024)

    #Loop through lld, putting names and indices of all inodes into "inodes" dictionary in format {name : index}

    #Check to make sure next inode isnt end of lld
    while( (struct.unpack('<IHBB', pointer[:8]))[0] != 0):
        data = struct.unpack('<IHBB', pointer[:8])
        # for i,x in enumerate(data):   testing purposes
        #     print(f'{x:10d} {lldnames[i]:s}')

        #Get Namelength and index
        index, namelen = data[0], data[2]


        #iterate through lld and get all characters of inode name, add them to 'name' string
        name = ""
        for i in range(namelen):
            fd.seek( (1024 * n) + nextinode + (8) + i)
            pointer = fd.read(1024)
            name += str(struct.unpack('<c', pointer[:1])[0])[2:-1]

        #once name is completed, add it and the index to inodes dict
        inodes.update({name : index})
        # print("inodes:", inodes) testing purposes

        #go to next lld item
        nextinode += data[1]
        if(nextinode > 256):
            break
        fd.seek( (1024 * n) + (nextinode))
        pointer = fd.read(1024)

def findinode(fd, firstinode, newfile):
    #iterate through dict of inodes
    for i in inodes.items():

            #Unpack the data for the inode
            inode = readinode(fd, firstinode, i[1]-1)
            inode_data = struct.unpack('<2H5I2H3II', inode[:44])
            mode = str(bin(inode_data[0]))

            #Assign the values for printing
            name = i[0]
            file_data = ""
            if(name == destfile):
                if(mode[2] == '2'):
                    pass
                    #copy file into directory
                else:
                    #Copy file over old file
                    overwrite_file(newfile, i[1], firstinode)
            else:
                #Create new file with contents of the file to be copied
                pass

def readFile(file):

#Read in file, get its inode data (mode, user id, size, etc.)
#Add its actual contents into a string 'file_data'

    file_data = ""
    file_stats = os.stat(file)

    mode = int(file_stats[0])
    uid = int(file_stats[4])
    gid = int(file_stats[5])
    size = int(file_stats[6])

    print("size:", type(size))
    links = 1
    atime, mtime, dtime, = int(time.time()), int(time.time()), int(time.time())

    inode_data = []

    inode_data.append(mode)
    inode_data.append(uid)
    inode_data.append(size)
    inode_data.append(atime)
    inode_data.append(0)
    inode_data.append(mtime)
    inode_data.append(dtime)
    inode_data.append(gid)
    inode_data.append(links)
    print(inode_data)

    for i in inode_data:
        print(type(i))



    with open(file, "rb") as fd:

        fd.seek(0)
        i_block = fd.read(size)

        for i in i_block:
            file_data+= chr(i)

    return file_data, inode_data


def main():
    global file_for_copy, destfile
    file_for_copy = sys.argv[2]
    destfile = sys.argv[3]

    with open(sys.argv[1], "r+b") as fd:
        # print("superblock:")
        sb = readblock(fd, 1)
        sb_data = struct.unpack('<13I6H4I2HI2H3I', sb[:104])
        # for i, x in enumerate(sb_data):       #testing purposes
        #     print(f'{x:10d} {sbnames[i]:s}')
        # print()

        # print("block group descriptor table:")
        bgdt = readblock(fd, 2)
        bgdt_data = struct.unpack('<3I3H', bgdt[:18])
        # for i,x in enumerate(bgdt_data):     # testing purposes
        #     print(f'{x:10d} {bgdtnames[i]:s}')
        # print()

        inode_index = bgdt_data[1]
        readbitmap(fd, inode_index)

        # print("Root Inode:")
        root_node = bgdt_data[2]
        root_node = readinode(fd, root_node, 1)
        root_data = struct.unpack('<2H5I2H3II', root_node[:44])
        # for i,x in enumerate(root_data):      testing purposes
        #     print(f'{x:10d} {itnames[i]:s}')
        # print()

        # print("LLD:")
        lld_pointer = root_data[12]
        readlld(fd, lld_pointer)

        newfile = readFile(file_for_copy)

        #Get first inode index, then run findinode
        firstinode = bgdt_data[2]
        findinode(fd, firstinode, newfile)




if __name__ == "__main__":

    main()
