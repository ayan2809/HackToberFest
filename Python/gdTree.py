import os
import argparse
import datetime

TAB_PADDING = 3
TAB = ' ' * TAB_PADDING
KB = 1000
MB = 1000000
GB = 1000000000
TB = 1000000000000

def getCommandLineArguments():
    programParser = argparse.ArgumentParser(
        add_help=False,
        prog="gdTree",
        usage="%(prog)s dir [-depth] [-sort_by] [-sort_order] [-display_size] [-display_date] [-dir_first]",
        description="Generates the subdirectory tree of a given directory.",
        epilog="""
            .______________                      
   ____   __| _/\__    ___/______   ____   ____  
  / ___\ / __ |   |    |  \_  __ \_/ __ \_/ __ \ 
 / /_/  > /_/ |   |    |   |  | \/\  ___/\  ___/ 
 \___  /\____ |   |____|   |__|    \___  >\___  >
/_____/      \/                        \/     \/

For any issues, feel free to contact me.
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    programParser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS,
        help="Show instructions on how to use this command.\n\n"
    )
    programParser.add_argument("dir",
        action="store",
        type=str,
        help="The directory whose tree will be generated.\n"
    )
    programParser.add_argument("-depth",
        action="store",
        nargs=1,
        type=int,
        default=-1,
        help="The maximum depth at which the program is allowed to go and generate the tree.\n\n"
    )
    programParser.add_argument("-sort_by",
        action="store",
        nargs=1,
        choices=["date_created", "date_modified", "date_accessed", "size", "extension","alpha"],
        default="alpha",
        metavar="",
        help="""The criteria based on which the program will sort the files / subdirectories. Possible values:\n
1) 'date_created': Date in which the entry was created.
2) 'date_modified': The last time that the entry was modified.
3) 'date_accessed': The last time that the entry was accessed.
4) 'size': The size of the entry.
5) 'extension': The extension of the entry.
6) 'alpha': Alphabetical order based on the name of the entry.\n\n"""
    )
    programParser.add_argument("-sort_order",
        action="store",
        nargs=1,
        choices=["asc", "desc"],
        default="asc",
        metavar="",
        help="The order of the files after sorting. It takes two values:\n1) 'asc': Ascending order.\n2) 'desc': Descending order.\n\n"
    )
    programParser.add_argument("-display_size",
        action="store",
        nargs=1,
        type=bool,
        default=0,
        help="Flag variable to decide whether or not to display the size of files / subdirectories.\n\n"
    )
    programParser.add_argument("-display_date",
        action="store",
        nargs=1,
        type=bool,
        default=0,
        help="Flag variable to decide whether or not to display the date of files / subdirectories, based on the sort_by criteria. It defaults to date of creation.\n\n"
    )
    programParser.add_argument("-dir_first",
        action="store",
        nargs=1,
        type=bool,
        default=0,
        help="Flag variable to decide whether or not to place directories before or after files, when generating the tree."
    )
    return programParser.parse_args()

def getEntrySize(entry):
    entrySize = None
    if entry.is_dir():
        entrySize = getDirectorySize(entry)
    else:
        entrySize = getFileSize(entry)
    return entrySize

def getFormattedEntrySize(entry):
    entrySize = getEntrySize(entry)
    return formatSize(entrySize)

def formatSize(entrySize):
    if entrySize < 1000:
        suffix = 'B'
    elif KB <= entrySize < MB:
        entrySize = round(entrySize / KB, 2)
        suffix = 'KB'
    elif MB <= entrySize < GB:
        entrySize = round(entrySize / MB, 2)
        suffix = 'MB'
    elif GB <= entrySize < TB:
        entrySize = round(entrySize / GB, 2)
        suffix = 'GB'
    else:
        entrySize = round(entrySize / TB, 2)
        suffix = 'TB'
    return '({} {})'.format(entrySize, suffix)

def getFileSize(file_entry):
    return file_entry.stat().st_size

def getDirectorySize(dir_entry):
    totalSize = 0
    with os.scandir(dir_entry) as d:
        for entry in d:
            if entry.is_file():
                totalSize += getFileSize(entry)
            else:
                totalSize += getDirectorySize(entry)
    return totalSize

def getEntryDate(entry, date='date_created'):
    timestamp = None
    if date == 'date_created':
        timestamp = os.stat(entry).st_ctime
    elif date == 'date_modified':
        timestamp = os.stat(entry).st_mtime
    else:
        timestamp = os.stat(entry).st_atime
    timestamp = int(timestamp)
    return "[{}]".format(datetime.datetime.fromtimestamp(timestamp))

def getDirSortedBySize(d):
    return sorted(d, key=lambda entry: getEntrySize(entry))

def getDirSortedByExtension(d):
    return sorted(d, key=lambda entry: str.lower(os.path.splitext(entry)[1]))

def getDirSortedByAlpha(d):
    return sorted(d, key=lambda entry: str.lower(entry.name))

def getDirSortedByDate(d, date_type='date_created'):
    if date_type=='date_modified':
        return getDirSortedByModificationDate(d)
    elif date_type=='date_accessed':
        return getDirSortedByLastAccessedDate(d)
    else:
        return getDirSortedByCreationDate(d)

def getDirSortedByCreationDate(d):
    return sorted(d, key=lambda entry: os.stat(entry).st_ctime)

def getDirSortedByModificationDate(d):
    return sorted(d, key=lambda entry: os.stat(entry).st_mtime)

def getDirSortedByLastAccessedDate(d):
    return sorted(d, key=lambda entry: os.stat(entry).st_atime)

def getDirSortedBy(d, key):
    sortDict = {
        'date_created' : getDirSortedByCreationDate, 
        'date_modified' : getDirSortedByModificationDate,
        'date_accessed' : getDirSortedByLastAccessedDate,
        'size' : getDirSortedBySize,
        'extension' : getDirSortedByExtension,
        'alpha' : getDirSortedByAlpha
    }
    return sortDict[key](d) if key in sortDict else d

def getSortedDir(directory, asc):
    dirs = []
    files = []
    for entry in directory:
        if entry.is_file():
            files.append(entry)
        else:
            dirs.append(entry)
    if asc:
        return dirs + files
    else:
        return files + dirs

def getSortedEntries(directory, order):
    if order=='desc':
        directory.reverse()
    return directory
 
def generateTree(directoryName, maxDepth=-1, displaySize=False, displayDate=False, dirFirst=False, sortBy="alpha", order="asc"):
    print(directoryName)
    genSubtree(directoryName, 1, maxDepth, displaySize, displayDate, dirFirst, sortBy, order, [""])

def genSubtree(directoryName, level, maxDepth, displaySize, displayDate, dirFirst, sortBy, order, padding):
    entrySize = ''
    entryDate = ''
    if maxDepth == -1 or (maxDepth > -1  and level <= maxDepth):   
        with os.scandir(directoryName) as d:

            newDir = getDirSortedBy(d, sortBy)
            newDir = getSortedEntries(newDir, order)
            newDir = getSortedDir(newDir, dirFirst)

            length = len(newDir)
            if length == 0:
                return
            
            lastDir = list(entry.name for entry in newDir if entry.is_dir())
            if len(lastDir) > 0:
                lastDir = lastDir[-1]

            for index, entry in enumerate(newDir):
                currentPadding = ""
                if displaySize:
                    entrySize = getFormattedEntrySize(entry)

                if displayDate:
                    entryDate = getEntryDate(entry)

                if level > 1:
                    # print(TAB, end="")
                    # print(TAB.join('│' for i in range(level-1)), end="")
                    print(TAB.join(padding), end="")
                
                if index == length-1:
                    print("{}└── {} {} {}".format(TAB, entry.name, entrySize, entryDate))
                else:
                    print("{}├── {} {} {}".format(TAB, entry.name, entrySize, entryDate))

                if entry.is_dir():
                    if lastDir == entry.name:
                        currentPadding = " "
                    else:
                        currentPadding = "│"
                    padding.append(currentPadding)
                    genSubtree(entry.path, level+1, maxDepth, displaySize, displayDate, dirFirst, sortBy, order, padding)
                    padding.pop()

def run():
    args = getCommandLineArguments()
    directory = args.dir
    depth = args.depth
    displaySize = args.display_size
    displayDate = args.display_date
    dirFirst = args.dir_first
    sortBy = args.sort_by[0]
    order = args.sort_order[0]
    generateTree(directory, depth, displaySize, displayDate, dirFirst, sortBy, order)

if __name__ == "__main__":
    run()