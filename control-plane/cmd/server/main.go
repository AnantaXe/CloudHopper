package main

import (
    "context"
    "log"
    "net"

    "github.com/jackc/pgx/v5/pgxpool"
    "github.com/redis/go-redis/v9"

    "google.golang.org/grpc"

    workflowpb "cloudhopper/control-plane/proto/workflow"

    "cloudhopper/control-plane/internal/api"
    "cloudhopper/control-plane/internal/eventing/redisstream"
    "cloudhopper/control-plane/internal/orchestrator"
    "cloudhopper/control-plane/internal/storage/postgres"
)

func main() {

    ctx := context.Background()

    db, err := pgxpool.New(
        ctx,
        "postgres://cloudhopper:password@localhost:5432/cloudhopper",
    )

    if err != nil {
        log.Fatal(err)
    }

    redisClient := redis.NewClient(
        &redis.Options{
            Addr: "localhost:6379",
        },
    )

    repo := postgres.NewWorkflowRepository(db)

    publisher := redisstream.NewPublisher(
        redisClient,
    )

    orch := orchestrator.NewService(
        repo,
        publisher,
    )

    workflowServer := api.NewWorkflowServer(
        orch,
    )

    go redisstream.StartConsumer(redisClient)

    lis, err := net.Listen(
        "tcp",
        ":50051",
    )

    if err != nil {
        log.Fatal(err)
    }

    grpcServer := grpc.NewServer()

    workflowpb.RegisterWorkflowServiceServer(
        grpcServer,
        workflowServer,
    )

    log.Println(
        "control-plane running on :50051",
    )

    if err := grpcServer.Serve(lis); err != nil {
        log.Fatal(err)
    }
}