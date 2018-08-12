import datetime
import os
import sys
from tkinter import Tk
from tkinter.filedialog import askdirectory
from shutil import copyfile

''' User Configuration '''

date_format_display = ["YYYY-DD-MM", "YYYY-MM-DD", "MM-DD-YYYY", "DD-MM-YYYY", "MMM DD YYYY"]
date_format = ["%Y-%d-%m", "%Y-%m-%d", "%m-%d-%Y", "%d-%m-%Y", "%b %d %Y"]

print("Pick a Date Format: ")


def pick_date_format():
    i = 1
    for d in date_format_display:
        print(str(i) + ") " + d)
        i += 1
    return input()


format_type = int(pick_date_format()) - 1

while format_type < 0 or format_type > len(date_format) - 1:
    format_type = int(pick_date_format()) - 1

print("Format " + date_format_display[format_type] + " selected")
print("Please pick the origin directory\n")

root = Tk()
root.withdraw()

origin = askdirectory()

print("Origin Selected" + '\n' + origin)

print("\nPlease Select the Destination")
dest = askdirectory()

print("Destination Selected" + '\n' + dest + '\n')

confirm_input = input("Files inside of " + origin + " will be moved to " + dest + "using the format" + date_format[
    format_type] + ". \nThis is okay? (Y/N)\n")

if confirm_input.lower() == "y":
    pass
else:
    print("Exiting")
    exit()

''' Process Files '''


def check_folder_exists(dest):
    if not os.path.exists(dest):
        os.makedirs(dest)


def move_file(file_path, filename):
    time_created = os.path.getctime(file_path)
    time_created = datetime.datetime.fromtimestamp(int(time_created))  # Converts to manipulable object

    dest_folder = dest + "/" + time_created.strftime(date_format[format_type])
    check_folder_exists(dest_folder)

    if not os.path.exists(dest_folder + '/' + filename):
        copyfile(file_path, dest_folder + '/' + filename)

num_files = len(os.listdir(origin))
files_done = 0
sys.stdout.write("Working on File " + str(files_done + 1) + " of " + str(num_files))
sys.stdout.flush()
for file in os.listdir(origin):
    sys.stdout.write("\rWorking on File " + str(files_done + 1) + " of " + str(num_files))
    sys.stdout.flush()
    if os.path.isfile(origin + '/' + file):
        move_file(origin + '/' + file, file)
    files_done += 1
