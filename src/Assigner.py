from os import listdir,mkdir,chdir
from sys import argv
from shutil import move
from shutil import make_archive, rmtree

annotator:int = int(argv[1])

try:
    mkdir("assigned")
except:
    pass

for i in range(annotator):
    try:
        mkdir(f"assigned/{i}")
    except FileExistsError:
        pass
for image in listdir("spilted"):
    i = 0 if i == annotator else i
    move(f"spilted/{image}", f"assigned/{i}")
    i+=1
    
chdir("assigned")
for i in range(annotator):
    make_archive(f"{i}","zip",f"{i}",verbose=True)
    rmtree(f"{i}")
    move(f"{i}.zip","..")