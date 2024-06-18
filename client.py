import asyncio
import time
from pydicom import Dataset
from scp import ModalityStoreSCP
import aiohttp
import logging
from aiohttp import ClientSession

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SeriesCollector:
    def __init__(self, first_dataset: Dataset) -> None:
        self.series_instance_uid = first_dataset.SeriesInstanceUID
        self.series: list[Dataset] = [first_dataset]
        self.last_update_time = time.time()
        self.dispatch_started = False

    def add_instance(self, dataset: Dataset) -> bool:
        if self.series_instance_uid == dataset.SeriesInstanceUID:
            self.series.append(dataset)
            self.last_update_time = time.time()
            return True
        return False

class SeriesDispatcher:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.modality_scp = ModalityStoreSCP(self)
        self.series_collector = None

    def add_dataset(self, dataset: Dataset):
        if self.series_collector is None:
            self.series_collector = SeriesCollector(dataset)
        else:
            self.series_collector.add_instance(dataset)
        logger.debug(f"Added dataset with SOP Instance UID: {dataset.SOPInstanceUID} to series")

    async def main(self) -> None:
        while True:
            await asyncio.sleep(0.2)
            await self.run_series_collectors()

    async def run_series_collectors(self) -> None:
        if self.series_collector:
            if time.time() - self.series_collector.last_update_time > 1:
                await self.dispatch_series_collector()

    async def dispatch_series_collector(self) -> None:
        if self.series_collector:
            try:
                
                patient_id = self.series_collector.series[0].PatientID
                patient_name = str(self.series_collector.series[0].PatientName)  
                study_instance_uid = self.series_collector.series[0].StudyInstanceUID
                series_instance_uid = self.series_collector.series_instance_uid
                num_instances = len(self.series_collector.series)

                
                logger.debug(f"Patient ID: {patient_id}")
                logger.debug(f"Patient Name: {patient_name}")
                logger.debug(f"Study Instance UID: {study_instance_uid}")
                logger.debug(f"Series Instance UID: {series_instance_uid}")
                logger.debug(f"Number of Instances: {num_instances}")

                
                data = {
                    "patient_id": patient_id,
                    "patient_name": patient_name,
                    "study_instance_uid": study_instance_uid,
                    "series_instance_uid": series_instance_uid,
                    "num_instances": num_instances
                }
                await self.send_to_server(data)
                self.series_collector = None
            except Exception as e:
                logger.error(f"Error during dispatching series collector: {e}")

    async def send_to_server(self, data: dict):
        try:
            async with ClientSession() as session:
                headers = {"access_token": "Floy_sirisha"}
                async with session.post("https://localhost:8000/store", json=data, headers=headers, ssl=False) as response:
                    if response.status == 200:
                        logger.info("Data sent successfully")
                    else:
                        logger.error(f"Failed to send data. Status code: {response.status}")
                        response_text = await response.text()
                        logger.error(f"Response: {response_text}")
        except Exception as e:
            logger.error(f"Exception during sending data to server: {e}")

if __name__ == "__main__":
    engine = SeriesDispatcher()
    engine.loop.run_until_complete(engine.main())
