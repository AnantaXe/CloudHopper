package orchestrator

import (
    "context"
    "time"

    "github.com/google/uuid"

    "cloudhopper/control-plane/internal/domain"
)

type Repository interface {
    SaveWorkflow(
        ctx context.Context,
        wf *domain.Workflow,
    ) error
}

type Publisher interface {
    Publish(
        ctx context.Context,
        stream string,
        event *domain.Event,
    ) error
}

type Service struct {
    repo      Repository
    publisher Publisher
}

func NewService(
    repo Repository,
    publisher Publisher,
) *Service {
    return &Service{
        repo: repo,
        publisher: publisher,
    }
}

func (s *Service) CreateWorkflow(
    ctx context.Context,
    workflowType string,
    payload []byte,
) (*domain.Workflow, error) {

    wf := &domain.Workflow{
        ID:        uuid.NewString(),
        Type:      workflowType,
        State:     domain.WorkflowCreated,
        Payload:   payload,
        CreatedAt: time.Now(),
        UpdatedAt: time.Now(),
    }

    if err := s.repo.SaveWorkflow(ctx, wf); err != nil {
        return nil, err
    }

    event := &domain.Event{
        ID:         uuid.NewString(),
        Type:       "WORKFLOW_CREATED",
        WorkflowID: wf.ID,
        Timestamp:  time.Now(),
    }

    if err := s.publisher.Publish(
        ctx,
        "workflow-events",
        event,
    ); err != nil {
        return nil, err
    }

    return wf, nil
}