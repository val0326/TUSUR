Веб-приложение должно склеить две картинки в одну по вертикали или
горизонтали в зависимости от желания пользователя, выдавать графики распре-
деления цветов исходных картинок и новой картинки.

@app.post("/vector_image")
def image_endpoint(*, vector):
    # Returns a cv2 image array from the document vector
    cv2img = my_function(vector)
    res, im_png = cv2.imencode(".png", cv2img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")