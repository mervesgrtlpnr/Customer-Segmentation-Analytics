from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

with open("rfm_segmentasyon_modeli.pkl", "rb") as f:
    model_data = pickle.load(f)

scaler = model_data['scaler']
kmeans = model_data['kmeans']
segment_isimleri = model_data['segment_isimleri']

segment_isimleri = {
    1: 'VIP',
    2: 'Uyuyan',
    0: 'Seyrek',
    3: 'Riskli Müşteriler'
}


class RFMData(BaseModel):
    Recency: int
    Frequency: int
    Monetary: float


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict_segment(data: RFMData):
    input_df = pd.DataFrame([data.model_dump()])

    input_log = np.log1p(input_df)

    input_scaled = scaler.transform(input_log)

    cluster_id = kmeans.predict(input_scaled)[0]

    profil_ismi = segment_isimleri.get(cluster_id, "Standart Müşteri")

    return {
        "cluster_id": int(cluster_id),
        "profile": profil_ismi
    }