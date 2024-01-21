from io import BytesIO
from PIL import Image
import requests
import json
import base64
import random
class request_img:
    def submit_post(self, url: str, data: dict):
        return requests.post(url, data=json.dumps(data))

    def save_encoded_image(self, b64_image: str, output_path: str):
        with open(output_path, "wb") as image_file:
            image_file.write(base64.b64decode(b64_image))

    def request_from_webui(self, prompt: str):
        txt2img_url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'
        data = {
            'prompt': '<lora:irene_V70:1>,' + prompt,
            'negative_prompt': '(((multi heads))),(((more than 1 heads))),(((exposed nipples))), (((nipples))), (worst quality, low quality:1.4),ugly eyes,ugly face,(((simple background))),monochrome ,lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, lowres, bad anatomy, bad hands, text, error, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, ugly,pregnant,vore,duplicate,morbid,mut ilated,tran nsexual, hermaphrodite,long neck,mutated hands,poorly drawn hands,poorly drawn face,mutation,deformed,blurry,bad anatomy,bad proportions,malformed limbs,extra limbs,cloned face,disfigured,gross proportions, (((missing arms))),(((missing legs))), (((extra arms))),(((extra legs))), plump,bad legs,error legs,username,blurry,bad feet, blur,',
            "cfg_scale": 7,
            #"width": random.randrange(64, 80, 8) * 8,
            #"height": random.randrange(64, 100, 8) * 8,
            "width": 512,
            "height": 512,
            "sampler_name": "Euler a",
            "steps": 20,
            'seed': -1,
            "enable_hr": True,  
            "hr_second_pass_steps": 10,
            "hr_scale": 2,
            "hr_upscaler": "ESRGAN_4x",
            "denoising_strength": 0.5,
            # "restore_faces": True,
        }
        response = self.submit_post(txt2img_url, data)
        print(response)
        self.save_encoded_image(response.json()['images'][0], 'dog.png')
        with Image.open('dog.png') as img:
            buf = BytesIO()
            img.save(buf, format='PNG')
            image_data = buf.getvalue()

        return image_data
