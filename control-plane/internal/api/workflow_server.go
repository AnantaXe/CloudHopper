package api

import (
    "context"

    workflowpb "cloudhopper/control-plane/proto/workflow"

    "cloudhopper/control-plane/internal/orchestrator"
)

type WorkflowServer struct {
    workflowpb.UnimplementedWorkflowServiceServer

    orchestrator *orchestrator.Service
}

func NewWorkflowServer(
    orchestrator *orchestrator.Service,
) *WorkflowServer {

    return &WorkflowServer{
        orchestrator: orchestrator,
    }
}

func (s *WorkflowServer) CreateWorkflow(
    ctx context.Context,
    req *workflowpb.CreateWorkflowRequest,
) (*workflowpb.CreateWorkflowResponse, error) {

    wf, err := s.orchestrator.CreateWorkflow(
        ctx,
        req.Type,
        req.Payload,
    )

    if err != nil {
        return nil, err
    }

    return &workflowpb.CreateWorkflowResponse{
        WorkflowId: wf.ID,
        Status:     string(wf.State),
    }, nil
}