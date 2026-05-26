package postgres

import (
    "context"

    "github.com/jackc/pgx/v5/pgxpool"

    "cloudhopper/control-plane/internal/domain"
)

type WorkflowRepository struct {
    db *pgxpool.Pool
}

func NewWorkflowRepository(
    db *pgxpool.Pool,
) *WorkflowRepository {
    return &WorkflowRepository{
        db: db,
    }
}

func (r *WorkflowRepository) SaveWorkflow(
    ctx context.Context,
    wf *domain.Workflow,
) error {

    query := `
    INSERT INTO workflows (
        id,
        type,
        state,
        payload,
        created_at,
        updated_at
    )
    VALUES ($1,$2,$3,$4,$5,$6)
    `

    _, err := r.db.Exec(
        ctx,
        query,
        wf.ID,
        wf.Type,
        wf.State,
        wf.Payload,
        wf.CreatedAt,
        wf.UpdatedAt,
    )

    return err
}