from os import listdir,mkdir,system
from sys import argv
from shutil import move
from shutil import rmtree

directory = argv[1]
images:list[str] = []
annotation:list[str] = []
info:list[str] 

for item in listdir(f"{directory}/images"):
    images.append(item)
for item in listdir(f"{directory}/labels"):
    annotation.append(item)
    
with open(f"{directory}/info.txt") as file:
    #dataset name
    info = file.readlines()
    name=info[0].replace("\n","")
    cls = info[2].split(" ")
#if len(images) % 10 != 0:
    #raise Warning("recommend images count = 10n")

print("creating dirs")
try:
    mkdir(f"{name}")
except FileExistsError:
    system(f"rm -r {name}")
mkdir(f"{name}/train")
mkdir(f"{name}/valid")
mkdir(f"{name}/test")
mkdir(f"{name}/train/images")
mkdir(f"{name}/train/labels")
mkdir(f"{name}/valid/images")
mkdir(f"{name}/valid/labels")
mkdir(f"{name}/test/images")
mkdir(f"{name}/test/labels")

print("now generating dataset")  
i = 0
while i < len(images):
    for a in range(i, i+7):
        move(f"{directory}/images/{images[a]}",f"{name}/train/images")
        move(f"{directory}/labels/{annotation[a]}",f"{name}/train/labels")
        i+=1
    for a in range(i,i+2):
        move(f"{directory}/images/{images[a]}",f"{name}/valid/images")
        move(f"{directory}/labels/{annotation[a]}",f"{name}/valid/labels")
        i += 1
    
    move(f"{directory}/images/{images[a]}",f"{name}/test/images")
    move(f"{directory}/labels/{annotation[a]}",f"{name}/test/labels")
    i += 1
    
print("Now generating yaml file")

text=["train: ../train/images\n",
      "valid: ../valid/images\n",
      "test: ../test/images\n",
      "",
      f"nc: {info[1]}",
      f"names: {cls}"
    ]
with open(f"{name}/data.yaml","w") as file:
    file.writelines(text)