import os, shutil, pathlib

shutil.copy("file.txt", "backup/")

with open("file.txt") as f:
    file = f.read()
print(file)

with open("file.txt", "a") as f:
    file = f.write("\n new content of the file")
with open("file.txt") as f:
    file = f.read()
print(file)

os.remove("file.txt")

shutil.copy("backup/file.txt", "file.txt")

os.remove("backup/file.txt")
