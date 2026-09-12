--
-- PostgreSQL database cluster dump
--

\restrict 7FDEZjQSb37sH968sU1dpVEmMOxXfdUXdzYWlaNaD0IuKMEtqFVMX5OvM0xkEsC

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE cloudhopper;
ALTER ROLE cloudhopper WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:HoS5JLXL2qhplmZv/46Nzg==$HRFkfh9hP7zvDo7oFBJU9ThNuIeex7QBa+ydluiCicY=:adtGwgMQJd28mk6Hs7VcYBEobtA1UBEg2Vh58BbbJLQ=';

--
-- User Configurations
--








\unrestrict 7FDEZjQSb37sH968sU1dpVEmMOxXfdUXdzYWlaNaD0IuKMEtqFVMX5OvM0xkEsC

--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

\restrict aROIWjN1ttpgQuv0nNXs6cFetdR5ba52FkGMJjmdjgsWBBS0UbrSWfRssKgR2Ad

-- Dumped from database version 16.15 (Debian 16.15-1.pgdg13+2)
-- Dumped by pg_dump version 18.1 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

\unrestrict aROIWjN1ttpgQuv0nNXs6cFetdR5ba52FkGMJjmdjgsWBBS0UbrSWfRssKgR2Ad

--
-- Database "cloudhopper" dump
--

--
-- PostgreSQL database dump
--

\restrict 8D47kJGtJH2x00QTcOEI1fdjUDxe63rZScwuBvOqFrxStkGxKlLDCtKKnj5ZFEC

-- Dumped from database version 16.15 (Debian 16.15-1.pgdg13+2)
-- Dumped by pg_dump version 18.1 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: cloudhopper; Type: DATABASE; Schema: -; Owner: cloudhopper
--

CREATE DATABASE cloudhopper WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE cloudhopper OWNER TO cloudhopper;

\unrestrict 8D47kJGtJH2x00QTcOEI1fdjUDxe63rZScwuBvOqFrxStkGxKlLDCtKKnj5ZFEC
\connect cloudhopper
\restrict 8D47kJGtJH2x00QTcOEI1fdjUDxe63rZScwuBvOqFrxStkGxKlLDCtKKnj5ZFEC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: refresh_tokens; Type: TABLE; Schema: public; Owner: cloudhopper
--

CREATE TABLE public.refresh_tokens (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    token_hash text NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    revoked boolean DEFAULT false NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.refresh_tokens OWNER TO cloudhopper;

--
-- Name: user_data; Type: TABLE; Schema: public; Owner: cloudhopper
--

CREATE TABLE public.user_data (
    user_id uuid NOT NULL,
    user_name text,
    user_password text
);


ALTER TABLE public.user_data OWNER TO cloudhopper;

--
-- Name: user_data1; Type: TABLE; Schema: public; Owner: cloudhopper
--

CREATE TABLE public.user_data1 (
    user_id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_name text,
    user_password text
);


ALTER TABLE public.user_data1 OWNER TO cloudhopper;

--
-- Name: users; Type: TABLE; Schema: public; Owner: cloudhopper
--

CREATE TABLE public.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash text NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    is_verified boolean DEFAULT false NOT NULL,
    failed_login_attempts integer DEFAULT 0 NOT NULL,
    account_locked_until timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.users OWNER TO cloudhopper;

--
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: cloudhopper
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- Name: user_data1 user_data1_pkey; Type: CONSTRAINT; Schema: public; Owner: cloudhopper
--

ALTER TABLE ONLY public.user_data1
    ADD CONSTRAINT user_data1_pkey PRIMARY KEY (user_id);


--
-- Name: user_data user_data_pkey; Type: CONSTRAINT; Schema: public; Owner: cloudhopper
--

ALTER TABLE ONLY public.user_data
    ADD CONSTRAINT user_data_pkey PRIMARY KEY (user_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: cloudhopper
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: cloudhopper
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: cloudhopper
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: idx_refresh_tokens_user_id; Type: INDEX; Schema: public; Owner: cloudhopper
--

CREATE INDEX idx_refresh_tokens_user_id ON public.refresh_tokens USING btree (user_id);


--
-- Name: refresh_tokens refresh_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cloudhopper
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 8D47kJGtJH2x00QTcOEI1fdjUDxe63rZScwuBvOqFrxStkGxKlLDCtKKnj5ZFEC

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

\restrict fHG6lFHfeTP9F4LassmQZc7ZdOZjcnBtlympP3eFpDdop4uZcs4xuSBGhor8mgv

-- Dumped from database version 16.15 (Debian 16.15-1.pgdg13+2)
-- Dumped by pg_dump version 18.1 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

\unrestrict fHG6lFHfeTP9F4LassmQZc7ZdOZjcnBtlympP3eFpDdop4uZcs4xuSBGhor8mgv

--
-- PostgreSQL database cluster dump complete
--

