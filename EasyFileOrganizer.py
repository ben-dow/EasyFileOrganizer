import datetime
import os
import sys
from tkinter import Tk
from tkinter.filedialog import askdirectory
from shutil import copyfile, copytree

'''Welcome!'''
hashes = '#' * 42
print(hashes)
print("#    Welcome to the EasyFileOrganizer    #")
print("#  github.com/ben-dow/EasyFileOrganizer  #")
print("#        Created By Ben Dow              #")
print(hashes)
print()

''' Global Helper Functions'''


def represent_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


''' User Configuration '''

date_format_display = \
    ["YYYY-DD-MM", "YYYY-MM-DD", "MM-DD-YYYY", "DD-MM-YYYY", "MMM DD YYYY"]  # Formats to display to user

date_format = \
    ["%Y-%d-%m", "%Y-%m-%d", "%m-%d-%Y", "%d-%m-%Y", "%b %d %Y"]  # Formats for use in datetime


# Function for Selecting the Date Format to use
def pick_date_format():
    while True:

        i = 1
        for d in date_format_display:  # Display the Options
            print(str(i) + ") " + d)
            i += 1

        format_number = input()

        if represent_int(format_number) and len(date_format) > int(format_number) - 1 >= 0:
            return int(format_number) - 1


''' Date Formatting '''
print("Pick a Date Format: ")
format_type = pick_date_format()
print("Format " + date_format_display[format_type] + " selected")  # Confirm Date Format

''' Preserve Sub Directories'''
print("Preserve Sub Directories? (Y/N)")
preserve_input = input()
preserve = None
if preserve_input.lower() == "y":
    preserve = True
else:
    preserve = False

''' Origin Directory '''
print("Please pick the origin directory\n")
root = Tk()
root.withdraw()
origin = askdirectory()
print("Origin Selected" + '\n' + origin)

''' Destination Directory '''
print("\nPlease Select the Destination")
dest = askdirectory()
print("Destination Selected" + '\n' + dest + '\n')

''' Confirmation of Action'''
confirm_input = input("Files inside of " + origin +
                      " will be moved to " + dest +
                      " using the format " + date_format_display[format_type] +
                      ". \nThis is okay? (Y/N)\n")

if confirm_input.lower() == "y":
    pass
else:
    print("Exiting")
    exit()

''' Process Files '''

'''Helper Functions'''


def path_str(beg, end):
    return beg + '/' + end


def path_exists(destination):
    return os.path.exists(destination)


def copy_file(orig, destination):
    if not path_exists(destination):
        copyfile(orig, destination)


def copy_folder(orig, destination):
    if not path_exists(destination):
        copytree(orig, destination)


def create_directory(parent_directory, directory_name):
    if not path_exists(path_str(parent_directory, directory_name)):
        os.makedirs(path_str(parent_directory, directory_name))


def get_time_created(path):
    time_created = os.path.getctime(path)
    return datetime.datetime.fromtimestamp(int(time_created))  # Converts to manipulable object


def move_directory_files(origin_path, destination, preserve_sub_dir, date_format_str):
    for orig_item_name in os.listdir(origin_path):  # Loop Through all items in directory

        sys.stdout.write("\rWorking on " + orig_item_name)  # Tell the user what item is currently being worked on
        sys.stdout.flush()

        date = get_time_created(path_str(origin_path, orig_item_name))  # Get the last edit date of the item
        date_directory_str = path_str(destination, date.strftime(date_format_str))  # Save the string used to create the directory for future use
        create_directory(destination, date.strftime(date_format_str))  # Create the directory with the correct date format for items

        if os.path.isfile(path_str(origin_path, orig_item_name)):  # Check if item is a file

            copy_file(path_str(origin_path, orig_item_name),
                      path_str(date_directory_str, orig_item_name))

        elif os.path.isdir(path_str(origin_path, orig_item_name)):  # Check if item is a directory
            if preserve_sub_dir:  # Preserve the sub directories of the parent directory

                copy_folder(path_str(origin_path, orig_item_name), path_str(date_directory_str, orig_item_name))
            else:  # get rid of all directories and only have the actual files
                move_directory_files(path_str(origin_path, orig_item_name), destination,
                                     preserve_sub_dir, date_format_str)


move_directory_files(origin, dest, preserve, date_format[format_type]) # run the application
