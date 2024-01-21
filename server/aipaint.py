# make sure you're logged in with `huggingface-cli login`
import random
import os as os
from PIL import Image
from io import BytesIO
import time
import oss2
from flask import Flask, request, jsonify
import request_img
import torch
from pyxxl import ExecutorConfig, PyxxlRunner
from pyxxl.ctx import g
import json
from flask import Flask

app = Flask(__name__)

program_start_time = time.time()

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"


def check_gpu_usage():
    if torch.cuda.is_available():
        gpu_total_mem = torch.cuda.get_device_properties(0).total_memory
        gpu_mem_usage = torch.cuda.memory_allocated() / gpu_total_mem
    else:
        print("GPU 无法使用")
        return None
    return gpu_mem_usage


def getRandom(randomlength=10):
    """
  生成一个指定长度的随机字符串
  """
    digits = "0123456789"
    ascii_letters = "abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    str_list = [random.choice(digits + ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def upload(image):
    auth = oss2.Auth('LTAI4G4G9xBm6esdVkSpjPEz', 'WDENaJox7D0WPhoxSNrjJmMgUg6ywp')
    bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', 'paint4art')
    name = 'aiimages/' + getRandom() + '.jpg'
    bucket.put_object(name, image)
    return "https://paint4art.oss-cn-beijing.aliyuncs.com/" + name


def compress_image(img_bytes, max_size):
    """Compresses the input image data to the specified max file size in kilobytes."""
    # Open the image from the input bytes
    img = Image.open(BytesIO(img_bytes)).convert('RGB')
    with BytesIO() as f:
        # Compress the image while its size is larger than the max size
        while True:
            # Convert image to JPEG format with high quality
            img.save(f, format='JPEG', quality=90)
            # Break the loop if the compressed image is within the size limit
            if f.tell() <= max_size * 1000:
                break
            # Reduce the quality by 10% each time
            img = img.quantize(colors=256, method=2)
        # Return the compressed image data
        f.seek(0)
        return f.read()


@app.route("/aigic", methods=['POST'])
def aigic():
    print("coming")
    # time0 = time.time()
    get_Data = json.loads(request.get_data())
    prompt = get_Data.get('desc')
    # time1 = time.time()
    # print("get desc:", time1 - time0)
    time0 = time.time()
    # check gpu memory
    gpu_usage = check_gpu_usage()
    if gpu_usage is None:
        print('GPU 不可用')
        return_dict = {"code": '500', "message": "GPU 不可用", "content": None }
        return json.dumps(return_dict)

    while True:
        usage = check_gpu_usage()
        print("usage", usage)
        if usage < 0.55:
            print("gen pic")
            image = request_img.request_img().request_from_webui(prompt=prompt)
            time1 = time.time()
            print("general_model:", time1 - time0)
            time0 = time.time()
            compressed_data = compress_image(image, max_size=1000)
            url = upload(compressed_data)
            time1 = time.time()
            print("upload:", time1 - time0)
            break
        else:
            print("GPU memory usage is {usage:.2f}%. Waiting...")
            time.sleep(5)  # 每隔 5 秒重新检查一次
    return_dict = {"code": '200', "message": None, "content": url}
    return json.dumps(return_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)