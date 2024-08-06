# ------------------------------------------------------------------------------------------ #
# Title: Assignment06_Starter
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   John Lewandowski,08/05/24, Initial attempt
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables and constants
students: list = []  # Table of student data
menu_choice: str  # Hold the choice made by the user.


class FileProcessor:
    """A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    John Lewandowski, 08/05/24, Created class
    """

    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads from a JSON file and loads the data into a dictionary

               ChangeLog: (Who, When, What)
               John Lewandowski, 08/05/24, Created function

               return: list"""
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except Exception as e:
            IO.output_error_messages(message="There was a problem reading the file", error=e)
        finally:
            if file.closed == False:
                file.close()
        return student_data

    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a JSON file from a list of dictionary rows

        ChangeLog: (Who, When, What)
        John Lewandowski, 08/05/24, Created function

        return: None"""
        try:
            file = open(file_name, "w")
            json.dump(student_data, file)
            file.close()
            IO.output_student_courses(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem writing the file"
            message += "Please check the file is not already open"
            IO.output_error_messages(message=message, error=e)
        finally:
            if file.closed == False:
                file.close()


class IO:
    """A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    John Lewandowski, 08/05/24, Created class
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error message to the user

        ChangeLog: (Who, When, What)
        John Lewandowski, 08/05/24, Lab 3 follow

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays a menu of choices to the user

        ChangeLog: (Who, When, What)
        John Lewandowski, 08/05/24, Lab 3 follow

        :return: None
        """
        print()
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user
        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Only 1, 2, 3, or 4 are valid options")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing the exception object to avoid the technical message

        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function
        RRoot,1.4.2030,Added code to toggle technical message off if no exception object is passed
        John Lewandowski, 08/05/24, Assignment 6 attempt 1
        :return: None
        """
        # Process the data to create and display a custom message
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} '
                  f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the Student data (First, Last, Course) from the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function
        John Lewandowski, 08/05/24, Assignment 6 adjustment
        :return: list with the new student data added
        """
        try:
            # Input the data
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Enter the name of the course: ")
            student = {"FirstName": student_first_name,
                       "LastName": student_last_name,
                       "CourseName": course_name}
            student_data.append(student)
            print()  # extra spacing
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="Error: One of your data is not the correct type.", error=e)
        except Exception as e:
            IO.output_error_messages(message="Entered data caused an error", error=e)
        return student_data


# Main Body
# When the program starts, read the file data into a list of lists (table)
# Extract data from file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):
    # Present the menu of choices
    IO.output_menu(menu=MENU)
    # Prompt user to make a choice
    menu_choice = IO.input_menu_choice()
    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue
    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue
    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue
    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")
print("Program Ended")
