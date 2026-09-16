"""Typed payload models for BRO source-document generators.

These dataclasses are optional convenience wrappers. Request classes and
source-document generators accept plain dictionaries as before.
"""

from dataclasses import dataclass, field
from typing import Any

# GMW


@dataclass
class GmwDeliveredLocation:
    X: float
    Y: float
    horizontalPositioningMethod: str


@dataclass
class GmwDeliveredVerticalPosition:
    localVerticalReferencePoint: str
    offset: float
    verticalDatum: str
    groundLevelPosition: float
    groundLevelPositioningMethod: str


@dataclass
class GmwConstructionRegistrationData:
    objectIdAccountableParty: str
    deliveryContext: str
    constructionStandard: str
    initialFunction: str
    numberOfMonitoringTubes: int
    groundLevelStable: str
    owner: int | str
    wellHeadProtector: str
    wellConstructionDate: str
    deliveredLocation: GmwDeliveredLocation | dict[str, Any]
    deliveredVerticalPosition: GmwDeliveredVerticalPosition | dict[str, Any]
    monitoringTubes: list[dict[str, Any]] = field(default_factory=list)
    wellStability: str | None = None
    nitgCode: str | None = None
    maintenanceResponsibleParty: int | str | None = None


# GMN


@dataclass
class GmnMonitoringTubeRef:
    broId: str
    tubeNumber: int


@dataclass
class GmnMeasuringPoint:
    measuringPointCode: str
    monitoringTube: GmnMonitoringTubeRef | dict[str, Any]


@dataclass
class GmnStartRegistrationData:
    objectIdAccountableParty: str
    name: str
    deliveryContext: str
    monitoringPurpose: str
    groundwaterAspect: str
    startDateMonitoring: list[str | None]
    measuringPoints: list[GmnMeasuringPoint | dict[str, Any]]


@dataclass
class GmnMeasuringPointData:
    eventDate: list[str | None]
    measuringPoint: GmnMeasuringPoint | dict[str, Any]


@dataclass
class GmnClosureData:
    endDateMonitoring: list[str | None]


@dataclass
class GmnTubeReferenceData:
    eventDate: list[str | None]
    measuringPoint: GmnMeasuringPoint | dict[str, Any]


# GLD


@dataclass
class GldMonitoringPointRef:
    broId: str
    tubeNumber: int


@dataclass
class GldStartRegistrationData:
    monitoringPoints: list[GldMonitoringPointRef | dict[str, Any]]
    objectIdAccountableParty: str | None = None
    groundwaterMonitoringNets: list[dict[str, Any]] = field(default_factory=list)


# GAR


@dataclass
class GarFieldMeasurement:
    parameter: str
    unit: str
    fieldMeasurementValue: float | str
    qualityControlStatus: str


@dataclass
class GarFieldResearch:
    samplingDateTime: str
    samplingStandard: str
    pumpType: str
    abnormalityInCooling: bool | str
    abnormalityInDevice: bool | str
    pollutedByEngine: bool | str
    filterAerated: bool | str
    groundWaterLevelDroppedTooMuch: bool | str
    abnormalFilter: bool | str
    sampleAerated: bool | str
    hoseReused: bool | str
    temperatureDifficultToMeasure: bool | str
    samplingOperator: str | None = None
    primaryColour: str | None = None
    secondaryColour: str | None = None
    colourStrength: str | None = None
    fieldMeasurements: list[GarFieldMeasurement | dict[str, Any]] = field(
        default_factory=list
    )


@dataclass
class GarAnalysis:
    parameter: str
    qualityControlStatus: str
    unit: str | None = None
    analysisMeasurementValue: float | str | None = None
    limitSymbol: str | None = None
    reportingLimit: float | str | None = None


@dataclass
class GarAnalysisProcess:
    analyses: list[GarAnalysis | dict[str, Any]]
    date: str | None = None
    analyticalTechnique: str | None = None
    valuationMethod: str | None = None


@dataclass
class GarLaboratoryAnalysis:
    analysisProcesses: list[GarAnalysisProcess | dict[str, Any]]
    responsibleLaboratoryKvk: str | None = None


@dataclass
class GarRegistrationData:
    objectIdAccountableParty: str
    qualityControlMethod: str
    gmwBroId: str
    tubeNumber: int | str
    fieldResearch: GarFieldResearch | dict[str, Any]
    groundwaterMonitoringNets: list[str] = field(default_factory=list)
    laboratoryAnalyses: list[GarLaboratoryAnalysis | dict[str, Any]] = field(
        default_factory=list
    )
