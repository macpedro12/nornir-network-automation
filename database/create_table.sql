CREATE TABLE IF NOT EXISTS service (
    service_id INT NOT NULL,
    service_name TEXT NOT NULL,
    applied_config TEXT,
    initial_config TEXT,
    status TEXT,
    PRIMARY KEY (service_id)
);