-- =========================
-- CHILD PROFILE TABLE
-- =========================
CREATE TABLE child_profile (
    child_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
    parent_phone VARCHAR(15) NOT NULL,
    village VARCHAR(100),
    district VARCHAR(100),
    weight_kg NUMERIC(5,2) CHECK (weight_kg > 0),
    blood_group VARCHAR(5),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster search by location
CREATE INDEX idx_child_location 
ON child_profile (village, district);

-- =========================
-- VACCINE SCHEDULE TABLE (NIS Reference)
-- =========================
CREATE TABLE vaccine_schedule (
    schedule_id SERIAL PRIMARY KEY,
    vaccine_name VARCHAR(100) NOT NULL,
    dose_number INT NOT NULL CHECK (dose_number > 0),
    recommended_age VARCHAR(50) NOT NULL, -- e.g., "At Birth", "6 Weeks"
    min_age_days INT CHECK (min_age_days >= 0),
    max_age_days INT CHECK (max_age_days >= min_age_days),

    UNIQUE (vaccine_name, dose_number)
);

-- Index for quick lookup
CREATE INDEX idx_schedule_vaccine 
ON vaccine_schedule (vaccine_name);

-- =========================
-- VACCINATION RECORD TABLE
-- =========================
CREATE TABLE vaccination_record (
    record_id SERIAL PRIMARY KEY,
    child_id INT NOT NULL,
    vaccine_name VARCHAR(100) NOT NULL,
    dose_number INT NOT NULL,
    date_given DATE,
    administered_by VARCHAR(100),
    batch_number VARCHAR(50),
    next_due_date DATE,
    status VARCHAR(20) NOT NULL CHECK (
        status IN ('Pending', 'Completed', 'Missed')
    ),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign Key
    CONSTRAINT fk_child
        FOREIGN KEY (child_id)
        REFERENCES child_profile(child_id)
        ON DELETE CASCADE,

    -- Optional reference to schedule
    CONSTRAINT fk_schedule
        FOREIGN KEY (vaccine_name, dose_number)
        REFERENCES vaccine_schedule(vaccine_name, dose_number)
        ON DELETE SET NULL
);

-- Indexes for performance
CREATE INDEX idx_vaccination_child 
ON vaccination_record (child_id);

CREATE INDEX idx_vaccination_status 
ON vaccination_record (status);

CREATE INDEX idx_vaccination_due 
ON vaccination_record (next_due_date);