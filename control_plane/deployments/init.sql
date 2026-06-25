-- workflow --

CREATE TABLE workflows (
    id UUID PRIMARY KEY,
    type TEXT NOT NULL,
    state TEXT NOT NULL,
    payload BYTEA,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
