from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from bert_inference import preprocess_and_inference
from processing import doPredicts
import pandas as pd
import os


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="static"), name="templates")
# app.mount("/images", StaticFiles(directory="static"), name="images")

# Разрешаем все источники для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Определяем обработчик для корневого URL
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Определяем путь к файлу index.html
    index_path = os.path.join("templates", "index.html")
    # Открываем файл и считываем его содержимое
    with open(index_path, "r") as file:
        content = file.read()
    # Возвращаем содержимое файла как HTML-страницу
    return HTMLResponse(content)

# @app.get("/next/", response_class=HTMLResponse)
# async def next():
#     index_path = os.path.join("templates", "next.html")
#     with open(index_path, "r") as file:
#         content = file.read()

#     return HTMLResponse(content)

@app.post("/upload")
def upload(file: UploadFile):
    contents = file.file.read() # Read the contents of the uploaded file
    data = BytesIO(contents) # Store the contents in a BytesIO object
    df = pd.read_csv(data) # Convert BytesIO object to Pandas DataFrame
    data.close() # Close the BytesIO object
    file.file.close()
    preprocess_and_inference(df)
    return

@app.get("/once-data/")
def onceData():
    data = pd.read_csv("processed_df.csv", index_col=0)
    data["ID урока"] = data["ID урока"].astype(int)
    data = data.drop(columns=["Unnamed: 0", "Дата старта урока", "Текст сообщения", "Дата сообщения", "len_text"])
    predicts_imgs = {}
    print(data)
    img_path = "static/images/img_general_vebinar.jpg"
    preds = doPredicts(data, img_path)
    predicts_imgs["data"] = preds
    predicts_imgs["path"] = img_path 
    return predicts_imgs

@app.get("/numeric-data/")
def numericData():
    data = pd.read_csv("processed_df.csv", index_col=0)
    data['ID урока'] = data['ID урока'].astype(int)
    data = data.drop(columns=["Unnamed: 0", "Дата старта урока", "Текст сообщения", "Дата сообщения", "len_text"])
    grouped_datas = {}
    predicts_imgs = []
    vebin_IDs = data["ID урока"].unique()
    print(vebin_IDs)
    for group_name, group_data in data.groupby("ID урока"):
        img_path = "static/images/img_" + str(group_name) + "_vebinar.jpg"
        preds = doPredicts(group_data, img_path, group_name)
        print(preds)
        print(img_path)
        pr = {}
        pr["data"] = preds
        pr["path"] = img_path
        pr["ID"] = group_name
        
        
        predicts_imgs.append(pr)
    print(predicts_imgs)
    return predicts_imgs

@app.get("/filter/")
def filter(need_class: str, id: int = None):
    data_path = "processed_df.csv" 
    data = pd.read_csv(data_path, index_col=0, encoding='utf-8') 
    print(data)
    if not id:
        filter = data[need_class] == 1
    else:
        filter = (data[need_class] == 1) & (data["ID урока"] == id)
    filltered = data[filter]
    filter_json = filltered.to_dict(orient='records');
    print(filter_json)
    return filter_json