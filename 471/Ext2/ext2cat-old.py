#!/usr/bin/env python3

import sys
import subprocess

#Create a program that acts as if you would run "ls -ail /" on the ext2 file system image
#inode number, permissions, links, owner name, owner group, file size, time of last modification, and file or directory name

def liHexToDec(value):
    value.reverse()
    value = ''.join(value)
    value = int(value, 16)
    return value

def pointerToIndex(pointer):
    pointer = liHexToDec(pointer)
    pointer = (pointer-1) * 256
    pointer = pointer + firstInodeIndex
    return str(pointer)

def getName(index):
    currentHexName = []
    currentName = ""
    for i in range(len(lld)):
        if (i == index):
            while(lld[i] != '00'):
                currentHexName.append(lld[i])
                i+= 1
    currentHexName.reverse
    for letter in currentHexName:
        letter = int(letter, 16)
        currentName += chr(letter)
    return currentName


def printInode(index, nameIndex):
    mode, name, i_block_index, i_block = "mode", "name", [], ""
    name = getName(nameIndex)
    buffer = 7 % len(index)
    currentInode = ""
    index = str(int(index) + 256)
    for i in range(len(image)):
        if(image[i][buffer:7] == index):
            mode = bin(liHexToDec(list(image[i][8:13].split(' '))))
            while(image[i][0] != '*'):
                currentInode += image[i][8:] + ' '
                i+=1
            break
    currentInode = currentInode.split(' ')[:-1]
    if(file == name):
        if(mode[2] == '1'):
            print(f"cat: {name}: Is a directory")
        else:
            i_block_index.append(currentInode[40])
            i = 1
            while(currentInode[40+i] != '00'):
                i_block_index.append(currentInode[40+i])
                i += 1
            i_block_index = str(liHexToDec(i_block_index) * 1024)
            buffer = 7 % len(i_block_index)
            for i in range(len(image)):
                if(image[i][buffer:7] == i_block_index):
                    while(image[i][0] != '*'):
                        i_block += image[i][8:] + ' '
                        i += 1
            i_block = i_block.split(' ')[:-1]
            i_block_data = ""
            for letter in i_block:
                letter = int(letter, 16)
                i_block_data += chr(letter)
            print(i_block_data)


#Get readable version of image and store it in variable called image, splitting it line by line
image = sys.argv[1]
file = sys.argv[2]
image = subprocess.check_output(f"od -Ad -t x1 {image}", shell=True, text="utf-8")
image = image.split('\n')

for i in image:
    if(i[0:7] == '0001600'):
        lldIndex = i

for i in image:
    if(i[0:7] == '0002048'):
        firstInodePointer = i

firstInodeIndex = list(firstInodePointer[32:43].split(' '))
firstInodeIndex = liHexToDec(firstInodeIndex)*1024

#Get pointer to linked list directory from the line 1600
#Turn to list, reverse, then turn to string to make things easier
#convert to decimal and multiply by 1024 to find lld index
#there is probably a more efficient way to do this
lldPointer = list(lldIndex[32:43].split(" "))
lldPointer = str(liHexToDec(lldPointer)*1024)

#Make buffer to properly find index of lld
#scan through image to find lld, once found, add all lines of it to lld variable
buffer = 7 % len(lldPointer)
lld = ""
for i in range(len(image)):
    if(image[i][buffer:7] == lldPointer):
        while(image[i] != '*'):
            lld += image[i][8:] + ' '
            i+=1
lld = lld.split(' ')[:-1]

#From the lld, get the index of the current inode(to be worked on) and the next one


lldCurrIndex = 0
lldNextIndex = liHexToDec(lld[lldCurrIndex+4:lldCurrIndex+6])

while(lldNextIndex):
    nameIndex = lldCurrIndex + 8
    currentIndex = lld[lldCurrIndex:lldCurrIndex+4]
    currentIndex = pointerToIndex(currentIndex)
    printInode(currentIndex, nameIndex)
    buffer = lldNextIndex + lldCurrIndex
    lldCurrIndex += lldNextIndex
    if(len(lld[buffer+4:buffer+6]) == 0):
        break
    lldNextIndex = liHexToDec(lld[buffer+4:buffer+6])
