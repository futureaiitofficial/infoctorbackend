
-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Organizations table (top level)
CREATE TABLE organizations (
    organization_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    subscription_plan VARCHAR(50),
    status VARCHAR(50) CHECK (status IN ('active', 'suspended', 'terminated')) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Hospitals table
CREATE TABLE hospitals (
    hospital_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    status VARCHAR(50) CHECK (status IN ('active', 'inactive')) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Departments table
CREATE TABLE departments (
    department_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hospital_id UUID NOT NULL REFERENCES hospitals(hospital_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    specialty VARCHAR(100),
    status VARCHAR(50) CHECK (status IN ('active', 'inactive')) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Providers table
CREATE TABLE providers (
    provider_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    department_id UUID NOT NULL REFERENCES departments(department_id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    speciality VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    status VARCHAR(50) CHECK (status IN ('active', 'inactive')) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Patients table
CREATE TABLE patients (
    patient_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20),
    email VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    status VARCHAR(50) CHECK (status IN ('active', 'inactive')) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Users table (for authentication and authorization)
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    status VARCHAR(50) CHECK (status IN ('active', 'inactive')) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for foreign keys
CREATE INDEX idx_hospitals_organization_id ON hospitals(organization_id);
CREATE INDEX idx_departments_hospital_id ON departments(hospital_id);
CREATE INDEX idx_providers_department_id ON providers(department_id);
CREATE INDEX idx_patients_organization_id ON patients(organization_id);
CREATE INDEX idx_users_organization_id ON users(organization_id);

-- ... (previous tables remain the same)

-- Roles table
CREATE TABLE roles (
    role_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Users table (updated to reference roles table)
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES roles(role_id),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) CHECK (status IN ('active', 'inactive')) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for role_id in users table
CREATE INDEX idx_users_role_id ON users(role_id);

-- Insert predefined roles
INSERT INTO roles (name, description) VALUES
('System Administrator', 'Manages overall system configuration, user accounts, and security settings.'),
('Physician', 'Enters and reviews patient medical information, orders tests, and prescribes medications.'),
('Nurse', 'Records patient vital signs, administers medications, and updates patient records.'),
('Medical Assistant', 'Assists with basic clinical tasks, updates patient information, and manages appointments.'),
('Pharmacist', 'Reviews and verifies medication orders, checks for drug interactions.'),
('Lab Technician', 'Enters and manages laboratory test results.'),
('Radiologist', 'Reviews and interprets imaging studies, enters findings into the EHR.'),
('Specialist', 'Provides specialized care and documentation within their field of expertise.'),
('Therapist', 'Documents therapy sessions and patient progress.'),
('Front Desk Staff', 'Manages patient check-in/check-out, schedules appointments, and handles basic administrative tasks.'),
('Billing Specialist', 'Manages insurance claims, coding, and financial aspects of patient care.'),
('HIM Specialist', 'Oversees medical records, ensures compliance with documentation standards.'),
('Quality Assurance Specialist', 'Monitors and reports on quality metrics, identifies areas for improvement.'),
('Compliance Officer', 'Ensures adherence to regulatory requirements and internal policies.'),
('IT Support Specialist', 'Provides technical support for EHR users, manages system updates and troubleshooting.'),
('Clinical Researcher', 'Accesses de-identified patient data for research purposes.'),
('Patient', 'Views personal health information, communicates with providers, and manages appointments through patient portals.'),
('Auditor', 'Reviews system access logs and user activities to ensure security and compliance.'),
('Care Coordinator', 'Manages patient care across different healthcare settings and providers.'),
('Telehealth Specialist', 'Manages virtual care appointments and related documentation.');
