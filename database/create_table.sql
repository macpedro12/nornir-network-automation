CREATE TABLE IF NOT EXISTS services (
    service_id DECIMAL NOT NULL,
    service_applied TEXT NOT NULL,
    service_name TEXT NOT NULL,
    applied_config TEXT,
    initial_config TEXT,
    status TEXT,
    date TIMESTAMP,
    PRIMARY KEY (service_id)
);

CREATE TABLE IF NOT EXISTS devices (
    hostname TEXT NOT NULL,
    ip TEXT NOT NULL,
    running_config TEXT,
    applied_services TEXT,
    status TEXT,
    PRIMARY KEY (hostname)
);