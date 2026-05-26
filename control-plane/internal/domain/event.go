package domain

import "time"

type Event struct {
    ID         string
    Type       string
    WorkflowID string
    Payload    []byte
    Timestamp  time.Time
}