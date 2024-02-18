import hashlib
import io
from os.path import realpath
from typing import List

import cv2 as cv
import fastapi.responses
import numpy
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw


def get_concat_h(im1, im2):
    dst = Image.new("RGB", (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def get_concat_v(im1, im2):
    dst = Image.new("RGB", (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def make_histogram(im, filename):
    img = cv.imread(im)
    plt.figure()
    color = ("r", "g", "b")
    for i, col in enumerate(color):
        histr = cv.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
        plt.savefig(f"./static/{filename}.jpg")


app = FastAPI()


def sum_two_args(x, y):
    return x + y


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.mount(
    "/static",
    StaticFiles(directory=realpath(f"{realpath(__file__)}/../static")),
    name="static",
)
templates = Jinja2Templates(directory="templates")


@app.get("/some_url/{something}", response_class=HTMLResponse)
async def read_something(request: Request, something: str):
    return templates.TemplateResponse(
        "some.html", {"request": request, "something": something}
    )


def create_some_image(some_difs):
    imx = 200
    imy = 200
    image = numpy.zeros((imx, imy, 3), dtype=numpy.int8)
    image[0 : imy // 2, 0 : imx // 2, 0] = some_difs  # noqa
    image[imy // 2 :, imx // 2 :, 2] = 240  # noqa
    image[imy // 2 :, 0 : imx // 2, 1] = 240  # noqa
    return image


@app.get("/bimage", response_class=fastapi.responses.StreamingResponse)
async def b_image(request: Request):
    # рисуем изображение, сюда можете вставить GAN, WGAN сети и т. д.
    # взять изображение из массива в Image PIL
    image = create_some_image(100)
    im = Image.fromarray(image, mode="RGB")
    # сохраняем изображение в буфере оперативной памяти
    imgio = io.BytesIO()
    im.save(imgio, "JPEG")
    imgio.seek(0)
    # Возвращаем изображение в виде mime типа image/jpeg
    return fastapi.responses.StreamingResponse(
        content=imgio, media_type="image/jpeg"
    )


@app.get("/image", response_class=HTMLResponse)
async def make_image(request: Request):
    image_n = "image.jpg"
    image_dyn = request.base_url.path + "bimage"
    image_st = request.url_for("static", path=f"/{image_n}")
    image = create_some_image(250)
    im = Image.fromarray(image, mode="RGB")
    im.save(f"./static/{image_n}")
    # передаем в шаблон две переменные, к которым сохранили url
    return templates.TemplateResponse(
        "image.html",
        {"request": request, "im_st": image_st, "im_dyn": image_dyn},
    )


@app.post("/image_form", response_class=HTMLResponse)
async def make_image_form(
    request: Request,
    name_op: str = Form(),
    number_op: int = Form(),
    r: int = Form(),
    g: int = Form(),
    b: int = Form(),
    files: List[UploadFile] = File(description="Multiple files as UploadFile"),
):
    # устанавливаем готовность прорисовки файлов, можно здесь про-
    # верить, что файлы вообще есть
    # лучше использовать исключения
    ready = False
    print(len(files))
    if len(files) > 0:
        if len(files[0].filename) > 0:
            ready = True
    images = []
    if ready:
        print([file.filename.encode("utf-8") for file in files])
        # преобразуем имена файлов в хеш -строку
        images = [
            "static/"
            + hashlib.sha256(file.filename.encode("utf-8")).hexdigest()
            + ".jpg"
            for file in files
        ]
        # берем содержимое файлов
        content = [await file.read() for file in files]
        # создаем объекты Image типа RGB размером 200 на 200
        p_images = [
            Image.open(io.BytesIO(con)).convert("RGB").resize((200, 200))
            for con in content
        ]
        # сохраняем изображения в папке static
        for i in range(len(p_images)):
            draw = ImageDraw.Draw(p_images[i])
            # Рисуем красный эллипс с черной окантовкой
            draw.ellipse(
                (100, 100, 150, 200 + number_op),
                fill=(r, g, b),
                outline=(0, 0, 0),
            )
            p_images[i].save("./" + images[i], "JPEG")
    # возвращаем html с параметрами-ссылками на изображения, кото-
    # рые позже будут
    # извлечены браузером запросами get по указанным ссылкам в img
    # src
    return templates.TemplateResponse(
        "forms.html", {"request": request, "ready": ready, "images": images}
    )


@app.get("/image_form", response_class=HTMLResponse)
def make_image_get(request: Request):
    return templates.TemplateResponse("forms.html", {"request": request})


@app.get("/transform", response_class=HTMLResponse)
def transform_images_get(request: Request):
    return templates.TemplateResponse("transform.html", {"request": request})


@app.post("/transform", response_class=HTMLResponse)
async def transform_images(
    request: Request,
    directions: str = Form(),
    files: List[UploadFile] = File(description="Multiple files as UploadFile"),
):
    # устанавливаем готовность прорисовки файлов, можно здесь про-
    # верить, что файлы вообще есть
    # лучше использовать исключения
    ready = False
    if len(files) > 1:
        if len(files[0].filename) > 0:
            ready = True
    images = []
    if ready:
        for file in files:
            digest_filename = hashlib.sha256(
                file.filename.encode("utf-8")
            ).hexdigest()
            images.append(f"static/{digest_filename}.jpg")

        # берем содержимое файлов
        content = [await file.read() for file in files]
        # создаем объекты Image типа RGB размером 200 на 200
        p_images = [
            Image.open(io.BytesIO(con)).convert("RGB").resize((200, 200))
            for con in content
        ]
        # сохраняем изображения в папке static
        for p_image, image_path in zip(p_images, images):
            p_image.save("./" + image_path, "JPEG")
    # возвращаем html с параметрами-ссылками на изображения, кото-
    # рые позже будут
    # извлечены браузером запросами get по указанным ссылкам в img
    # src
    if directions == "vertical":
        image_result = get_concat_v(p_images[0], p_images[1])

    else:
        image_result = get_concat_h(p_images[0], p_images[1])
    image_result.save("./static/result.jpg", "JPEG")

    make_histogram("./static/result.jpg", "image_result_hist")
    make_histogram(images[0], "hist1")
    make_histogram(images[1], "hist2")

    return templates.TemplateResponse(
        "transform.html",
        {
            "request": request,
            "ready": ready,
            "image1": images[0],
            "image2": images[1],
            "image_result": "./static/result.jpg",
            "image1_gist": "./static/hist1.jpg",
            "image2_gist": "./static/hist2.jpg",
            "image_result_gist": "./static/image_result_hist.jpg",
        },
    )
