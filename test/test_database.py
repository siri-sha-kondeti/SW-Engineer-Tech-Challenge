import sqlite3
import pytest

DATABASE = "dicom_data.db"

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(":memory:")  
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE received_data (
        PatientID TEXT,
        PatientName TEXT,
        StudyInstanceUID TEXT,
        SeriesInstanceUID TEXT,
        InstancesInSeries INTEGER
    )
    """)
    conn.commit()
    yield conn
    conn.close()

def test_insert_data(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
    INSERT INTO received_data (PatientID, PatientName, StudyInstanceUID, SeriesInstanceUID, InstancesInSeries)
    VALUES (?, ?, ?, ?, ?)
    """, ("11", "Ritter^Swen", "2.25.336686478142883928648119453336617209501", "2.25.224448196368772239566748891329233754634", 6))
    db_connection.commit()

    cursor.execute("SELECT * FROM received_data")
    data = cursor.fetchone()
    assert data == ("11", "Ritter^Swen", "2.25.336686478142883928648119453336617209501", "2.25.224448196368772239566748891329233754634", 6)
