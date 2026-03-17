import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from config import config

logger = config.logger

app = FastAPI(title="Research center classifier")

bundle = joblib.load(config.model_bundle)

center_classifier = bundle["model"]
scaler = bundle["scaler"]
cluster_labels = bundle["labels"]
logger.info("Sucessfully loaded research center classifier pipeline")


class ResearchCenterMetrics(BaseModel):
    internalFacilitiesCount: int
    hospitals_10km: int
    pharmacies_10km: int
    facilityDiversity_10km: float
    facilityDensity_10km: float


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "200"}


@app.post("/predict")
def predict(payload: ResearchCenterMetrics) -> dict[str, str]:
    df = pd.DataFrame([payload.model_dump()])
    scaled_df = scaler.transform(df)
    cluster = int(center_classifier.predict(scaled_df)[0])
    label = cluster_labels.get(cluster, "Unknown")
    return {"predictedCategory": label}
