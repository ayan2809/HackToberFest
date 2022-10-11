import os
import argparse

# Generating the error messages
INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .txt file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."


def validate_file(file_name):
	'''
	validate file name and path.
	'''
	if not valid_path(file_name):
		print(INVALID_PATH_MSG%(file_name))
		quit()
	elif not valid_filetype(file_name):
		print(INVALID_FILETYPE_MSG%(file_name))
		quit()
	return

# validate file type and path	
def valid_filetype(file_name):
	return file_name.endswith('.txt')

def valid_path(path):
	return os.path.exists(path)
		
	
# get the file name/path and validate it
def read(args):
	file_name = args.read[0]

	validate_file(file_name)

	# read and print the file content
	with open(file_name, 'r') as f:
		print(f.read())


# get path to directory
def show(args):
	dir_path = args.show[0]
	
	# validate path
	if not valid_path(dir_path):
		print("Error: No such directory found.")
		exit()

	# get text files in directory
	files = [f for f in os.listdir(dir_path) if valid_filetype(f)]
	print("{} text files found.".format(len(files)))
	print('\n'.join(f for f in files))
	

	
# delete the file
def delete(args):
	file_name = args.delete[0]

	validate_file(file_name)

	os.remove(file_name)
	print("Successfully deleted {}.".format(file_name))
	

def copy(args):
	# file to be copied
	file1 = args.copy[0]
	# the file to copy upon
	file2 = args.copy[1]

	validate_file(file1)

	if not valid_filetype(file2):
		print(INVALID_FILETYPE_MSG%(file2))
		exit()

	# copies file1 to file2
	with open(file1, 'r') as f1:
		with open(file2, 'w') as f2:
			f2.write(f1.read())
	print("Successfully copied {} to {}.".format(file1, file2))


def rename(args):
	old_filename = args.rename[0]
	new_filename = args.rename[1]

	validate_file(old_filename)

	# get the type of new file name
	if not valid_filetype(new_filename):
		print(INVALID_FILETYPE_MSG%(new_filename))
		exit()

	# renaming
	os.rename(old_filename, new_filename)
	print("Successfully renamed {} to {}.".format(old_filename, new_filename))
def main():
	# create parser object
	parser = argparse.ArgumentParser(description = "A text file manager!")

	# defining arguments for parser object
	parser.add_argument("-r", "--read", type = str, nargs = 1,
						metavar = "file_name", default = None,
						help = "Opens and reads the specified text file.")
	
	parser.add_argument("-s", "--show", type = str, nargs = 1,
						metavar = "path", default = None,
						help = "Shows all the text files on specified directory path.\
						Type '.' for current directory.")
	
	parser.add_argument("-d", "--delete", type = str, nargs = 1,
						metavar = "file_name", default = None,
						help = "Deletes the specified text file.")
	
	parser.add_argument("-c", "--copy", type = str, nargs = 2,
						metavar = ('file1','file2'), help = "Copy file1 contents to \
						file2 Warning: file2 will get overwritten.")
	
	parser.add_argument("--rename", type = str, nargs = 2,
						metavar = ('old_name','new_name'),
						help = "Renames the specified file to a new name.")

	# parse the arguments from standard input
	args = parser.parse_args()
	
	# calling functions depending on type of argument
	if args.read != None:
		read(args)
	elif args.show != None:
		show(args)
	elif args.delete !=None:
		delete(args)
	elif args.copy != None:
		copy(args)
	elif args.rename != None:
		rename(args)


if __name__ == "__main__":
	# calling the main function
	main()
