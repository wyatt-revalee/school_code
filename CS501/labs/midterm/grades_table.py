#!/usr/bin/env python3

import urllib.request

#For this assignment I am reusing my read_csv function from lab3/utils.py
def read_csv(file_path, field_sep=",", record_sep="\n"):
    with urllib.request.urlopen(file_path) as req:
        data =  req.read().decode("utf-8")
    data = data.split('\n')
    keys = []
    linedData = []

    #Create list from csv file, put the keys in a list names keys, and the rest of the data in separate lines of a list name linedData
    for i in range(len(data)):
        if(i == 0):
            keys = data[i].split(',')
        else:
            linedData.append(data[i].split(','))

    #Iterate through lined data, make dictionaries with the 'keys' list as keys (first, last, a1-a6) and the values as the student's respective values. Once an entry is complete, add the dictionary to the 'data' dictionary, creating dictionary of dictionaries, with numbered indices as keys and student data as values, and return it.

    #As a second thought / side note: This might make more sense with 'data' as a list, but I am used to the dicts so I'm not gonna bother changing it for this assignment
    data = {}
    for i in range(len(linedData)):
        tempDict = {}
        j = 0
        for line in linedData[i]:
            tempDict.update({keys[j]: line})
            j += 1
            if(j == len(keys)):
                data.update({i: tempDict})
    return data


def get_students(student_data):

    students = []

    #Iterate through students, add them to a list, students, if they meet the criteria:
#My Name: Wyatt Revalee
#1. first letter of first name = "w' AND first letter of last name = 'r'
#2. second letter of first name = 'y' AND second letter of last name = 'e'
#3. last letter of first name = 't' AND last letter of last name = 'e'

    for data in student_data.values():
        if(data['First Name'][0].upper() == 'W' and data['Last Name'][0].upper() == 'R'):
            students.append(data)
        elif(data['First Name'][1].upper() == 'Y' and data['Last Name'][1].upper() == 'E'):
            students.append(data)
        elif(data['First Name'][-1].upper() == 'T' and data['Last Name'][-1].upper() == 'E'):
            students.append(data)

    return students

def get_names_and_average(students):

        #Make new dict to hold students names and their scores, format: {last, first : average grade}
    names_and_scores = {}

    for i in students:
        first = i['First Name']
        last = i['Last Name']

        #Iterate through students scores, add them all, and divide to get the average
        scores = 0
        for num in range(1,6):
            scores += float(i[f'Assignment {num}'])
        scores = scores/6

        #Add students names and scores to new dict (see above)
        names_and_scores.update({ last + ', ' + first : scores})

    return names_and_scores

def get_class_average(names_and_scores):

    #Iterate through student scores, add them all together (scores) and keep track of how many scores there are (count)
    count = 0
    scores = 0
    for i in names_and_scores.values():
        scores += i
        count += 1

    #Return the average percentage (sum of student scores / amount of students)
    return (scores/count)


def main():

    #Run functions, store in data, and pass that data to next function
    #More details in comments of functions

    student_data = read_csv("https://cs.indstate.edu/~lmay1/assets/fake-grades.csv")

    students = get_students(student_data)

    names_and_scores = get_names_and_average(students)

    avg = get_class_average(names_and_scores)
    avg = "{:.2f}".format(avg)

    padding = ' '*30

    #Loop through students, print their names and scores as specified (reducing to 2 decimal places and adding a buffer of space padding)
    #This also makes uses of sorted() to sort the dictionary by last name, not sure if this is what was wanted though.
    for i in sorted(names_and_scores.items()):
        #Get name and create buffer
        name = i[0]
        buffer = len(name)

        #If name is longer than 30 characters, truncate it to 30
        if( len(name) > 30):
            name = name[:30]

        #Format average to 2 decimal places (0.00)
        average = "{:.2f}".format(i[1])

        print(name + padding[buffer:] + ' | ' + str(average) + ' %')

    #Print line of hyphens '-' and then on the next line print the average score of students, formatted as specified
    print('-'*41)
    print("Average" + padding[7:] + ' | ' + avg + ' %')

if __name__ == "__main__":
        main()
