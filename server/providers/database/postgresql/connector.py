import asyncio
import psycopg

from agent_runtime.database.domain.model import (
    DatabaseAssessment,
    DatabaseEndpoint,
)

from providers.database.base import DatabaseProvider


class PostgreSQLProvider(DatabaseProvider):
    """PostgreSQL database provider implementation using psycopg."""

    def _connect(self, endpoint: DatabaseEndpoint):
        return psycopg.connect(
            host=endpoint.host,
            port=endpoint.port,
            user=endpoint.username,
            password=endpoint.password,
            dbname=endpoint.database_name,
            connect_timeout=10,
        )

    def _assess_database(
        self,
        endpoint: DatabaseEndpoint,
    ) -> DatabaseAssessment:

        conn = self._connect(endpoint)

        try:
            with conn.cursor() as cur:

                # Database size
                cur.execute(
                    """
                    SELECT pg_database_size(%s)
                    """,
                    (endpoint.database_name,),
                )
                database_size_bytes = cur.fetchone()[0]
                database_size_gb = database_size_bytes / (1024 ** 3)

                # PostgreSQL version
                cur.execute("SHOW server_version;")
                version = cur.fetchone()[0]

                # Tables
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = 'public';
                    """
                )
                table_count = cur.fetchone()[0]

                # Indexes
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM pg_indexes
                    WHERE schemaname = 'public';
                    """
                )
                index_count = cur.fetchone()[0]

                # Views
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM information_schema.views
                    WHERE table_schema = 'public';
                    """
                )
                view_count = cur.fetchone()[0]

                # Schemas
                cur.execute(
                    """
                    SELECT COUNT(DISTINCT table_schema)
                    FROM information_schema.tables;
                    """
                )
                schema_count = cur.fetchone()[0]

                # Stored procedures
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM information_schema.routines
                    WHERE routine_type = 'PROCEDURE';
                    """
                )
                stored_procedure_count = cur.fetchone()[0]

                # Functions
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM information_schema.routines
                    WHERE routine_type = 'FUNCTION';
                    """
                )
                function_count = cur.fetchone()[0]

                # Triggers
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM information_schema.triggers;
                    """
                )
                trigger_count = cur.fetchone()[0]

                # Foreign keys
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM information_schema.table_constraints
                    WHERE constraint_type = 'FOREIGN KEY';
                    """
                )
                foreign_key_count = cur.fetchone()[0]

                # Average connections
                cur.execute(
                    """
                    SELECT COALESCE(AVG(numbackends), 0)
                    FROM pg_stat_database;
                    """
                )
                avg_connections = cur.fetchone()[0]

                # Peak connections
                cur.execute(
                    """
                    SELECT COALESCE(MAX(numbackends), 0)
                    FROM pg_stat_database;
                    """
                )
                peak_connections = cur.fetchone()[0]

                # Extensions
                cur.execute(
                    """
                    SELECT extname
                    FROM pg_extension;
                    """
                )
                extensions = [row[0] for row in cur.fetchall()]

                # Buffer cache hit ratio
                cur.execute(
                    """
                    SELECT
                        COALESCE(
                            100.0 * SUM(blks_hit)
                            / NULLIF(SUM(blks_hit) + SUM(blks_read), 0),
                            0
                        )
                    FROM pg_stat_database;
                    """
                )
                cpu_percent = cur.fetchone()[0]

                # Database relation size ratio.
                #
                # This is not actually memory usage; PostgreSQL does not
                # expose database RAM usage through this query.
                cur.execute(
                    """
                    SELECT
                        COALESCE(
                            100.0 * SUM(pg_database_size(datname))
                            / NULLIF(
                                SUM(pg_database_size(datname))
                                + COALESCE(
                                    (
                                        SELECT SUM(pg_total_relation_size(c.oid))
                                        FROM pg_class c
                                        WHERE c.relkind IN ('r', 'm', 't')
                                    ),
                                    0
                                ),
                                0
                            ),
                            0
                        )
                    FROM pg_stat_database;
                    """
                )
                memory_percent = cur.fetchone()[0]

                # I/O counters
                cur.execute(
                    """
                    SELECT COALESCE(
                        SUM(blks_read + blks_hit),
                        0
                    )
                    FROM pg_stat_database;
                    """
                )
                iops = cur.fetchone()[0]

            return DatabaseAssessment(
                engine=endpoint.engine,
                version=version,
                database_size_gb=database_size_gb,
                schemas=schema_count,
                indexes=index_count,
                tables=table_count,
                views=view_count,
                stored_procedures=stored_procedure_count,
                functions=function_count,
                triggers=trigger_count,
                foreign_keys=foreign_key_count,
                extensions=extensions,
                avg_connections=int(avg_connections or 0),
                peak_connections=int(peak_connections or 0),
                cpu_percent=float(cpu_percent or 0),
                memory_percent=float(memory_percent or 0),
                iops=int(iops or 0),
            )

        finally:
            conn.close()

    async def assess_database(
        self,
        endpoint: DatabaseEndpoint,
    ) -> DatabaseAssessment:

        return await asyncio.to_thread(
            self._assess_database,
            endpoint,
        )

    def _test_connection(
        self,
        endpoint: DatabaseEndpoint,
    ) -> bool:

        conn = None

        try:
            conn = self._connect(endpoint)

            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()

            return result[0] == 1

        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

        finally:
            if conn is not None:
                conn.close()

    async def test_connection(
        self,
        endpoint: DatabaseEndpoint,
    ) -> bool:

        return await asyncio.to_thread(
            self._test_connection,
            endpoint,
        )

    async def discover_databases(
        self,
        token_id: str,
        endpoint: DatabaseEndpoint,
    ) -> list[DatabaseEndpoint]:

        return []

    def _get_schema(
        self,
        endpoint: DatabaseEndpoint,
    ) -> dict:

        conn = self._connect(endpoint)

        try:
            schema = {}

            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public';
                    """
                )

                tables = cur.fetchall()

                for (table_name,) in tables:

                    cur.execute(
                        """
                        SELECT column_name, data_type
                        FROM information_schema.columns
                        WHERE table_schema = 'public'
                        AND table_name = %s;
                        """,
                        (table_name,),
                    )

                    columns = cur.fetchall()

                    schema[table_name] = {
                        column_name: data_type
                        for column_name, data_type in columns
                    }

            return schema

        finally:
            conn.close()

    async def get_schema(
        self,
        endpoint: DatabaseEndpoint,
    ) -> dict:

        return await asyncio.to_thread(
            self._get_schema,
            endpoint,
        )

    def _get_replication_position(
        self,
        endpoint: DatabaseEndpoint,
    ) -> str:

        conn = self._connect(endpoint)

        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT pg_current_wal_lsn();"
                )

                return str(cur.fetchone()[0])

        finally:
            conn.close()

    async def get_replication_position(
        self,
        endpoint: DatabaseEndpoint,
    ) -> str:

        return await asyncio.to_thread(
            self._get_replication_position,
            endpoint,
        )

    def _freeze_writes(
        self,
        endpoint: DatabaseEndpoint,
    ) -> bool:

        conn = self._connect(endpoint)

        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT pg_start_backup('freeze_writes');"
                )

            conn.commit()
            return True

        except Exception as e:
            print(f"Failed to freeze writes: {e}")
            conn.rollback()
            return False

        finally:
            conn.close()

    async def freeze_writes(
        self,
        endpoint: DatabaseEndpoint,
    ) -> bool:

        return await asyncio.to_thread(
            self._freeze_writes,
            endpoint,
        )

    def _unfreeze_writes(
        self,
        endpoint: DatabaseEndpoint,
    ) -> bool:

        conn = self._connect(endpoint)

        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT pg_stop_backup();"
                )

            conn.commit()
            return True

        except Exception as e:
            print(f"Failed to unfreeze writes: {e}")
            conn.rollback()
            return False

        finally:
            conn.close()

    async def unfreeze_writes(
        self,
        endpoint: DatabaseEndpoint,
    ) -> bool:

        return await asyncio.to_thread(
            self._unfreeze_writes,
            endpoint,
        )

    async def health_check(
        self,
        endpoint: DatabaseEndpoint,
    ) -> bool:

        return await self.test_connection(endpoint)