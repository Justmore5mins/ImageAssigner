from os import listdir,mkdir,system
from sys import argv
from hashlib import md5
from shutil import copyfile

#hash the filenames
for dir in argv[1:]:
    for file in listdir(dir):
        copyfile(f"{dir}/{file}", f"spilted/{md5(file.encode()).hexdigest()}.{file.split('.')[-1]}")
        system(f"rm {dir}/{file}")
