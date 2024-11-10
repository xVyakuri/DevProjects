# Author: Andrew Xie
# Date: 10/27/2024

import subprocess
import os
import time
import json

# This Program asks the User for a file and will create a shortcut for that file
# This file can be anywhere

# for whenever i need to clear the terminal to make everything cleaner
def clear_terminal():
	os.system('clear')

# have something for desktop path
def getDesktopPath():
	return os.path.join(os.path.expanduser("~"), "Desktop")
	
# finding the filename with the find command
def findFile(filename, search_path="/"):
	# go through every directory from the starting path of "/" unless paramater is different
	for dirpath, _, files in os.walk(search_path):
		if filename in files:
			return os.path.join(dirpath, filename)
	
	return None
	
	
def read_Link(targetPath):
	try:
		# Based on the relative path of a target file, get the absolute path
		absolutePath = subprocess.check_output(["readlink", "-f", targetPath], text=True).strip()
		return absolutePath
	except subprocess.CalledProcessError as e:
		print(f"Error reading link: {e}")
		return None
                                       

# Function for making a shortcut
def createShortcut(targetPath):
	# Find the shortcut of that filename and ask if the user wants to actually create the shortcut
		
	desktopPath = getDesktopPath()
	# just make a shortcut for the first file that appeared in the system
	absolutePath = read_Link(targetPath)
	if absolutePath is None:
		print(f"Could not Read the link for {targetPath}")
		return
	
	shortcutName = os.path.basename(absolutePath)
	shortcutPath = os.path.join(desktopPath, f"{shortcutName}")

	try:
		if not os.path.exists(shortcutPath):
			subprocess.check_call(["ln", "-s", absolutePath, shortcutPath])
			print(f"Shortcut created on Desktop: {shortcutPath}")
		else:
			print("Shortcut already exists on the desktop.")
	except FileExistsError:
		print("Error: A file with that name already exists on the Desktop.")
	except PermissionError:
		print("Error: You do not have permission to create a link on the Desktop.")
	except Exception as e:
		print(f"An unexpected error occured: {e}")
		
			
	print("Returning to Main Menu...")
	time.sleep(5)
	

# Function for deleting a shortcut from user's Desktop
def deleteShortcut():
	clear_terminal()
	# Ask for the filename of the specific shortcut
	shortcutName = str(input("Please enter the shortcut/link to remove:\t"))
	
	desktopPath = getDesktopPath()
	shortcutPath = os.path.join(desktopPath, shortcutName)
	
	# Ask for confirmation to delete from home directory
	continuing = str(input("Are you sure you want to delete this shortcut? Enter (Y/y)\t"))
	
	if continuing == "y":
		if os.path.islink(shortcutPath):
			try:
				os.unlink(shortcutPath)
				print(f"Shortcut '{shortcutName}' has been deleted from the Desktop.")
			except Exception as e:
				print(f"An unexpected error occured: {e}")
		else:
			print("Error: The specified shortcut does not exist or is not a symbolic link.")
	
	print("Returning to Main Menu...")
	time.sleep(5)

# Function to report all of the files and their corresponding shortcuts on the User's Desktop
def systemReport():
	clear_terminal()	
	
	desktopPath = getDesktopPath()
	shortcuts = {}
	totalCount = 0
	
	for i in os.listdir(desktopPath):
		iPath = os.path.join(desktopPath, i)
		if os.path.islink(iPath):
			targetPath = os.readlink(iPath)
			shortcuts[i] = targetPath
			totalCount += 1
			
	if shortcuts:
		print("\nReport of all Shortcuts on the Desktop:\n\nTotal Shortcuts = " + str(totalCount))
		for name, target in shortcuts.items():
			print(f"{name} \t->\t {target}")
	else:
		print("No Shortcuts found on the Desktop.")
	
	print("Returning to Main Menu...")
	time.sleep(5)

# Main
def main():
	while True:
		print("\n\t\t\tWelcome to the Symbolic Link Creator\n")
		
		clear_terminal()
		# Print out 3 options to do, (1) create a shortcut, (2) delete a shortcut, 3) Make shortcut report
		print("Enter Selection:\n\n"
			+ "\t1 - Create a Shortcut in your Home Directory.\n"
			+ "\t2 - Remove a Shortcut from your Home Directory.\n"
			+ "\t3 - Run a Shortcut Report.\n"
			+ "\nPlease enter a number (1 - 3) or 'Q/q' to quit the program.")
			
		choice = str(input(""))
		
		# Call other functions based on choice
		# if 1 make shortcut function
		if choice == "1":
			clear_terminal()
			# Ask for filename
			filename = str(input("Please enter the file name to create a shortcut:\t"))
			foundFile = findFile(filename)
			
			if foundFile:
				# Ask for confirmation to delete from home directory
				print("File Found")
				continuing = str(input("Are you sure you want to create this shortcut? Enter (Y/y)\t"))
				
				if continuing == "y":
					createShortcut(foundFile)
			else:
				print(f"Error: The file '{filename}' was not found on the system.")
				print("Returning to Main Menu...")
				time.sleep(5)
		# if 2 delete shortcut function
		elif choice == "2":
			deleteShortcut()
		# if 3 make system report function
		elif choice == "3":
			systemReport()
		# if quit exit the program nicely
		elif choice.lower() == "q":
			print("Exiting Program.")
			time.sleep(1)
			
			break
		else:
			print("Invalid Choice Option")
		
	print("Goodbye...")
	
	clear_terminal()
	
if __name__ == "__main__":
	main()
		
		
		
