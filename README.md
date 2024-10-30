
# Infoctor EHR API

Infoctor EHR API is a multi-tenant Electronic Health Record (EHR) system built with FastAPI, featuring FHIR and HL7 interoperability.

## Features

- Multi-tenant architecture
- Role-based access control
- JWT authentication
- CRUD operations for Organizations, Hospitals, Departments, Providers, and Patients
- FHIR and HL7 interoperability for patient data

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/infoctor-ehr-api.git
   cd infoctor-ehr-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a PostgreSQL database
   - Update the database connection string in `app/database.py`

5. Run the application:
   ```
   uvicorn main:app --reload
   ```

6. Access the API documentation at `http://localhost:8000/docs`

## Usage

1. Create a superuser account using the provided script or API endpoint.
2. Use the superuser account to create organizations and other user accounts.
3. Log in using the `/auth/token` endpoint to obtain a JWT token.
4. Use the JWT token to authenticate requests to other endpoints.

## API Endpoints

- `/auth`: User authentication and management
- `/organizations`: CRUD operations for organizations
- `/hospitals`: CRUD operations for hospitals
- `/departments`: CRUD operations for departments
- `/providers`: CRUD operations for healthcare providers
- `/patients`: CRUD operations for patients, including FHIR and HL7 interoperability

### Interoperability Endpoints

- `GET /patients/{patient_id}/fhir`: Get patient data in FHIR format
- `POST /patients/fhir`: Create a patient from FHIR data
- `GET /patients/{patient_id}/hl7`: Get patient data in HL7 format
- `POST /patients/hl7`: Create a patient from HL7 data
- `POST /patients/send_hl7`: Send patient data as an HL7 message to an external system

For detailed API documentation, refer to the Swagger UI at `/docs` or ReDoc at `/redoc`.

## Running Tests

To run the unit tests for the interoperability module:

1. Ensure you have pytest installed:
   ```
   pip install pytest
   ```

2. Run the tests:
   ```
   pytest tests/test_interoperability.py
   ```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
