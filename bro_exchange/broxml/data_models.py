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
