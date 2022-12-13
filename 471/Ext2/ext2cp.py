#!/usr/bin/env python3

#As of 10/16/22 this file is (mostly) working
#There are a few bugs:
#   When filling a new inode things dont quite get placed properly, should be easy fix
#   The lld is not being updated when overwriting / creating a new file. Some issue with seeking through the file to iterate through the lld.

import struct
import sys
import time
import os

from names import *

if( len(sys.argv) < 4):
        print("Usage: file system image, source, destination")
        quit()

inodes = {}
destfile = ""
file_for_copy = sys.argv[2]

def get_dir(dest):
    #If destination file is a dir, split it up into dir name and rest of path

    for i in range(len(dest)):
        if(dest[i] == '/'):
            dirfile = dest[:i]
            dest = dest[i+1:]
            break

    return dest, dirfile

def readblock(fd, n):       #parameters: descriptor and block number
    fd.seek( 1024*n)         #assuming 1024 is the block size
    return fd.read(1024)

def readinode(fd, n, m):
    fd.seek( (1024 * n) + (256 * m) )
    return fd.read(1024)

def read_blockbitmap(fd, index):
    fd.seek(1024 * index)
    bitmap = fd.read(96)

    bitmap = struct.unpack('<48c', bitmap[:48])

    # print("bitmap:",  bitmap)

    newbit = ""

    for i in range(len(bitmap)):
        newbit += str(bitmap[i])[4:-1]

    new_index = 0

    for i in newbit:
        if i == 'f':
            new_index += 4

    # print(new_index)

    return new_index

def read_inodebitmap(fd, index):
    fd.seek(1024 * index)
    bitmap = fd.read(96)

    bitmap = struct.unpack('<32c', bitmap[:32])

    # print("bitmap:",  bitmap)

    newbit = ""

    for i in range(len(bitmap)):
        newbit += str(bitmap[i])[4:-1]

    new_index = 0

    for i in newbit:
        if i == 'f':
            new_index += 4

    new_index += 1
    # print("next free inode index:", new_index)

    return new_index

def read_dir(fd, n):
    #function for reading lld's that aren't the root of the system

    dir_inodes = {}

    nextinode = 0
    fd.seek( (1024 * n) + (nextinode) )
    pointer = fd.read(1024)

    while( (struct.unpack('<IHBB', pointer[:8]))[0] != 0):
        data = struct.unpack('<IHBB', pointer[:8])
        # for i,x in enumerate(data):   #testing purposes
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
        dir_inodes.update({name : index})
        # print("inodes:", inodes) testing purposes

        #go to next lld item
        nextinode += data[1]
        if(nextinode > 256):
            break
        fd.seek( (1024 * n) + (nextinode))
        pointer = fd.read(1024)

    return dir_inodes

def edit_dir(fd, n):
    #function for editing lld's that aren't the root of the system
    #Based off of the read_dir function, tweaked for modifying rather than just getting indices and names


    nextinode = 0
    fd.seek( (1024 * n) + (nextinode) )
    pointer = fd.read(1024)

    new_lld_towrite = []

    while( (struct.unpack('<IHBB', pointer[:8]))[0] != 0):
        data = struct.unpack('<IHBB', pointer[:8])
        # for i,x in enumerate(data):   #testing purposes
        #     print(f'{x:10d} {lldnames[i]:s}')

        #Get Namelength and index
        index, reclen, namelen, filetype = data[0], data[1], data[2], data[3]


        #iterate through lld and get all characters of inode name, add them to 'name' string
        name = ""
        for i in range(namelen):
            fd.seek( (1024 * n) + nextinode + (8) + i)
            pointer = fd.read(1024)
            name += str(struct.unpack('<c', pointer[:1])[0])[2:-1]

        #once name is completed, add it and the index to inodes dict
        item = []
        item.append(index)
        item.append(reclen)
        item.append(namelen)
        item.append(filetype)
        item.append(name)
        new_lld_towrite.append(item)
        # print("inodes:", inodes) testing purposes

        #go to next lld item
        nextinode += data[1]
        if(nextinode > 256):
            break
        fd.seek( (1024 * n) + (nextinode))
        pointer = fd.read(1024)

    return new_lld_towrite

def write_iblock(fd, index, data):
    fd.seek(1024 * index)
    # print(f"Writing to {1024 * index}")
    fd.write(data)

def copy_into_dir(fd, newfile, index, firstinode):

    global inode_count, dir_inode_index

    dir_inodes = read_dir(fd, index)

    # print("dir index:", index)
    size = newfile[1][2]


    #Iterate through files of directory, when found, store index
    for inode in dir_inodes.items():

        inode_index = inode[1]
        name = inode[0]

        if(name == destfile):
            #Overwrite inode & iblock
            overwrite_file(newfile, inode_index, firstinode, name)

            #Overwrite lld data
            update_lld(fd, dir_inode_index, inode_count, destfile, size, True)
            quit()

    #Create new file in directory

    #Overwrite inode data, and then i_block data
    overwrite_file(newfile, inode_count, firstinode)

    #update directory's content, superblock, and inode bitmap
    update_superblock(fd, 1, 1)
    update_bitmaps(fd, 1, 1)
    update_lld(fd, dir_inode_index, inode_count, destfile, size)

    quit()

def overwrite_file(newfile, index, firstinode, name = False):

    # print("index:", index)

    choice = 'y'
    if(name):
        choice = input(f"cp: overwrite '{name}'? ")

    if (choice != 'y'): quit()
    else:

        #Open image for reading and writing
        with open(sys.argv[1], 'r+b') as image_for_writing:

            new_index = (1024 * firstinode) + (256 * (index - 1))

            #Seek to location of inode for replacement
            image_for_writing.seek(new_index)

            # print(f"Writing to inode {index}, index {new_index}")
            # print("index:", (1024 * firstinode) + (256 * (index - 1) ) )

            #Read inode to find the i_block location and store it for later
            data = image_for_writing.read(116)
            data = struct.unpack('<2H5I2H3IQ', data[:48])
            i_block_index = data[12]

            if(i_block_index == 0): i_block_index = free_iblock

            #pack new inode data into correct format
            inode_data = struct.pack('<2H5I2H', newfile[1][0], newfile[1][1], newfile[1][2], newfile[1][3], newfile[1][4], newfile[1][5], newfile[1][6], newfile[1][7], newfile[1][8])

            #Write data in
            #THIS IS A LITTLE BIT BROKEN. INDEX IS OFF BY A LITTLE BIT BUT MOSTLY WORKS. IDK WHY ITS OFF THOUGH.
            image_for_writing.write(inode_data)

            #Prepare i_block data for writing by formatting and packing it
            # length = len(newfile[0]) USE THIS FOR FILES OVER 1024
            length = inode_size
            iblock_data = struct.pack( '<' + str(length) + 's', bytes(newfile[0], 'utf-8'))

            #THIS CODE DOESN'T WORK PROPERLY UNLESS BOTH FILES (SOURCE AND DESTINATION) ARE THE SAME SIZE
            #Need to figure out how to handle cases with smaller or (especially) larger files

            write_iblock(image_for_writing, i_block_index, iblock_data)

            #Update superblock, inode bitmap, and lld

def update_superblock(fd, blocks_used, inodes_used):

    with open(sys.argv[1], 'r+b') as fd:
        fd.seek(1036)

        data = struct.pack('<2I', free_iblocks_count-blocks_used, free_inodes_count-inodes_used)
        fd.write(data)


def update_lld(fd, dir_inode_index, file_inode_index, name, filesize, overwrite = False):
    with open(sys.argv[1], 'r+b') as fd:

        addlinks = 0
        if(not overwrite):
            addlinks =1

        #Get original info from inode to modify it with new info
        inode = readinode(fd, dir_inode_index, firstinode_index-1)
        inode_data = struct.unpack('<2H5I2H3IQ', inode[:48])
        # print("inode data:", inode_data)
        size = inode_data[2] + filesize
        size = struct.pack('<I', size)
        i_block_index = inode_data[12]

        index = ( 1024 * firstinode_index) + ( 256 * (dir_inode_index-1) )

        #Overwrite size of dir inode
        fd.seek(index + 4)
        # print("Writing to:", (index + 4))
        fd.write(size)

        #Overwrite modtime
        fd.seek(index + 16)
        modtime = int(time.time())
        modtime = struct.pack('<I', modtime)
        # print("Writing to:", (index + 16))
        fd.write(modtime)

        fd.seek(index + 26)
        addlinks = struct.pack('<H', addlinks)
        # print("Writing to:", (index + 26))
        fd.write(addlinks)

        #Finished updating the inode of the directory
        #Next, update the lld of it

        #This function should probably grab all the lld data and store them as characters to write back later, then find the item with a rec_len > 255, make it a proper rec_len to our new file, and then append all our data
        #Then pack all that info up and write it over the lld, making it now include our file
        lld = edit_dir(fd, i_block_index)

        #Edit last rec-len and grab the old one for later
        endrec = 0
        for item in lld:
            if(item[1] > 256):
                endrec = item[1]
                item[1] = 8 + item[2] + (4 - ( (len(item[4])) % 4) )

        newfile = [file_inode_index, endrec, len(name), 1, name]

        lld.append(newfile)

        data = []

        for i in lld:
            data.append(struct.pack('<IHQQ' + str(len(str(i[4]))) + 's', i[0], i[1], i[2], i[3], bytes(i[4], 'utf-8')))


    #Theoretically this should seek through the lld (directory) of the file we are (over)writing, and write in each file of the lld at a time as it iterates through our list of packed files
    #Currently it returns a ValueError: seek of closed file (10/16/22)
    for i in range(len(data)):
        index = (1024 * i_block_index) + len(data[i])
        print("Writing to:", i_block_index * 1024)
        fd.seek(i_block_index * 1024)
        if i > 0:
            print("Writing to:", (i_block_index * 1024) + (len(data[i])) )
            fd.seek( index )
            fd.write(data[i])
        #pack lld into correct format, then write it into the iblock and the lld is updated



def update_bitmaps(fd, block_index, inode_index):
    with open(sys.argv[1], 'r+b') as fd:
        fd.seek(1024 * block_index)
        # fd.write(blocks_used+1)
        fd.seek(1024 * inode_index)
        # fd.write(inodes_used+1)


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
        # for i,x in enumerate(data):   #testing purposes
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

    global dir_inode_index

    for i in inodes.items():

            #Unpack the data for the inode
            inode = readinode(fd, firstinode, i[1]-1)
            inode_data = struct.unpack('<2H5I2H3IQ', inode[:48])
            mode = str(bin(inode_data[0]))

            #Get the name and index of current node
            name = i[0]
            inode_index = i[1]
            dest_size = inode_data[2]
            source_size = newfile[1][2]
            i_block_index = inode_data[12]

            #Program goes into three paths here:
            # 1. if destination is a directory, copy file into the directory
            #2. If destination is an existing file, copy over the file
            #3. If destination does not exist, then create it

            if(name == destdir or name == destfile):
                dir_inode_index = inode_index
                if(mode[2] == '1'):
                    copy_into_dir(fd, newfile, i_block_index, firstinode)
                    #copy file into directory
                    update_lld(fd, dir_inode_index, inode_index, destfile, source_size, True)
                    #update lld
                    quit()

                else:
                    #Copy file over old file

                    #Only overwrites iblocks according to the inode size in the superblock
                    overwrite_file(newfile, inode_index, firstinode, name)
                    update_lld(fd, dir_inode_index, inode_index, destfile, source_size, True)
                    quit()
    else:
        #Create new file with contents of the file to be copied

        #Steps:
        # Find next free inode, copy inode data into it
        #find i_blocks for inode, copy file data into it
        # Update superblock, inode bitmap, block bitmap, and lld
        overwrite_file(newfile, inode_index, firstinode, name)

        update_superblock(fd, 1, 1)
        update_bitmaps(fd, 1, 1)
        update_lld(fd, 2, inode_count, destfile, source_size)
        quit()


def readFile(file):

    #Read in file, get its inode data (mode, user id, size, etc.)
    #Add its actual contents into a string 'file_data'

    file_data = ""

    #Get inode stats of file, then put respective values into variables
    file_stats = os.stat(file)

    mode = int(file_stats[0])
    uid = int(file_stats[4])
    gid = int(file_stats[5])
    size = int(file_stats[6])
    if size > inode_size: size = inode_size
    links = 1
    atime, mtime, ctime, = int(time.time()), int(time.time()), int(time.time())


    #Make a list for the inode data and append each item to the list
    inode_data = []

    inode_data.append(mode)
    inode_data.append(uid)
    inode_data.append(size)
    inode_data.append(atime)
    inode_data.append(ctime)
    inode_data.append(mtime)
    inode_data.append(0)
    inode_data.append(gid)
    inode_data.append(links)


    #Open file for copy and get its text data to write with later
    with open(file, "rb") as fd:

        fd.seek(0)
        i_block = fd.read(size)

        for i in i_block:
            file_data+= chr(i)

    return file_data, inode_data


def main():

    global file_for_copy, destfile, destdir, inode_count, free_iblock, inode_size, firstinode_index
    global free_inodes_count, free_iblocks_count
    file_for_copy = sys.argv[2]
    destfile = sys.argv[3]

    destdir = False

    #If destination is a directory, split it into the directory name and inner file path
    for i in destfile:
        if i == '/':
            dest = get_dir(destfile)
            break

    if 'dest' in locals():
        destfile, destdir = dest[0], dest[1]


    with open(sys.argv[1], "r+b") as fd:
        # Get superblock data
        sb = readblock(fd, 1)
        sb_data = struct.unpack('<13I6H4I2HI2H3I', sb[:104])
        # for i, x in enumerate(sb_data):       #testing purposes
        #     print(f'{x:10d} {sbnames[i]:s}')
        # print()

        free_iblocks_count = sb_data[3]
        free_inodes_count = sb_data[4]

        # print(free_iblocks_count, free_inodes_count)

        inode_size = sb_data[26]
        # print("Inode size:", inode_size)

        # Get block group descriptor table data
        bgdt = readblock(fd, 2)
        bgdt_data = struct.unpack('<3I3H', bgdt[:18])
        # for i,x in enumerate(bgdt_data):     # testing purposes
        #     print(f'{x:10d} {bgdtnames[i]:s}')
        # print()

        #Get index of first inode from bgdt, read inode bitmap and store number of used inodes
        bitmap_index = bgdt_data[1]
        inode_count = read_inodebitmap(fd, bitmap_index)
        firstinode_index = bgdt_data[2]

        i_block_index = bgdt_data[0]
        free_iblock = read_blockbitmap(fd, i_block_index)

        # print("free iblock:", free_iblock)




        # Iterate through root inode to get the index for its i_block
        root_node = bgdt_data[2]
        root_node = readinode(fd, root_node, 1)
        root_data = struct.unpack('<2H5I2H3II', root_node[:44])
        # for i,x in enumerate(root_data):      #testing purposes
        #     print(f'{x:10d} {itnames[i]:s}')
        # print()

        #Assign index of roots i_block (lld) to var, read through it
        #The function readlld() reads in the data of the directory and stores the information, more info in the function itself
        lld_pointer = root_data[12]
        readlld(fd, lld_pointer)

        #Get data for file to be copied
        newfile = readFile(file_for_copy)

        #Get first inode index, then run findinode
        firstinode = bgdt_data[2]
        findinode(fd, firstinode, newfile)




if __name__ == "__main__":

    main()
