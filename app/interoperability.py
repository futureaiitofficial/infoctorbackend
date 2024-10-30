
from fhir.resources.patient import Patient as FHIRPatient
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from hl7 import parse as hl7_parse
from hl7.client import MLLPClient
from app.models.patient import Patient
from app.schemas.patient import PatientCreate
from uuid import UUID
import json
from fastapi import HTTPException

def patient_to_fhir(patient: Patient) -> dict:
    try:
        fhir_patient = FHIRPatient(
            id=str(patient.patient_id),
            identifier=[Identifier(value=str(patient.patient_id))],
            name=[HumanName(family=patient.last_name, given=[patient.first_name])],
            gender=patient.gender,
            birthDate=patient.date_of_birth.isoformat()
        )
        return json.loads(fhir_patient.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting patient to FHIR: {str(e)}")

def fhir_to_patient(fhir_data: dict) -> PatientCreate:
    try:
        return PatientCreate(
            first_name=fhir_data['name'][0]['given'][0],
            last_name=fhir_data['name'][0]['family'],
            date_of_birth=fhir_data['birthDate'],
            gender=fhir_data['gender'],
            organization_id=UUID(fhir_data['identifier'][0]['value'])
        )
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Invalid FHIR data: Missing key {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting FHIR to patient: {str(e)}")

def patient_to_hl7(patient: Patient) -> str:
    try:
        hl7_message = f"MSH|^~\&|INFOCTOR|HOSPITAL|HL7RECV|ANYWHERE|20230101000000||ADT^A01|MSG00001|P|2.3\r"
        hl7_message += f"PID|||{patient.patient_id}||{patient.last_name}^{patient.first_name}||{patient.date_of_birth}|{patient.gender}"
        return hl7_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting patient to HL7: {str(e)}")

def hl7_to_patient(hl7_message: str) -> PatientCreate:
    try:
        parsed_message = hl7_parse(hl7_message)
        pid_segment = parsed_message.segment('PID')
        
        return PatientCreate(
            first_name=str(pid_segment[5][1]),
            last_name=str(pid_segment[5][0]),
            date_of_birth=str(pid_segment[7]),
            gender=str(pid_segment[8]),
            organization_id=UUID(str(pid_segment[3][0]))
        )
    except IndexError as e:
        raise HTTPException(status_code=400, detail=f"Invalid HL7 message: Missing required field {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting HL7 to patient: {str(e)}")

async def send_hl7_message(host: str, port: int, message: str):
    try:
        async with MLLPClient(host, port) as client:
            response = await client.send_message(message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending HL7 message: {str(e)}")
