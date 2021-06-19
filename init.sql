CREATE USER test_user with encrypted password '123';
CREATE DATABASE project_db;
GRANT ALL PRIVILEGES ON DATABASE project_db TO test_user;

\connect project_db;
CREATE EXTENSION IF NOT EXISTS timescaledb WITH SCHEMA public;
CREATE TABLE public.users_resource_stats (
    user_id real not null,
    resource_used integer not null,
    dt timestamp not null default now()
    );
CREATE INDEX ON users_resource_stats (user_id);
CREATE MATERIALIZED VIEW users_sum_stats AS
SELECT user_id, sum(resource_used) FROM users_resource_stats GROUP BY user_id;
CREATE UNIQUE INDEX ON users_sum_stats (user_id);
REFRESH MATERIALIZED VIEW concurrently users_sum_stats ;
