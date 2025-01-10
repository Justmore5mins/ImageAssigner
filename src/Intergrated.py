from os import listdir,mkdir,system
from shutil import move,make_archive
from cv2 import VideoCapture,CAP_PROP_FRAME_COUNT, imwrite

class VideoPreprocess:
    def __init__(self,dir:str):
        self.items = listdir(dir)
        try:
            rmtree(".DS_Store")
        except:
            pass
        try:
            mkdir("spilted")
        except FileExistsError:
            from shutil import rmtree
            rmtree("spilted") if input("Folder spilted exists, reset it?(Y/n)").lower() == "y" else exit(1)
            
    def spilt(self,interval:int = 5):
        for item in self.items:
            video = VideoCapture(item)
            total = CAP_PROP_FRAME_COUNT/(interval if interval != 0 else 1)
            delay = 0;
            for i in range(total-1):
                success, image = video.read()
                if success and delay == interval:
                    imwrite(f"spilted/{item.split('.')[0]}{i}.jpg", image)
                    delay = 0
                    print(f"{i} out of {total} images ({(i/total*100):.2f}%) done", end="\r",flush=True)
                delay += 1
                
    def hash(self):
        from hashlib import md5
        for item in listdir("spilted"):
            move(item, f"{md5(item.encode()).hexdigest()}.{item.split('.')[-1]}")
            
    def assign(self, annotator:int = 5):
        mkdir("assigned")
        for i in range(annotator):
            mkdir(f"assigned/{i}")
        
        i = 0
        while i < len(listdir("spilted")):
            move(f"spilted/{listdir("spilted")[i]}",f"assigned/{i%annotator}/{listdir("spilted")[i]}")
            i += 1
        
        for i in list("assigned"):
            make_archive(f"assigned/{i}","zip",f"{i}",verbose=True)
            system(f"rm assigned/{i}")
            move(f"assigned/{i}.zip","..")
            
if __name__ == "main":
    assign = VideoPreprocess("videosrc")
    assign.spilt()
    assign.hash()
    assign.assign()