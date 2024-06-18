import sqlite3
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
import uvicorn
from contextlib import asynccontextmanager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = "dicom_data.db"
API_KEY = "Floy_sirisha"
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS received_data (
        PatientID TEXT,
        PatientName TEXT,
        StudyInstanceUID TEXT,
        SeriesInstanceUID TEXT,
        InstancesInSeries INTEGER
    )
    """)
    conn.commit()
    conn.close()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/store")
async def store_data(request: Request, api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    
    data = await request.json()
    patient_id = data.get("patient_id")
    patient_name = data.get("patient_name")
    study_instance_uid = data.get("study_instance_uid")
    series_instance_uid = data.get("series_instance_uid")
    num_instances = data.get("num_instances")

    if not all([patient_id, patient_name, study_instance_uid, series_instance_uid, num_instances]):
        raise HTTPException(status_code=400, detail="Missing data fields")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO received_data (PatientID, PatientName, StudyInstanceUID, SeriesInstanceUID, InstancesInSeries)
        VALUES (?, ?, ?, ?, ?)
        """, (patient_id, patient_name, study_instance_uid, series_instance_uid, num_instances))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="server.key", ssl_certfile="server.crt")
