package redisstream

import (
    "context"
    "fmt"

    "github.com/redis/go-redis/v9"
)

func StartConsumer(
    client *redis.Client,
) {

    ctx := context.Background()

    for {

        streams, err := client.XRead(
            ctx,
            &redis.XReadArgs{
                Streams: []string{
                    "workflow-events",
                    "$",
                },
                Block: 0,
            },
        ).Result()

        if err != nil {
            continue
        }

        for _, stream := range streams {
            for _, msg := range stream.Messages {

                fmt.Println(
                    "received event:",
                    msg.Values,
                )
            }
        }
    }
}