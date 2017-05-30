"""
This is a self contained LRU Cache implementation module
"""
from collections import OrderedDict
import csv

class LRUCache(object):
    """
    This class contains all the methods for the LRU Cache implementation
    """
    def __init__(self):
        """
        The  __init__(self) method initializes the values of the queue, the number of elements
        in the queue, reader and writer object and the fieldnames of the csv file
        """
        self.reader = None
        self.writer = None
        self.fieldnames = None
        self.lru_queue = OrderedDict()
        self.cache_count = 0

    def get_csv_file(self):
        """
        The  get_csv_file(self) method reads the csv file into reader object and inserts into
        lru_queue. We convert the Total marks to float for sorting the data when we exit
        """
        with open("students.csv", "rb") as file_obj:
            self.reader = csv.DictReader(file_obj, delimiter=',')
            self.fieldnames = self.reader.fieldnames
            for row in self.reader:
                temp = dict(row)
                temp['Total'] = float(temp['Total'])
                self.lru_queue[temp['ID']] = temp
                self.cache_count = self.cache_count + 1

    def set_csv_data(self, data, fieldnames):
        """
        The set_csv_file(self) method first clears the entire csv file including the headers,
        then we write the header and the the individual row in the queue.
        """
        file_obj = open("students.csv", "w+")
        file_obj.close()
        with open("students.csv", "w") as f_obj:
            self.writer = csv.DictWriter(f_obj, fieldnames=fieldnames)
            self.writer.writeheader()
            for item in data:
                self.writer.writerow(item)
        print "-/-/-/-/-/-/-/-/-/-/-/Exiting the program.-/-/-/-/-/-/-/-/-/-/-/-/-/"

    def update_lru_queue(self, student_data):
        """
        The update_lru_queue(self) method updates the current queue containing csv data
        with a new value provided in the method
        """
        self.lru_queue[student_data['ID']] = student_data
        self.cache_count = self.cache_count + 1

    def create_new_data(self):
        """
        The create_new_data(self) method takes various input values of a student, calculates
        the total, then create a dictionary object and sends the dictionary to
        update_lru_queue(self, student_data)
        """
        if self.cache_count == 20:
            self.lru_queue.popitem(last=False)
        print "Please enter the follwing details:"
        print "Enter student's ID:"
        student_id = raw_input()
        print "Enter student's Name:"
        student_name = raw_input()
        print "Enter student's marks in Science if enrolled else enter \"-\" without quotes:"
        science_marks = raw_input()
        print "Enter student's marks in Maths if enrolled else enter \"-\" without quotes:"
        maths_marks = raw_input()
        print "Enter student's marks in English if enrolled else enter \"-\" without quotes:"
        english_marks = raw_input()
        total = 0.0
        if science_marks != '-':
            total = total+float(science_marks)
        if maths_marks != '-':
            total = total+float(maths_marks)
        if english_marks != '-':
            total = total+float(english_marks)
        student_data = {'ID':student_id,
                        'Name':student_name,
                        'Science':science_marks,
                        'Maths':maths_marks,
                        'English':english_marks,
                        'Total':total}
        print "-/-/-/-/-/-/-/-/-/-/-/Values added successfully.-/-/-/-/-/-/-/-/-/-/"
        self.update_lru_queue(student_data)

    def read_csv_data(self):
        """
        The read_csv_file(self) method shows the student values based on the ID of the student
        """
        if self.cache_count == 0:
            print "No data present in file."
        else:
            print "Enter the ID of the Student:"
            student_id = raw_input()
            if student_id in self.lru_queue:
                student_data = self.lru_queue[student_id]
                print "***************  Student ID    : ", student_data['ID']
                print "***************  Stduent Name  : ", student_data['Name']
                print "***************  Science Marks : ", student_data['Science']
                print "***************  Maths Marks   : ", student_data['Maths']
                print "***************  English Marks : ", student_data['English']
                print "***************  Total Marks   : ", student_data['Total']
                data = self.lru_queue.pop(student_id)
                self.cache_count = self.cache_count - 1
                self.update_lru_queue(data)
            else:
                print "No such student found."

    def update_csv_data(self):
        """
        The update_csv_file(self) method takes the ID of student whose data needs to be updated.
        Then if ID is available it calls the create_new_data(self) method
        """
        if self.cache_count == 0:
            print "No data present in file."
        else:
            print "Enter the ID of the Student:"
            student_id = raw_input()
            if student_id in self.lru_queue:
                self.lru_queue.pop(student_id)
                self.cache_count = self.cache_count - 1
                self.create_new_data()
            else:
                print "No such student found."

    def delete_csv_data(self):
        """
        The delete_csv_file(self) method takes the ID of student whose data needs to be updated.
        Then if ID is available it removes the student data from the queue
        """
        if self.cache_count == 0:
            print "No data present in file."
        else:
            print "Enter the ID of the Student:"
            student_id = raw_input()
            if student_id in self.lru_queue:
                self.lru_queue.pop(student_id)
                self.cache_count = self.cache_count - 1
                print "-/-/-/-/-/-/-/-/-/-/-/-/Student deleted successfully.-/-/-/-/-/-/-/-/-/-/-/"
            else:
                print "No such student found."

    def exit(self):
        """
        The exit(self) method sorts the students data in the queue and sends the sorted data
        to the set_csv_data(self, data, fieldnames)
        """
        print "-/-/-/-/-/-/-/-/-/-/-/-/Please wait while we exit.-/-/-/-/-/-/-/-/-/-/-/-/-/"
        if self.cache_count > 0:
            students_data = []
            for value in self.lru_queue.itervalues():
                students_data.append(value)
            sorted_data = sorted(students_data, key=lambda k: k['Total'], reverse=True)
            self.set_csv_data(sorted_data, self.fieldnames)

    def start(self):
        """
        The start(self) method displayes the menu to the user and takes in the input of the option.
        """
        option = None
        self.get_csv_file()
        while option != 'E':
            print """Please enter one of the options to proceed:
---------  Create an Entry:: C  ------------------------
---------  Read an Entry:: R    ------------------------
---------  Update an Entry:: U  ------------------------
---------  Delete an Entry:: D  ------------------------
---------  Exit:: E             ------------------------------------"""
            option = raw_input()
            print option
            if option == 'C':
                self.create_new_data()
            if option == 'R':
                self.read_csv_data()
            if option == 'U':
                self.update_csv_data()
            if option == 'D':
                self.delete_csv_data()
            if option == 'E':
                self.exit()
                break

if __name__ == "__main__":
    LRU = LRUCache()
    LRU.start()
