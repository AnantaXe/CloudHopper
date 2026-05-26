package domain

type TaskStatus string

const (
    TaskPending   TaskStatus = "PENDING"
    TaskRunning   TaskStatus = "RUNNING"
    TaskCompleted TaskStatus = "COMPLETED"
    TaskFailed    TaskStatus = "FAILED"
)

type Task struct {
    ID         string
    WorkflowID string
    WorkerType string
    Status     TaskStatus
    Payload    []byte
}