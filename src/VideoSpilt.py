from cv2 import VideoCapture, imwrite,CAP_PROP_FRAME_COUNT
from sys import argv
from time import perf_counter
from os import listdir

interval = int(argv[1])
i = 0

try:
    from os import mkdir
    mkdir("spilted")
except FileExistsError:
    from os import system
    print("Folder already exists")
    system("rm -r spilted; mkdir spilted")
    
allcount = 0
for video in listdir(argv[2]):
    video = f"{argv[2]}/{video}"
    system(f"mv {video} {video.spilt(".")[0]}.mp4") if 'MOV' in video.upper() else None
    allcount += int(VideoCapture(video).get(CAP_PROP_FRAME_COUNT)/interval) if interval != 0 else int(VideoCapture(video).get(CAP_PROP_FRAME_COUNT))

start = perf_counter()
for video in listdir(argv[2]):
    cap = VideoCapture(f"{argv[2]}/{video}")
    framecount = cap.get(CAP_PROP_FRAME_COUNT)
    framecount = int(framecount /interval) if interval != 0 else framecount
    success,image = cap.read()
    if interval != 0:
        delay = 0
        round_time = 0
        while success:
            success,image = cap.read()
            if delay == interval and success:
                imwrite(f"spilted/{video.split('.')[0]}{i}.jpg", image)
                time = perf_counter() - start
                print(f"{i} out of {allcount} images ({(i/allcount*100):.2f}%) done", end="\r",flush=True)
                delay = 0
                i += 1
                round_time = perf_counter()
            delay += 1
    
    else:
        round_time = 0
        while success:
            success,image = cap.read()
            imwrite(f"spilted/{video.split(".")[0]}{i}.jpg", image) if success else exit(1)
            time = perf_counter() - start
            print(f"{i} out of {allcount} images ({(i/allcount):.2f}%) done, est {(time):.2f} secs ,eta {(time)*allcount/(1 if i == 0 else i):.2f} secs, {1/(perf_counter() - round_time):.2f} fps", end="\r",flush=True)
            round_time = perf_counter()
            i += 1
            
    def warning(round:int):
        raise RuntimeError(f"save image failed at {round} image")