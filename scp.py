import logging
from pydicom.dataset import FileMetaDataset
from pynetdicom import AE, events, evt, debug_logger
from pynetdicom.sop_class import (
    MRImageStorage, CTImageStorage, SecondaryCaptureImageStorage,
    AmbulatoryECGWaveformStorage, BasicTextSRStorage, BasicVoiceAudioWaveformStorage,
    BlendingSoftcopyPresentationStateStorage, CardiacElectrophysiologyWaveformStorage,
    ChestCADSRStorage, ColonCADSRStorage, ColorSoftcopyPresentationStateStorage,
    ComprehensiveSRStorage, ComputedRadiographyImageStorage, DigitalIntraOralXRayImageStorageForPresentation,
    DigitalIntraOralXRayImageStorageForProcessing, DigitalMammographyXRayImageStorageForPresentation,
    DigitalMammographyXRayImageStorageForProcessing, DigitalXRayImageStorageForPresentation,
    DigitalXRayImageStorageForProcessing, EncapsulatedPDFStorage, EnhancedCTImageStorage,
    EnhancedMRImageStorage, EnhancedSRStorage, EnhancedXAImageStorage, EnhancedXRFImageStorage,
    GeneralECGWaveformStorage, GrayscaleSoftcopyPresentationStateStorage, HemodynamicWaveformStorage,
    KeyObjectSelectionDocumentStorage, MammographyCADSRStorage, MRSpectroscopyStorage,
    MultiFrameGrayscaleByteSecondaryCaptureImageStorage, MultiFrameGrayscaleWordSecondaryCaptureImageStorage,
    MultiFrameSingleBitSecondaryCaptureImageStorage, MultiFrameTrueColorSecondaryCaptureImageStorage,
    NuclearMedicineImageStorage, OphthalmicPhotography16BitImageStorage, OphthalmicPhotography8BitImageStorage,
    OphthalmicTomographyImageStorage, PositronEmissionTomographyImageStorage, ProcedureLogStorage,
    RawDataStorage, RealWorldValueMappingStorage,
    RTBeamsTreatmentRecordStorage, RTBrachyTreatmentRecordStorage, RTDoseStorage, RTImageStorage,
    RTPlanStorage, RTStructureSetStorage, RTTreatmentSummaryRecordStorage, SpatialFiducialsStorage,
    SpatialRegistrationStorage, StereometricRelationshipStorage, TwelveLeadECGWaveformStorage,
    UltrasoundImageStorage, UltrasoundMultiFrameImageStorage, VLEndoscopicImageStorage,
    VLMicroscopicImageStorage, VLPhotographicImageStorage, VLSlideCoordinatesMicroscopicImageStorage,
    XRayAngiographicImageStorage, XRayRadiationDoseSRStorage
)

debug_logger()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ModalityStoreSCP:
    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher
        self.ae = AE(ae_title=b'STORESCP')
        self.scp = None
        self._configure_ae()

    def _configure_ae(self) -> None:
        handlers = [(evt.EVT_C_STORE, self.handle_store)]
        sop_classes = [
            MRImageStorage, CTImageStorage, SecondaryCaptureImageStorage,
            AmbulatoryECGWaveformStorage, BasicTextSRStorage, BasicVoiceAudioWaveformStorage,
            BlendingSoftcopyPresentationStateStorage, CardiacElectrophysiologyWaveformStorage,
            ChestCADSRStorage, ColonCADSRStorage, ColorSoftcopyPresentationStateStorage,
            ComprehensiveSRStorage, ComputedRadiographyImageStorage, DigitalIntraOralXRayImageStorageForPresentation,
            DigitalIntraOralXRayImageStorageForProcessing, DigitalMammographyXRayImageStorageForPresentation,
            DigitalMammographyXRayImageStorageForProcessing, DigitalXRayImageStorageForPresentation,
            DigitalXRayImageStorageForProcessing, EncapsulatedPDFStorage, EnhancedCTImageStorage,
            EnhancedMRImageStorage, EnhancedSRStorage, EnhancedXAImageStorage, EnhancedXRFImageStorage,
            GeneralECGWaveformStorage, GrayscaleSoftcopyPresentationStateStorage, HemodynamicWaveformStorage,
            KeyObjectSelectionDocumentStorage, MammographyCADSRStorage, MRSpectroscopyStorage,
            MultiFrameGrayscaleByteSecondaryCaptureImageStorage, MultiFrameGrayscaleWordSecondaryCaptureImageStorage,
            MultiFrameSingleBitSecondaryCaptureImageStorage, MultiFrameTrueColorSecondaryCaptureImageStorage,
            NuclearMedicineImageStorage, OphthalmicPhotography16BitImageStorage, OphthalmicPhotography8BitImageStorage,
            OphthalmicTomographyImageStorage, PositronEmissionTomographyImageStorage, ProcedureLogStorage,
            RawDataStorage, RealWorldValueMappingStorage,
            RTBeamsTreatmentRecordStorage, RTBrachyTreatmentRecordStorage, RTDoseStorage, RTImageStorage,
            RTPlanStorage, RTStructureSetStorage, RTTreatmentSummaryRecordStorage, SpatialFiducialsStorage,
            SpatialRegistrationStorage, StereometricRelationshipStorage, TwelveLeadECGWaveformStorage,
            UltrasoundImageStorage, UltrasoundMultiFrameImageStorage, VLEndoscopicImageStorage,
            VLMicroscopicImageStorage, VLPhotographicImageStorage, VLSlideCoordinatesMicroscopicImageStorage,
            XRayAngiographicImageStorage, XRayRadiationDoseSRStorage
        ]

        for sop_class in sop_classes:
            self.ae.add_supported_context(sop_class)

        self.scp = self.ae.start_server(('127.0.0.1', 6667), block=False, evt_handlers=handlers)
        logger.info("SCP Server started")

    def handle_store(self, event: events.Event) -> int:
        dataset = event.dataset
        dataset.file_meta = event.file_meta
        try:
            
            logger.debug(f"Received dataset with SOP Instance UID: {dataset.SOPInstanceUID}")
            logger.debug(f"Dataset transfer syntax: {event.context.transfer_syntax}")
            logger.debug("Complete dataset:")
            logger.debug(dataset)

            # Add the dataset to the dispatcher
            self.dispatcher.add_dataset(dataset)
            logger.info("Dataset successfully added to dispatcher")

            return 0x0000  
        except Exception as e:
            logger.error(f"Failed to handle store request: {e}")
            return 0xC000  
