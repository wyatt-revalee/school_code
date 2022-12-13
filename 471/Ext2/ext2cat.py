#!/usr/bin/env python3

import struct
import sys
import time
import os

from names import *

inodes = {}
destfile = ""

def readblock(fd, n):       #parameters: descriptor and block number
    fd.seek( 1024*n)         #assuming 1024 is the block size
    return fd.read(1024)

def readinode(fd, n, m):
    fd.seek( (1024 * n) + (256 * m) )
    return fd.read(1024)

def readlld(fd, n):

    global inodes

    #Get root inode info
    nextinode = 0
    fd.seek( (1024 * n) + (nextinode) )
    pointer = fd.read(1024)

    #Loop through lld, putting names and indices of all inodes into "inodes" dictionary in format {name : index}

    #Check to make sure next inode isnt end of lld
    while( (struct.unpack('IHBB', pointer[:8]))[0] != 0):
        data = struct.unpack('IHBB', pointer[:8])
        # for i,x in enumerate(data):   testing purposes
        #     print(f'{x:10d} {lldnames[i]:s}')

        #Get Namelength and index
        index, namelen = data[0], data[2]


        #iterate through lld and get all characters of inode name, add them to 'name' string
        name = ""
        for i in range(namelen):
            fd.seek( (1024 * n) + nextinode + (8) + i)
            pointer = fd.read(1024)
            name += str(struct.unpack('c', pointer[:1])[0])[2:-1]

        #once name is completed, add it and the index to inodes dict
        inodes.update({name : index})
        # print("inodes:", inodes) testing purposes

        #go to next lld item
        nextinode += data[1]
        if(nextinode > 256):
            break
        fd.seek( (1024 * n) + (nextinode))
        pointer = fd.read(1024)

def printinode(fd, firstinode):
    #iterate through dict of inodes
    for i in inodes.items():

            #Unpack the data for the inode
            inode = readinode(fd, firstinode, i[1]-1)
            inode_data = struct.unpack('2H5I2H3II', inode[:44])
            mode = str(bin(inode_data[0]))
            file_data_index = inode_data[12]

            #Assign the values for printing
            name = i[0]
            file_data = ""
            if(name == destfile):
                if(mode[2] == '1'):
                    print(f"cat: {name}: Is a directory")
                    quit()
                else:
                    file_data = []

                    for i in range(1000):

                        fd.seek( (1024 * (file_data_index)) + i )
                        pointer = fd.read(1024)
                        file_data.append((struct.unpack('c', pointer[:1])[0])[0])
                    file_text = ""
                    for i in file_data:
                        file_text += chr(i)
                    print(file_text)
                    quit()

def binToRWX(bin):
    rwx = ""
    if(bin[2]):
        rwx += 'd'
    else:
        rwx += '-'
    for i in range(8, 17):
        if(bin[i] == '1' and (i == 8 or i == 11 or i == 14)):
            rwx += 'r'
        elif(bin[i] == '1' and (i == 9 or i == 12 or i == 15)):
            rwx += 'w'
        elif(bin[i] == '1' and (i == 10 or i == 13 or i == 16)):
            rwx += 'x'
        else:
            rwx += '-'
    return rwx

def formatDate(date):
    return time.strftime('%b %d %H:%M', time.localtime(date))

def main():
    global destfile
    destfile = sys.argv[2]

    with open(sys.argv[1], "rb") as fd:
        # print("superblock:")
        sb = readblock(fd, 1)
        sb_data = struct.unpack('<13I6H4I2HI2H3I', sb[:104])
        # for i, x in enumerate(sb_data):       testing purposes
        #     print(f'{x:10d} {sbnames[i]:s}')
        # print()

        # print("block group descriptor table:")
        bgdt = readblock(fd, 2)
        bgdt_data = struct.unpack('3I3H', bgdt[:18])
        # for i,x in enumerate(bgdt_data):      testing purposes
        #     print(f'{x:10d} {bgdtnames[i]:s}')
        # print()

        # print("Root Inode:")
        root_node = bgdt_data[2]
        root_node = readinode(fd, root_node, 1)
        root_data = struct.unpack('2H5I2H3II', root_node[:44])
        for i,x in enumerate(root_data):      #testing purposes
            print(f'{x:10d} {itnames[i]:s}')
        print()

        # print("LLD:")
        lld_pointer = root_data[12]
        readlld(fd, lld_pointer)


        #Get first inode index, then run printInode
        firstinode = bgdt_data[2]
        printinode(fd, firstinode)
        print(f"cat: {destfile}: No such file or directory")


if __name__ == "__main__":

    main()
