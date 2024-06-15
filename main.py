import os.path
import numpy as np
from fastapi import FastAPI
import uvicorn
import fastapi.responses
import io
from fastapi import Form,File,UploadFile
from typing import List
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import hashlib
from PIL import Image, ImageDraw, ImageEnhance, ImageGrab, ImageOps
import matplotlib.pyplot as plt
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
# возвращаем основной обработанный шаблон index.html
@app.get("/")
def read_root(request: Request):
 return templates.TemplateResponse("index.html", {"request": request})
@app.post("/")
async def check(request: Request ):
    return templates.TemplateResponse("forms.html",{"request": request,"ready": False, "images": []})

@app.post("/image_form", response_class=HTMLResponse)
async def make_image(request: Request, number_op: float = Form(),files: List[UploadFile] = File(description="Multiple files as UploadFile")):
#посылаем post запрос на сайт Google для проверки прохождения Captcha
    ready = False
    print(len(files))
    if (len(files) > 0):
        if (len(files[0].filename) > 0):
            ready = True
            images = []
            if ready:
                    print([file.filename.encode('utf-8') for file in files])
#преобразуем имена файлов в хеш -строку
                    images = ["static/" + hashlib.sha256(file.filename.encode('utf-8')).hexdigest()for file in files]
   # берем содержимое файлов
                    content = [await file.read() for file in files]
   # создаем объекты Image типа RGB размером 200 на 200
                    p_images = [Image.open(io.BytesIO(con)).convert("RGB").resize((200, 200))for con in content]
                    for i in range(len(p_images)):

   # задание
                        enhancer = ImageEnhance.Contrast(p_images[i])
                        img_array_after = np.asarray(p_images[i])
                        colors, counts = np.unique(img_array_after.reshape(-1, 3), axis=0, return_counts=True)
                        plt.figure(figsize=(10, 5))
                        plt.bar(range(len(colors)), counts, color=colors / 255)
                        plt.xlabel('Цвет')
                        plt.ylabel('Количество пикселей')
                        plt.title('Распределение цветов на изображении')
                        image_before = plt.savefig("static/before.png")
                        #plt.clf()

                        p_images[i] = enhancer.enhance(number_op)
                        enhancer.enhance(number_op)
                        p_images[i].save("./" + images[i], 'JPEG')
                        img_array_after = np.asarray(p_images[i])
                        colors, counts = np.unique(img_array_after.reshape(-1, 3), axis=0, return_counts=True)
                        plt.figure(figsize=(10, 5))
                        plt.bar(range(len(colors)), counts, color=colors / 255)
                        plt.xlabel('Цвет')
                        plt.ylabel('Количество пикселей')
                        plt.title('Распределение цветов на изображении')
                        image_after = plt.savefig("static/After.png")
                        #plt.clf()
    return templates.TemplateResponse("forms.html", {"request": request,"ready": ready, "images": images})


@app.get("/image_form", response_class=HTMLResponse)
async def make_image(request: Request):
   return templates.TemplateResponse("forms.html", {"request": request})



if __name__=="__main__":
    uvicorn.run(app,host="localhost", port=8000)
