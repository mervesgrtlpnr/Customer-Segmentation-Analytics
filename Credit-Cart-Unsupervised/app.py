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

with open("customer_segmentation_model.pkl", "rb") as f:
    model_data = pickle.load(f)

scaler = model_data['ss']
pca = model_data['pca2']
kmeans_final = model_data['kmeans']


SEGMENT_ISIMLERI = {
    7: 'VIP / Premium Müşteri',
    4: 'Riskli / Nakit Avansçı',
    10: 'Taksitli Alışverişçi',
    13: 'Pasif / Uyuyan Müşteri'
}


class CustomerData(BaseModel):
    BALANCE: float
    PURCHASES: float
    ONEOFF_PURCHASES: float
    INSTALLMENTS_PURCHASES: float
    CASH_ADVANCE: float
    CREDIT_LIMIT: float
    BALANCE_FREQUENCY: float = 0.87
    PURCHASES_FREQUENCY: float = 0.49
    ONEOFFPURCHASESFREQUENCY: float = 0.20
    PURCHASESINSTALLMENTSFREQUENCY: float = 0.36
    CASHADVANCEFREQUENCY: float = 0.13
    CASHADVANCETRX: float = 3.0
    PURCHASES_TRX: float = 14.0
    PAYMENTS: float = 1733.0
    MINIMUM_PAYMENTS: float = 864.0
    PRCFULLPAYMENT: float = 0.15
    TENURE: float = 12.0


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict_segment(data: CustomerData):
    input_dict = data.dict()
    columns = [
        'BALANCE', 'BALANCE_FREQUENCY', 'PURCHASES', 'ONEOFF_PURCHASES',
        'INSTALLMENTS_PURCHASES', 'CASH_ADVANCE', 'PURCHASES_FREQUENCY',
        'ONEOFFPURCHASESFREQUENCY', 'PURCHASESINSTALLMENTSFREQUENCY',
        'CASHADVANCEFREQUENCY', 'CASHADVANCETRX', 'PURCHASES_TRX',
        'CREDIT_LIMIT', 'PAYMENTS', 'MINIMUM_PAYMENTS', 'PRCFULLPAYMENT', 'TENURE'
    ]

    input_df = pd.DataFrame([input_dict], columns=columns)

    scaled_data = scaler.transform(input_df)
    pca_data = pca.transform(scaled_data)
    cluster_id = kmeans_final.predict(pca_data)[0]

    profil_ismi = SEGMENT_ISIMLERI.get(cluster_id, "Standart Müşteri")

    return {
        "cluster_id": int(cluster_id),
        "profile": profil_ismi
    }
