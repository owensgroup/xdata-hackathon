# Read in the file
filedata = None
with open('output.txt', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('(', '')
filedata = filedata.replace(')', '<br>')
filedata = filedata.replace(', ', ' - ')
filedata = filedata.replace("u'\u", "&#x")
filedata = filedata.replace("\u", "&#x")
filedata = filedata.replace("'", "")


# Write the file out again
with open('output.html', 'w') as file:
  file.write(filedata)

