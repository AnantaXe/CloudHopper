from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    dsn: str = Field(..., env="SYNC_POSTGRES_DSN")
    max_connections: int = Field(20, env="SYNC_POSTGRES_MAX_CONNECTIONS")
    schema: str = Field("sync_subsystem", env="SYNC_POSTGRES_SCHEMA")


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(..., env="SYNC_KAFKA_BOOTSTRAP_SERVERS")
    security_protocol: str = Field("PLAINTEXT", env="SYNC_KAFKA_SECURITY_PROTOCOL")
    client_id: str = Field("cloudhopper-sync", env="SYNC_KAFKA_CLIENT_ID")
    schema_registry_url: str | None = Field(None, env="SYNC_KAFKA_SCHEMA_REGISTRY_URL")
    group_id: str = Field("cloudhopper-sync-group", env="SYNC_KAFKA_GROUP_ID")
    retry_topic_suffix: str = Field(".retry", env="SYNC_KAFKA_RETRY_TOPIC_SUFFIX")
    dead_letter_topic_suffix: str = Field(".dlq", env="SYNC_KAFKA_DLQ_TOPIC_SUFFIX")


class TemporalSettings(BaseSettings):
    host: str = Field("localhost", env="SYNC_TEMPORAL_HOST")
    namespace: str = Field("default", env="SYNC_TEMPORAL_NAMESPACE")
    task_queue: str = Field("cloudhopper-sync-worker", env="SYNC_TEMPORAL_TASK_QUEUE")
    workflow_default_timeout_seconds: int = Field(900, env="SYNC_TEMPORAL_WORKFLOW_TIMEOUT")


class ObservabilitySettings(BaseSettings):
    otlp_endpoint: str | None = Field(None, env="SYNC_OTEL_EXPORTER_OTLP_ENDPOINT")
    prometheus_port: int = Field(9410, env="SYNC_PROMETHEUS_PORT")
    log_level: str = Field("INFO", env="SYNC_LOG_LEVEL")


class CDCSettings(BaseSettings):
    enabled: bool = Field(True, env="SYNC_CDC_ENABLED")
    debezium_connect_url: str = Field(..., env="SYNC_DEBEZIUM_CONNECT_URL")
    supported_sources: list[str] = Field(
        ["postgresql", "mysql", "sqlserver", "oracle", "mongodb"],
        env="SYNC_CDC_SUPPORTED_SOURCES",
    )
    max_lag_threshold_ms: int = Field(1000, env="SYNC_CDC_MAX_LAG_MS")


class SyncSettings(BaseSettings):
    environment: str = Field("dev", env="SYNC_ENVIRONMENT")
    tenant_namespace: str = Field("default", env="SYNC_TENANT_NAMESPACE")
    postgres: PostgresSettings = PostgresSettings()
    kafka: KafkaSettings = KafkaSettings()
    temporal: TemporalSettings = TemporalSettings()
    observability: ObservabilitySettings = ObservabilitySettings()
    cdc: CDCSettings = CDCSettings()

    class Config:
        env_prefix = "SYNC_"
        case_sensitive = False
