"""
Developed by Wyatt Rose

converts html files from directory 'directory' to pdfs in 'destination'
names the pdf the title of the html
"""
# pip install pdfkit, download and install wkhtmltopdf, add C:\Program Files\wkhtmltopdf\bin (or the direct path) to path variables
import pdfkit
import os
import re
import sys
from pathlib import Path

# GLOBAL VARS:
# directory of html files, double backslashes are treated as single backslash in path
directory = "C:\\Users\\wjros\\OneDrive\\Documents\\Catholic\\NewAdvent\\summa"
# previous files in destination directory will be DELETED!
# destination must be manually created
# a folder named 'A_MISC' must be manually created in the destination directory
destination = "C:\\Users\\wjros\\OneDrive\\Documents\\Catholic\\NewAdvent\\PDFs\\summaPDFs_1"


def main():
    
    # if directory doesnt exist, create directory
    if not os.path.isdir(f"{destination}"):
        os.mkdir(f"{destination}")
    
    # Delete the contents of destination directory
    #for file in os.scandir(destination):
    #    os.remove(file.path)
    
    # for every file in directory
    for filename in os.listdir(f"{directory}"):
        # print source path
        print(f"fileName: {directory}\{filename}")
        # open file in directory
        with open(f"{directory}\{filename}", encoding="utf8") as file:
            title = ""
            
            try:
                # search for tile in html
                for line in file:
                    # regex to find title from line
                    regex = re.search("title>(.+)<", str(line))
                    
                    # if regex found, save to title
                    if regex != None:
                        # pull title from regex object
                        title = regex.group()
                        
                        # strip extra html characters from regex object
                        titleArray = re.split('>|<', title)
                        title = titleArray[1]
                        
                        # print title to verify
                        print(f"Title: {title}")

                # format the source of the html
                src = directory + "\\" + filename
                src = Path(src)
                
                # make sure no whitespace surrounds title, no invalid path characters
                title = title.strip()
                # remove all invalid characters from title
                title = re.sub('[:?<>|*"/]', '-', title)
                
                # remove 'CHURCH FATHERS:' from title
                if re.search("SUMMA THEOLOGICA-", title):
                    title = re.split('THEOLOGICA-', title)
                    title = title[1]
                    title = title.strip()
                
                
                # find name in title, add to destination
                subDirName = re.split('[()]', title)
                # if name exists, add directory
                if len(subDirName) > 2:
                    title = subDirName[0]
                    title = title.strip()
                    
                    book = re.split('[,]', subDirName[1])
                    question = book[1]
                    question = question.strip()
                    
                    book = book[0]
                    book = book.strip()
                    # remove . from st name
                    question = re.sub('[.]', '', question)
                    # format question number with 3 digits
                    
                    questionArray = re.split(' ', question)
                    questionArray[1] = f'{int(questionArray[1]):03d}'
                    question = questionArray[0] + " " + questionArray[1]
                    print(f"Question: {question}")
                    
                    # if directory doesnt exist, create directory
                    if not os.path.isdir(f"{destination}\\{book}"):
                        os.mkdir(f"{destination}\\{book}")
                        
                    dst = destination + "\\" + book + "\\" + question + " " + title + ".pdf"
                else:
                    dst = destination + "\\" + title + ".pdf"
                    
                
                dst = Path(dst)
                print(f"Destination: {dst}")

                # windows won't open file unless its closed
                file.close()
                
                # if file ends in .htm, 
                if re.search("\.htm$", str(src)):
                    # convert html to pdf using verbose and local file access enabled
                    pdfkit.from_file(str(src), str(dst), verbose=True, options={"enable-local-file-access": True})
                else:
                    print("Not HTML!")
        
            except:
                print("SKIP")


main()
