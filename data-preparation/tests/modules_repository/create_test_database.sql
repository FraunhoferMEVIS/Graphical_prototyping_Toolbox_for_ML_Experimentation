-- Create Schema
CREATE SCHEMA mimiciv_hosp;
CREATE SCHEMA mimiciv_icu;

-- Create Tables
CREATE TABLE mimiciv_hosp.admissions
(
    subject_id INTEGER NOT NULL,
    hadm_id INTEGER NOT NULL,
    admittime TIMESTAMP NOT NULL,
    dischtime TIMESTAMP,
    deathtime TIMESTAMP,
    admission_type VARCHAR(40) NOT NULL,
    admission_location VARCHAR(60),
    discharge_location VARCHAR(60),
    insurance VARCHAR(255),
    language VARCHAR(10),
    marital_status VARCHAR(30),
    race VARCHAR(80),
    edregtime TIMESTAMP,
    edouttime TIMESTAMP,
    hospital_expire_flag SMALLINT
);

CREATE TABLE mimiciv_hosp.patients
(
    subject_id INTEGER NOT NULL,
    gender CHAR(1) NOT NULL,
    anchor_age SMALLINT,
    anchor_year SMALLINT NOT NULL,
    anchor_year_group VARCHAR(20) NOT NULL,
    dod DATE
);

CREATE TABLE mimiciv_icu.chartevents
(
    subject_id INTEGER NOT NULL,
    hadm_id INTEGER NOT NULL,
    stay_id INTEGER NOT NULL,
    charttime TIMESTAMP NOT NULL,
    storetime TIMESTAMP,
    itemid INTEGER NOT NULL,
    value VARCHAR(200),
    valuenum FLOAT,
    valueuom VARCHAR(20),
    warning SMALLINT
);

-- Add Random Data to the Tables
INSERT INTO mimiciv_hosp.admissions
(
    subject_id,
    hadm_id,
    admittime,
    dischtime,
    deathtime,
    admission_type,
    admission_location,
    discharge_location,
    insurance,
    language,
    marital_status,
    race,
    edregtime,
    edouttime,
    hospital_expire_flag
)
SELECT
    generate_series(1, 100) AS subject_id,
    generate_series(1000, 1099) AS hadm_id,
    NOW() - (random() * 365 * 5 || ' days')::INTERVAL AS admittime,
    NOW() - (random() * 365 || ' days')::INTERVAL AS dischtime,
    NOW() - (random() * 365 * 2 || ' days')::INTERVAL AS deathtime,
    CASE WHEN random() < 0.5 THEN 'Emergency' ELSE 'Elective' END AS admission_type,
    CASE WHEN random() < 0.2 THEN 'Emergency Room' ELSE 'Floor' END AS admission_location,
    CASE WHEN random() < 0.2 THEN 'Home' ELSE 'Floor' END AS discharge_location,
    CASE WHEN random() < 0.3 THEN 'Private' ELSE 'Medicaid' END AS insurance,
    CASE WHEN random() < 0.7 THEN 'English' ELSE 'Spanish' END AS language,
    CASE WHEN random() < 0.5 THEN 'Married' ELSE 'Single' END AS marital_status,
    CASE WHEN random() < 0.8 THEN 'White' ELSE 'Black' END AS race,
    NOW() - (random() * 365 * 5 || ' days')::INTERVAL AS edregtime,
    NOW() - (random() * 365 * 4 || ' days')::INTERVAL AS edouttime,
    CASE WHEN random() < 0.1 THEN 1 ELSE 0 END AS hospital_expire_flag
FROM generate_series(1, 100);

INSERT INTO mimiciv_hosp.patients
(
    subject_id,
    gender,
    anchor_age,
    anchor_year,
    anchor_year_group,
    dod
)
SELECT
    generate_series(1, 100) AS subject_id,
    CASE WHEN random() < 0.5 THEN 'M' ELSE 'F' END AS gender,
    trunc(random() * 100) AS anchor_age,
    extract(year from NOW())::INTEGER - trunc(random() * 10) AS anchor_year,
    CASE
        WHEN random() < 0.3 THEN 'Young'
        WHEN random() < 0.6 THEN 'Middle'
        ELSE 'Old'
    END AS anchor_year_group,
    CASE WHEN random() < 0.1 THEN NOW() - (random() * 365 * 2 || ' days')::INTERVAL ELSE NULL END AS dod
FROM generate_series(1, 1000);

INSERT INTO mimiciv_icu.chartevents
(
    subject_id,
    hadm_id,
    stay_id,
    charttime,
    storetime,
    itemid,
    value,
    valuenum,
    valueuom,
    warning
)
SELECT
    generate_series(1, 100) AS subject_id,
    generate_series(1000, 1099) AS hadm_id,
    generate_series(2000, 2099) AS stay_id,
    NOW() - (random() * 365 * 5 || ' days')::INTERVAL AS charttime,
    NOW() - (random() * 365 * 5 || ' days')::INTERVAL AS storetime,
    generate_series(3000, 3099) AS itemid,
    CASE WHEN random() < 0.8 THEN random()::TEXT ELSE NULL END AS value,
    CASE WHEN random() < 0.8 THEN random() ELSE NULL END AS valuenum,
    CASE WHEN random() < 0.8 THEN 'units' ELSE NULL END AS valueuom,
    CASE WHEN random() < 0.1 THEN 1 ELSE 0 END AS warning
FROM generate_series(1, 1000);