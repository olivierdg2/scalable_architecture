import queue
from threading import Thread
import requests

from ast import literal_eval as make_tuple

from PIL import Image, ImageDraw
import json
import timeit 

def multi_process(addresses, no_workers, PIDS={}):
    image = Image.new('RGB', (680, 440), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    class Worker(Thread):
        def __init__(self, request_queue):
            Thread.__init__(self)
            self.queue = request_queue

        def run(self):
            while True:
                content = self.queue.get()
                if content == "":
                    break
                resp = requests.get(content)
                data = json.loads(resp.content)
                draw.point([int(data["x"]), int(data["y"])], make_tuple(data["value"]))
                pid = data["Pid"]
                if pid in PIDS.keys():
                    PIDS[pid] += 1
                else:
                    PIDS[pid] = 1
                self.queue.task_done()

    # Create queue and add addresses
    q = queue.Queue()
    for url in addresses:
        q.put(url)

    # Create workers and add tot the queue
    workers = []
    for _ in range(no_workers):
        worker = Worker(q)
        worker.start()
        workers.append(worker)

    # Workers keep working till they receive an empty string
    for _ in workers:
        q.put("")
    
    # Join workers to wait till they finished
    for worker in workers:
        worker.join()

    return image, PIDS


if __name__ == "__main__":
    start = timeit.default_timer()
    urls = []
    for y in range(440):
        for x in range(680):
            
            urls.append(f"http://192.168.1.7:6969/?x={x}&y={y}")


    image, pids = multi_process(urls, 32)
    stop = timeit.default_timer()
    print('ça a pris: ', stop-start, "s")
    image.show("Our beautiful mandelbrot")
    
    total_requests = 440 * 680
    for key, value in pids.items():
    	print(f"Server id: {key} => {int((value/total_requests)*100)}%")
    
    
