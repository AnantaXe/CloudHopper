import asyncpg

from agent_runtime.database.domain.model import (
    DatabaseAssessment,
    DatabaseEndpoint,
)

from providers.database.base import DatabaseProvider

class PostgreSQLProvider(DatabaseProvider):
    """PostgreSQL database provider implementation."""

    """For Production, remove password from the class and use a secure method to handle credentials, such as environment variables or a secrets manager."""

    async def assess_database(self, endpoint: DatabaseEndpoint) -> DatabaseAssessment:
        """Assess the PostgreSQL database and return a DatabaseAssessment object."""
        conn = await asyncpg.connect(
            user=endpoint.username,
            password=endpoint.password,
            database=endpoint.database_name,
            host=endpoint.host,
            port=endpoint.port,
        )
        try:
        
            result = await conn.fetchrow("SELECT pg_database_size($1) AS size", endpoint.database_name)
            database_size_gb = result["size"] / (1024 ** 3)  # Convert bytes to GB
            version = await conn.fetchval("SHOW server_version;")
            table_count = await conn.fetchval("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
            index_count = await conn.fetchval("SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public';")
            view_count = await conn.fetchval("SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'public';")
            schema_count = await conn.fetchval("SELECT COUNT(DISTINCT table_schema) FROM information_schema.tables;")
            stored_procedure_count = await conn.fetchval("SELECT COUNT(*) FROM information_schema.routines WHERE routine_type='PROCEDURE';")
            function_count = await conn.fetchval("SELECT COUNT(*) FROM information_schema.routines WHERE routine_type='FUNCTION';")
            trigger_count = await conn.fetchval("SELECT COUNT(*) FROM information_schema.triggers;")
            foreign_key_count = await conn.fetchval("SELECT COUNT(*) FROM information_schema.table_constraints WHERE constraint_type='FOREIGN KEY';")
            avg_connections = await conn.fetchval("SELECT avg(numbackends) FROM pg_stat_database;")
            peak_connections = await conn.fetchval("SELECT max(numbackends) FROM pg_stat_database;")
            extensions = await conn.fetch("SELECT extname FROM pg_extension;")
            cpu_percent = await conn.fetchval("SELECT (100 * sum(blks_hit) / nullif(sum(blks_hit) + sum(blks_read), 0)) AS hit_ratio FROM pg_stat_database;")
            memory_percent = await conn.fetchval("SELECT (100 * sum(pg_database_size(datname)) / nullif(sum(pg_database_size(datname)) + sum(pg_total_relation_size(relid)), 0)) AS memory_usage FROM pg_stat_database;")
            iops = await conn.fetchval("SELECT sum(blks_read + blks_hit) AS total_iops FROM pg_stat_database;")

            # Additional assessment metrics can be added here
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
                extensions=[ext['extname'] for ext in extensions],        
                avg_connections=avg_connections,    
                peak_connections=peak_connections,   
                cpu_percent=cpu_percent,      
                memory_percent=memory_percent,   
                iops=iops              
            )
        finally:
            await conn.close()


    async def test_connection(self, endpoint: DatabaseEndpoint) -> bool:
        """Test the PostgreSQL database connection and return True if successful, False otherwise."""
        try:
            conn = await asyncpg.connect(
                user=endpoint.username,
                password=endpoint.password,
                database=endpoint.database_name,
                host=endpoint.host,
                port=endpoint.port,
            )
            await conn.close()
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    async def discover_databases(self, token_id: str, endpoint: DatabaseEndpoint) -> list[DatabaseEndpoint]:
        pass


    async def get_schema(self, endpoint: DatabaseEndpoint) -> dict:

        conn = await asyncpg.connect(
            user=endpoint.username,
            password=endpoint.password,
            database=endpoint.database_name,
            host=endpoint.host,
            port=endpoint.port,
        )
        try: 
            schema = {}
            tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            for table in tables:
                table_name = table['table_name']
                columns = await conn.fetch(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';")
                schema[table_name] = {col['column_name']: col['data_type'] for col in columns}
            return schema
        finally:
            await conn.close()


    async def get_replication_position(self, endpoint: DatabaseEndpoint) -> str:
        conn = await asyncpg.connect(
            user=endpoint.username,
            password=endpoint.password,
            database=endpoint.database_name,
            host=endpoint.host,
            port=endpoint.port,
        )
        try:
            replication_position = await conn.fetchval("SELECT pg_current_wal_lsn();")
            return replication_position
        finally:
            await conn.close()


    async def freeze_writes(self, endpoint: DatabaseEndpoint) -> bool:
        conn = await asyncpg.connect(
            user=endpoint.username,
            password=endpoint.password,
            database=endpoint.database_name,
            host=endpoint.host,
            port=endpoint.port,
        )
        try:
            await conn.execute("SELECT pg_start_backup('freeze_writes');")
            return True
        except Exception as e:
            print(f"Failed to freeze writes: {e}")
            return False
        finally:
            await conn.close()

    async def unfreeze_writes(self, endpoint: DatabaseEndpoint) -> bool:
        conn = await asyncpg.connect(
            user=endpoint.username,
            password=endpoint.password,
            database=endpoint.database_name,
            host=endpoint.host,
            port=endpoint.port,
        )
        try:
            await conn.execute("SELECT pg_stop_backup();")
            return True
        except Exception as e:
            print(f"Failed to unfreeze writes: {e}")
            return False
        finally:
            await conn.close()

    async def health_check(self, endpoint: DatabaseEndpoint) -> bool:
        try:
            conn = await asyncpg.connect(
                user=endpoint.username,
                password=endpoint.password,
                database=endpoint.database_name,
                host=endpoint.host,
                port=endpoint.port,
            )
            await conn.close()
            return True
        except Exception as e:
            print(f"Health check failed: {e}")
            return False

        

        