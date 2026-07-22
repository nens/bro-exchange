import os
from typing import Any

from lxml import etree

from bro_exchange.bhp.connector import deliver_requests, validate_request
from bro_exchange.broxml.mappings import (  # mappings
    codespace_map_gld1,
    ns_regreq_map_gld1,
    ns_regreq_map_gld2,
    ns_regreq_map_gld3,
    xsi_regreq_map_gld1,
)
from bro_exchange.broxml.request_helpers import (
    check_required_kwargs,
    coerce_srcdocdata,
    has_value,
    normalize_optional_kwargs,
)
from bro_exchange.checks import check_missing_args

from .sourcedocs import gen_gld_startregistration, gen_gld_addition


def get_supported_gld_srcdocs() -> dict[str, tuple[str, ...]]:
    """Return supported GLD source-document names per request type."""

    return {
        "registration": ("GLD_StartRegistration", "GLD_Addition", "GLD_Closure"),
        "replace": ("GLD_StartRegistration", "GLD_Addition"),
        "delete": ("GLD_Addition", "GLD_Closure"),
    }


# =============================================================================
# General info
# =============================================================================

# https://schema.broservices.nl/xsd/isgmw/1.1/isgmw-messages.xsd


# %%


class gld_registration_request:

    """
    Build a GLD registration request XML.

    Supported srcdocs are available through `get_supported_gld_srcdocs()["registration"]`.
    """

    def __init__(self, srcdoc: str, **kwargs: Any):
        """
        Parameters
        ----------
        srcdoc:
            One of the supported GLD registration source document names.
        **kwargs:
            - `requestReference` (required)
            - `qualityRegime` (required)
            - `srcdocdata` (required): dict, `SourceDocData`, or dataclass instance.
            - `deliveryAccountableParty` (optional)
            - `broId` (optional; only required for specific srcdocs)
        """

        # NOTE: IN PROGRESS, MORE SOURCEDOCUMENTS TYPES WILL BE INCLUDED

        self.allowed_srcdocs = list(get_supported_gld_srcdocs()["registration"])

        if srcdoc not in self.allowed_srcdocs:
            raise Exception("Sourcedocument type not allowed")

        self.srcdoc = srcdoc
        self.kwargs = kwargs
        self.request = None
        self.validation_info = None
        self.validation_report = None
        self.delivery_info = None
        self.delivery_id = None

        normalize_optional_kwargs(self.kwargs, ["deliveryAccountableParty", "broId"])

        # Request arguments:
        arglist = {
            "deliveryAccountableParty": "optional",
            "broId": "optional",
            "qualityRegime": "obligated",
            "requestReference": "obligated",
            "srcdocdata": "obligated",
        }

        # Check wether all obligated registration request arguments for method 'initialize' are in kwargs
        check_missing_args(
            self.kwargs, arglist, "gmw_registration with method initialize"
        )
        check_required_kwargs(
            self.kwargs, arglist, "gmw_registration with method initialize"
        )
        self.kwargs["srcdocdata"] = coerce_srcdocdata(self.kwargs["srcdocdata"])

        self.requestreference = self.kwargs["requestReference"]

    def generate(self):
        # Generate xml document base:
        if self.srcdoc == "GLD_StartRegistration":
            req = etree.Element(
                "registrationRequest",
                nsmap=ns_regreq_map_gld2,
                attrib={
                    "xmlns": ns_regreq_map_gld1["xmlns"],
                    ("{%s}" % ns_regreq_map_gld2["xsi"])
                    + "schemaLocation": xsi_regreq_map_gld1["schemaLocation"],
                },
            )

        elif self.srcdoc == "GLD_Addition":
            req = etree.Element(
                "registrationRequest",
                nsmap=ns_regreq_map_gld3,
                attrib={
                    "xmlns": ns_regreq_map_gld1["xmlns"],
                    ("{%s}" % ns_regreq_map_gld3["xsi"])
                    + "schemaLocation": xsi_regreq_map_gld1["schemaLocation"],
                },
            )

        # Define registration request arguments:
        requestReference = etree.SubElement(
            req,
            ("{%s}" % ns_regreq_map_gld2["brocom"]) + "requestReference",
            nsmap=ns_regreq_map_gld2,
        )
        requestReference.text = self.kwargs["requestReference"]
        
        if "deliveryAccountableParty" in self.kwargs:
            deliveryAccountableParty = etree.SubElement(
                req,
                ("{%s}" % ns_regreq_map_gld2["brocom"]) + "deliveryAccountableParty",
                nsmap=ns_regreq_map_gld2,
            )
            deliveryAccountableParty.text = str(self.kwargs["deliveryAccountableParty"])

        bro_id = self.kwargs.get("broId", None)
        if has_value(bro_id):
            broId = etree.SubElement(
                req,
                ("{%s}" % ns_regreq_map_gld2["brocom"]) + "broId",
                nsmap=ns_regreq_map_gld2,
            )
            broId.text = str(bro_id)

        qualityRegime = etree.SubElement(
            req,
            ("{%s}" % ns_regreq_map_gld2["brocom"]) + "qualityRegime",
            nsmap=ns_regreq_map_gld2,
        )
        qualityRegime.text = str(self.kwargs["qualityRegime"])

        # Create sourcedocument and add to registrationrequest:
        if self.srcdoc == "GLD_StartRegistration":
            if "broId" in self.kwargs:
                raise Exception(
                    "Registration request argument 'broId' not allowed in combination with given sourcedocument"
                )
            else:
                sourceDocument = gen_gld_startregistration(
                    self.kwargs["srcdocdata"], ns_regreq_map_gld2, codespace_map_gld1
                )
                req.append(sourceDocument)

        elif self.srcdoc == "GLD_Addition":
            if "broId" not in self.kwargs:
                raise Exception(
                    "Registration request argument 'broId' required in combination with given sourcedocument"
                )
            else:
                sourceDocument = gen_gld_addition(
                    self.kwargs["srcdocdata"], ns_regreq_map_gld3, codespace_map_gld1
                )
                req.append(sourceDocument)

        self.requesttree = etree.ElementTree(req)
        self.request = etree.tostring(self.requesttree, encoding="utf8", method="xml")
        # print(etree.tostring(req, pretty_print=True,encoding='unicode'))

    def write_request(self, filename, output_dir=None):
        if output_dir is None:
            self.requesttree.write(filename, pretty_print=True)
        else:
            self.requesttree.write(
                os.path.join(output_dir, filename), pretty_print=True
            )

    def validate(
        self,
        token=None,
        user=None,
        password=None,
        project_id=None,
        demo=False,
    ):
        if self.request is None:
            raise Exception("Request isn't generated yet")
        self.validation_info = validate_request(
            self.request, token, user, password, project_id, demo
        )
        try:
            self.validation_status = self.validation_info["status"]
        except:
            pass

    def deliver(
        self,
        token=None,
        user=None,
        password=None,
        project_id=None,
        demo=False,
    ):
        if self.delivery_id is not None:
            raise Exception("Request has already been delivered")
        if self.validation_status != "VALIDE":
            raise Exception("Request isn't valid")
        if self.validation_status is None:
            raise Exception("Request isn't validated")

        reqs = {self.requestreference: self.request}

        self.delivery_info = deliver_requests(
            reqs, token, user, password, project_id, demo
        )

        try:
            self.delivery_id = self.delivery_info.json()["identifier"]
        except:
            pass


# %% gld replace request


class gld_replace_request:
    # VRAAG: WAT IS VOOR GLD ADDITION DE EENHEID VAN CORRECTIE? WORDEN DE
    # GML IDS VAN HET OBSPROC EN OBS VERVANGEN OF NIET?

    # AANNAME: BIJ DE ID's van OBSPROC mag de gml id in de replace niet
    # aanwezig zijn in een ander document (gaat hier aannemelijk niet om href,
    # maar echt om de initialisatie). De observation gml id mag ook niet eerder
    # gebruikt zijn (betekend ook niet gml id van oude observatie)

    """
    Build a GLD replace request XML.

    Supported srcdocs are available through `get_supported_gld_srcdocs()["replace"]`.
    """

    def __init__(self, srcdoc: str, **kwargs: Any):
        """
        Parameters
        ----------
        srcdoc:
            One of the supported GLD replace source document names.
        **kwargs:
            - `requestReference` (required)
            - `qualityRegime` (required)
            - `correctionReason` (required)
            - `srcdocdata` (required): dict, `SourceDocData`, or dataclass instance.
            - `deliveryAccountableParty` (optional)
            - `broId` (required for current supported srcdocs)
        """

        # NOTE: IN PROGRESS, MORE SOURCEDOCUMENTS TYPES WILL BE INCLUDED

        self.allowed_srcdocs = list(get_supported_gld_srcdocs()["replace"])

        if srcdoc not in self.allowed_srcdocs:
            raise Exception("Sourcedocument type not allowed")

        self.srcdoc = srcdoc
        self.kwargs = kwargs
        self.request = None
        self.validation_info = None
        self.validation_report = None
        self.delivery_info = None
        self.delivery_id = None

        normalize_optional_kwargs(self.kwargs, ["deliveryAccountableParty", "broId"])

        # Request arguments:
        arglist = {
            "deliveryAccountableParty": "optional",
            "broId": "optional",
            "qualityRegime": "obligated",
            "requestReference": "obligated",
            "correctionReason": "obligated",
            "srcdocdata": "obligated",
        }

        # Check wether all obligated registration request arguments for method 'initialize' are in kwargs
        check_missing_args(
            self.kwargs, arglist, "gmw_registration with method initialize"
        )
        check_required_kwargs(
            self.kwargs, arglist, "gmw_registration with method initialize"
        )
        self.kwargs["srcdocdata"] = coerce_srcdocdata(self.kwargs["srcdocdata"])

        self.requestreference = self.kwargs["requestReference"]

    def generate(self):
        # Generate xml document base:
        if self.srcdoc in ["GLD_StartRegistration", "GLD_Addition"]:
            req = etree.Element(
                "replaceRequest",
                nsmap=ns_regreq_map_gld3,
                attrib={
                    "xmlns": ns_regreq_map_gld1["xmlns"],
                    ("{%s}" % ns_regreq_map_gld3["xsi"])
                    + "schemaLocation": xsi_regreq_map_gld1["schemaLocation"],
                },
            )

        # Define registration request arguments:
        requestReference = etree.SubElement(
            req,
            ("{%s}" % ns_regreq_map_gld2["brocom"]) + "requestReference",
            nsmap=ns_regreq_map_gld2,
        )
        requestReference.text = self.kwargs["requestReference"]

        delivery_accountable_party = self.kwargs.get("deliveryAccountableParty")
        if has_value(delivery_accountable_party):
            deliveryAccountableParty = etree.SubElement(
                req,
                ("{%s}" % ns_regreq_map_gld2["brocom"]) + "deliveryAccountableParty",
                nsmap=ns_regreq_map_gld2,
            )
            deliveryAccountableParty.text = str(delivery_accountable_party)

        bro_id = self.kwargs.get("broId")
        if has_value(bro_id):
            broId = etree.SubElement(
                req,
                ("{%s}" % ns_regreq_map_gld2["brocom"]) + "broId",
                nsmap=ns_regreq_map_gld2,
            )
            broId.text = str(bro_id)

        qualityRegime = etree.SubElement(
            req,
            ("{%s}" % ns_regreq_map_gld2["brocom"]) + "qualityRegime",
            nsmap=ns_regreq_map_gld2,
        )
        qualityRegime.text = self.kwargs["qualityRegime"]

        correctionReason = etree.SubElement(
            req,
            "correctionReason",
            attrib={"codeSpace": "urn:bro:gld:CorrectionReason"},
            nsmap=ns_regreq_map_gld2,
        )

        correctionReason.text = self.kwargs["correctionReason"]

        # Create sourcedocument and add to registrationrequest:
        if self.srcdoc == "GLD_StartRegistration":
            if "broId" not in self.kwargs:
                raise Exception(
                    "Registration request argument 'broId' required in combination with given sourcedocument"
                )
            else:
                sourceDocument = gen_gld_startregistration(
                    self.kwargs["srcdocdata"], ns_regreq_map_gld2, codespace_map_gld1
                )
                req.append(sourceDocument)

        elif self.srcdoc == "GLD_Addition":
            if "broId" not in self.kwargs:
                raise Exception(
                    "Registration request argument 'broId' required in combination with given sourcedocument"
                )
            else:
                sourceDocument = gen_gld_addition(
                    self.kwargs["srcdocdata"], ns_regreq_map_gld3, codespace_map_gld1
                )
                req.append(sourceDocument)

        self.requesttree = etree.ElementTree(req)
        self.request = etree.tostring(self.requesttree, encoding="utf8", method="xml")
        # print(etree.tostring(req, pretty_print=True,encoding='unicode'))

    def write_request(self, filename, output_dir=None):
        if output_dir is None:
            self.requesttree.write(filename, pretty_print=True)
        else:
            self.requesttree.write(
                os.path.join(output_dir, filename), pretty_print=True
            )

    def validate(
        self,
        token=None,
        user=None,
        password=None,
        project_id=None,
        demo=False,
    ):
        if self.request is None:
            raise Exception("Request isn't generated yet")
        self.validation_info = validate_request(
            self.request, token, user, password, project_id, demo
        )
        try:
            self.validation_status = self.validation_info["status"]
        except:
            pass

    def deliver(
        self,
        token=None,
        user=None,
        password=None,
        project_id=None,
        demo=False,
    ):
        if self.delivery_id is not None:
            raise Exception("Request has already been delivered")
        if self.validation_status != "VALIDE":
            raise Exception("Request isn't valid")
        if self.validation_status is None:
            raise Exception("Request isn't validated")

        reqs = {self.requestreference: self.request}

        self.delivery_info = deliver_requests(
            reqs, token, user, password, project_id, demo
        )
        try:
            self.delivery_id = self.delivery_info.json()["identifier"]
        except:
            pass


# %% delete request:


class gld_delete_request:

    """
    Convert an existing GLD request XML into a delete request XML.

    Supported srcdocs are available through `get_supported_gld_srcdocs()["delete"]`.
    """

    def __init__(
        self,
        srcdoc: bytes | str,
        correctionReason: str,
        requestReference: str | None = None,
    ):
        """

        Parameters
        ----------
        srcdoc : string
            sourcedoc to be deleted (check allowed srcdoc types)

        Returns
        -------
        None, saves generated replace request xml to output directory

        """
        print("BRO Exchange: GLD Delete Request needs to be updated.")

        self.allowed_srcdocs = list(get_supported_gld_srcdocs()["delete"])
        self.srcdoc = etree.fromstring(srcdoc)
        self.correctionReason = correctionReason
        self.request = None
        self.requesttree = None
        self.validation_info = None
        self.validation_report = None
        self.delivery_info = None
        self.delivery_id = None
        self.validation_status = None

        check = "unvalid"

        for element in list(self.srcdoc.iter()):
            # print(element.tag)
            for allowed in self.allowed_srcdocs:
                if allowed in element.tag:
                    check = "valid"

        if check != "valid":
            raise Exception("Sourcedocument type not allowed")

        self.requestreference = requestReference
        if self.requestreference is None:
            for element in list(self.srcdoc.iter()):
                if "requestReference" in element.tag and element.text:
                    self.requestreference = element.text
                    break

    def generate(self):
        correctionreason_there = False

        for element in list(self.srcdoc.iter()):
            # print(element.tag)
            if "correctionReason" in element.tag:
                correctionreason_there = True
                correctionreason_el = element
            if "qualityRegime" in element.tag:
                qualityRegime_el = element.tag
            if "Request" in element.tag:
                element.tag = "deleteRequest"

        if correctionreason_there is False:
            correctionReason = etree.Element(
                "correctionReason", attrib={"codeSpace": "urn:bro:gld:CorrectionReason"}
            )
            correctionReason.text = self.correctionReason
            qualityRegime_el = self.srcdoc.find(qualityRegime_el)

            qualityRegime_el.addnext(correctionReason)

        else:
            correctionreason_el.text = self.correctionReason

        self.request = etree.tostring(self.srcdoc)

        self.requesttree = etree.ElementTree(self.srcdoc)

    def write_request(self, filename, output_dir=None):
        if output_dir is None:
            self.requesttree.write(filename, pretty_print=True)
        else:
            self.requesttree.write(
                os.path.join(output_dir, filename), pretty_print=True
            )

    def validate(
        self,
        token=None,
        user=None,
        password=None,
        project_id=None,
        demo=False,
    ):
        if self.request is None:
            raise Exception("Request isn't generated yet")
        self.validation_info = validate_request(
            self.request, token, user, password, project_id, demo
        )
        try:
            self.validation_status = self.validation_info["status"]
        except:
            pass

    def deliver(
        self,
        token=None,
        user=None,
        password=None,
        project_id=None,
        demo=False,
    ):
        if self.delivery_id is not None:
            raise Exception("Request has already been delivered")
        if self.validation_status != "VALIDE":
            raise Exception("Request isn't valid")
        if self.validation_status is None:
            raise Exception("Request isn't validated")

        reqs = {self.requestreference: self.request}

        self.delivery_info = deliver_requests(
            reqs, token, user, password, project_id, demo
        )
        try:
            self.delivery_id = self.delivery_info.json()["identifier"]
        except:
            pass
