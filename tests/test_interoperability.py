
import pytest
from datetime import date
from uuid import UUID
from app.interoperability import patient_to_fhir, fhir_to_patient, patient_to_hl7, hl7_to_patient
from app.models.patient import Patient
from app.schemas.patient import PatientCreate
from fastapi import HTTPException

@pytest.fixture
def sample_patient():
    return Patient(
        patient_id=UUID("12345678-1234-5678-1234-567812345678"),
        organization_id=UUID("87654321-8765-4321-8765-432187654321"),
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        gender="male",
        email="john.doe@example.com",
        phone="1234567890",
        address="123 Main St, Anytown, USA",
        status="active"
    )

def test_patient_to_fhir(sample_patient):
    fhir_data = patient_to_fhir(sample_patient)
    assert fhir_data["id"] == str(sample_patient.patient_id)
    assert fhir_data["name"][0]["family"] == sample_patient.last_name
    assert fhir_data["name"][0]["given"][0] == sample_patient.first_name
    assert fhir_data["gender"] == sample_patient.gender
    assert fhir_data["birthDate"] == sample_patient.date_of_birth.isoformat()

def test_fhir_to_patient():
    fhir_data = {
        "id": "12345678-1234-5678-1234-567812345678",
        "identifier": [{"value": "87654321-8765-4321-8765-432187654321"}],
        "name": [{"family": "Doe", "given": ["John"]}],
        "gender": "male",
        "birthDate": "1990-01-01"
    }
    patient_create = fhir_to_patient(fhir_data)
    assert patient_create.first_name == "John"
    assert patient_create.last_name == "Doe"
    assert patient_create.gender == "male"
    assert patient_create.date_of_birth == "1990-01-01"
    assert patient_create.organization_id == UUID("87654321-8765-4321-8765-432187654321")

def test_patient_to_hl7(sample_patient):
    hl7_message = patient_to_hl7(sample_patient)
    assert "MSH|^~\&|INFOCTOR|HOSPITAL|HL7RECV|ANYWHERE" in hl7_message
    assert f"PID|||{sample_patient.patient_id}||{sample_patient.last_name}^{sample_patient.first_name}||{sample_patient.date_of_birth}|{sample_patient.gender}" in hl7_message

def test_hl7_to_patient():
    hl7_message = "MSH|^~\&|INFOCTOR|HOSPITAL|HL7RECV|ANYWHERE|20230101000000||ADT^A01|MSG00001|P|2.3\rPID|||87654321-8765-4321-8765-432187654321||Doe^John||1990-01-01|male"
    patient_create = hl7_to_patient(hl7_message)
    assert patient_create.first_name == "John"
    assert patient_create.last_name == "Doe"
    assert patient_create.gender == "male"
    assert patient_create.date_of_birth == "1990-01-01"
    assert patient_create.organization_id == UUID("87654321-8765-4321-8765-432187654321")

def test_fhir_to_patient_invalid_data():
    invalid_fhir_data = {"name": [{"family": "Doe"}]}  # Missing 'given' name
    with pytest.raises(HTTPException) as excinfo:
        fhir_to_patient(invalid_fhir_data)
    assert "Invalid FHIR data: Missing key" in str(excinfo.value)

def test_hl7_to_patient_invalid_message():
    invalid_hl7_message = "MSH|^~\&|INFOCTOR|HOSPITAL|HL7RECV|ANYWHERE|20230101000000||ADT^A01|MSG00001|P|2.3\rPID|||87654321-8765-4321-8765-432187654321"  # Missing patient name
    with pytest.raises(HTTPException) as excinfo:
        hl7_to_patient(invalid_hl7_message)
    assert "Invalid HL7 message: Missing required field" in str(excinfo.value)
