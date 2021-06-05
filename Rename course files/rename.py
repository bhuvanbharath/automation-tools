import pandas as pd
import os

cwd = os.getcwd()
print('Current working directory: '+cwd)

#---walking thru the current working directory---#

#---root = cwd, dir = sub dirs in cwd, files = files in cwd---#
for root,dirs,files in os.walk(cwd):
    for file in files:
       if file.endswith('.csv'):
           #---extract data
           filenames_df = pd.read_csv(file, header = None)
           
#print (filenames_df)
FileNames = filenames_df[0]    
    
#---get the name of the files after sorting by the date modified---#
Files = os.listdir(cwd)
full_list = [os.path.join(cwd,i) for i in Files]    #this method is called List comprehension
time_sorted_list = sorted(full_list, key=os.path.getmtime)

#---remove the path from elements and extract only name of the files in the cwd---
sorted_filename_list = [ os.path.basename(i) for i in time_sorted_list]

i = 0 #list index
topicNo = 1 #topicNos
FileNo = 0 #renaming index

for file in sorted_filename_list:

    #---check for filenames with no extension---#
    SplitExt = os.path.splitext(file)
    if SplitExt[1] == '':
        
        source = cwd + '\\' + file

        #---check for the topic files and create txt files---#
        TopicCheck = str(topicNo) + '. '
        if FileNames[i].find(TopicCheck) != -1:
            #print (FileNames[i])
            FileNames[i].replace(TopicCheck,'')
            
            #---create the txt file---#
            f = open('0' + str(FileNo) +'. ' + FileNames[i]+'.txt','w')
            f.close
            
            topicNo = topicNo + 1
            i=i+1
            
        destination = cwd + '\\' + str(FileNo) + '.' + FileNames[i] + '.mp4'
        os.rename(source,destination) #rename it finally!
        
        FileNo = FileNo+1
        i=i+1

