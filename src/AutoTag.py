from ultralytics import YOLO
from cv2 import VideoCapture,imwrite
from hashlib import md5
from time import process_time

class AutoAnnotation:
    def __init__(self,model:str,video:str,device:str|int|list[int] = "cpu"):
        self.video = VideoCapture(video)
        self.model = YOLO(model=model)
        if device != "cpu":
            self.model.to(device)
        self.cls = model.names
    
    def detect(self,conf=0.8,cls:list = None):
        if cls is None:
            cls = self.cls
        
        state = True
        print("model loaded, now started processing")
        while state:
            state, frame = self.video.read()
            filename = md5(str(process_time).encode()).hexdigest()
            imwrite(f"{filename}.jpg",frame)
            nones = []
            results = self.model.predict(frame,stream=True,conf=conf,classes=cls)
            items:list[str] = []
            if not results:
                nones.append(filename)
            for res in results:
                for box in res.boxes:
                    x,y,w,h = box.xywh
                    detect_cls = box.cls
                    items.append(f"{detect_cls} {x} {y} {w} {h}")
                    print(f"detected {self.cls[detect_cls]} with {box.conf}% confidence at {x},{y},{w},{h} (x,y,w,h)")
                with open(filename,"w") as file:
                    file.writelines(items)
        print("done!")

if __name__ == "__main__":
    AutoAnnotation("Note2025Alpha3a_ncnn_model","../videosrc/IMG_0554.mp4")