import pytest
import sqlite3
from httpx import AsyncClient, ASGITransport
from server import app  
import os

DATABASE = "dicom_data.db"
API_KEY = os.getenv("API_KEY", "Floy_sirisha")  

@pytest.mark.asyncio
@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://localhost:8000", verify=False) as client:
        yield client

@pytest.mark.asyncio
@pytest.fixture
async def setup_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM received_data")
    conn.commit()
    conn.close()
    yield

@pytest.mark.asyncio
async def test_store_endpoint(async_client, setup_database):
    data = {
        "patient_id": "11",
        "patient_name": "Ritter^Swen",
        "study_instance_uid": "2.25.336686478142883928648119453336617209501",
        "series_instance_uid": "2.25.224448196368772239566748891329233754634",
        "num_instances": 6
    }
    headers = {"access_token": API_KEY}  
    response = await async_client.post("/store", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

   
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM received_data")
    result = cursor.fetchone()
    print(f"DEBUG: {result}") 
    assert result == (
        "2.25.224448196368772239566748891329233754634", 
        "Ritter^Swen",  
        "11",  
        "2.25.336686478142883928648119453336617209501", 
        6  
    )
    conn.close()
