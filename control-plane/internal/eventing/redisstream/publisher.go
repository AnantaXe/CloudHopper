package redisstream

import (
    "context"
    "encoding/json"

    "github.com/redis/go-redis/v9"

    "cloudhopper/control-plane/internal/domain"
)

type Publisher struct {
    client *redis.Client
}

func NewPublisher(
    client *redis.Client,
) *Publisher {
    return &Publisher{
        client: client,
    }
}

func (p *Publisher) Publish(
    ctx context.Context,
    stream string,
    event *domain.Event,
) error {

    data, err := json.Marshal(event)
    if err != nil {
        return err
    }

    return p.client.XAdd(
        ctx,
        &redis.XAddArgs{
            Stream: stream,
            Values: map[string]interface{}{
                "event": string(data),
            },
        },
    ).Err()
}