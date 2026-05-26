package domain

import "time"

type WorkflowState string

const (
    WorkflowCreated WorkflowState = "CREATED"
    WorkflowRunning WorkflowState = "RUNNING"
    WorkflowFailed  WorkflowState = "FAILED"
    WorkflowDone    WorkflowState = "DONE"
)

type Workflow struct {
    ID        string
    Type      string
    State     WorkflowState
    Payload   []byte
    CreatedAt time.Time
    UpdatedAt time.Time
}