SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- \restrict gtLofk5iLw18PvbELsO4WEZXAXehtrkLXaecyFgguCoaWEzCMyKIVZRqMEHzYSP

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

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
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."audit_log_entries" ("instance_id", "id", "payload", "created_at", "ip_address") VALUES
	('00000000-0000-0000-0000-000000000000', 'ddba1bc0-8efc-4493-aefb-ff3d4bf52fbc', '{"action":"user_confirmation_requested","actor_id":"77c7f38a-84ae-4eb8-a8e5-22eccfcda790","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"user","traits":{"provider":"email"}}', '2025-10-26 13:00:42.665487+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e261e118-2ab2-468e-9743-a4294ca84866', '{"action":"user_deleted","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"user_email":"test@jayd.ai","user_id":"77c7f38a-84ae-4eb8-a8e5-22eccfcda790","user_phone":""}}', '2025-10-26 13:03:58.737676+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e218a916-a04f-4e61-a730-f8ca14e5ae1c', '{"action":"user_signedup","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"team","traits":{"provider":"email"}}', '2025-10-27 09:20:24.305665+00', ''),
	('00000000-0000-0000-0000-000000000000', 'f0f09b30-8efd-4a31-8946-d6b5de7cebf1', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 09:20:24.314399+00', ''),
	('00000000-0000-0000-0000-000000000000', '3cb19ebd-d31e-465c-9c5a-d3c8274923d2', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 09:28:57.752625+00', ''),
	('00000000-0000-0000-0000-000000000000', '74f6f0e4-f187-4941-bafb-b8e09b439778', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 09:32:01.955865+00', ''),
	('00000000-0000-0000-0000-000000000000', '8fee7b5a-da87-4be5-90c1-8c91b8a688d4', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 09:32:37.287314+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b55a5ee2-df9d-4121-87f8-5effb5d9dc90', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 09:34:02.187192+00', ''),
	('00000000-0000-0000-0000-000000000000', 'adf24f2a-31fa-40f9-8a72-b59d87721c6c', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 09:37:07.273718+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a82728ab-9cec-4f0e-8d37-ccac69f912e1', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 09:41:01.805583+00', ''),
	('00000000-0000-0000-0000-000000000000', '8f0b1650-9518-4e97-8a3f-b3b876ef454d', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 11:44:31.999207+00', ''),
	('00000000-0000-0000-0000-000000000000', 'd2e7c0a9-4488-439e-a1be-3e8cf9ceb7c4', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 11:46:16.909836+00', ''),
	('00000000-0000-0000-0000-000000000000', '26e389f4-ece2-4d21-b433-9a128b81c891', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 16:25:37.918545+00', ''),
	('00000000-0000-0000-0000-000000000000', '8e47b8d4-b56d-4bbd-a65b-2ba4ede92165', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 16:25:50.658565+00', ''),
	('00000000-0000-0000-0000-000000000000', '574cd7d7-4f1e-4d5d-997d-bd127d211a40', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 17:50:53.941139+00', ''),
	('00000000-0000-0000-0000-000000000000', 'd08b9e08-f9d0-499c-a45c-0c04eff8f086', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 17:52:06.659002+00', ''),
	('00000000-0000-0000-0000-000000000000', '6f0fb93e-6f0e-45dd-93f0-e9986c4a26c0', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 17:56:34.832433+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b3d1eddd-ae3b-40de-96c6-19e167b35b3d', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 17:57:17.297957+00', ''),
	('00000000-0000-0000-0000-000000000000', '359fd2a9-055d-49dd-a8c1-959dc2a489a7', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 18:00:49.771028+00', ''),
	('00000000-0000-0000-0000-000000000000', '9fd32cba-73f0-4df5-9e2b-da295fcacd5d', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 19:18:42.206774+00', ''),
	('00000000-0000-0000-0000-000000000000', '5d5de28d-b7db-407f-a19f-91683a97c09a', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 19:19:01.607567+00', ''),
	('00000000-0000-0000-0000-000000000000', '943f9a94-5111-42a4-8416-5e815dbb18a1', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 19:19:30.85723+00', ''),
	('00000000-0000-0000-0000-000000000000', '8a1b17d7-2488-4570-b1e1-42b680363cb8', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 20:45:55.964368+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a3a5f4a1-a50e-49c6-98be-b13d5906c7a5', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 20:46:30.241345+00', ''),
	('00000000-0000-0000-0000-000000000000', '1a5978dc-ddcd-4948-a275-0918eafbfe3f', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 20:47:01.515165+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e820dc2e-9ff3-4a9e-8dce-b5c3cdb929ca', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 22:33:48.350151+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e82b53d7-c144-4386-a5c9-acc060b1ba7b', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 22:35:14.071944+00', ''),
	('00000000-0000-0000-0000-000000000000', '966e7800-b2a7-4704-87f3-91d62bc2426e', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-27 22:36:03.941399+00', ''),
	('00000000-0000-0000-0000-000000000000', '4035d295-d166-48de-9909-1ee177ab599b', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-10-28 14:09:09.37567+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e6da2841-cc75-4874-9709-2eacb99148d3', '{"action":"token_refreshed","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-10-28 16:36:43.417983+00', ''),
	('00000000-0000-0000-0000-000000000000', '9d845960-f27d-40d2-8225-1c3d1e380ab2', '{"action":"token_revoked","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-10-28 16:36:43.444835+00', ''),
	('00000000-0000-0000-0000-000000000000', 'cb55b849-a875-4f66-9c55-d3bb15ceea93', '{"action":"token_refreshed","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-10-28 16:36:43.639851+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b6bbcfce-59d6-4c4f-a52f-243072b5f898', '{"action":"login","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-11-05 09:15:31.308377+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e9c42db1-5126-421d-b161-cb920a823ae6', '{"action":"token_refreshed","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-05 13:59:31.341843+00', ''),
	('00000000-0000-0000-0000-000000000000', '4de37056-fb4e-4a25-9cab-86480d162c1d', '{"action":"token_revoked","actor_id":"51eee0a1-8f20-4403-b5f1-0566375db20b","actor_username":"test@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-05 13:59:31.351347+00', ''),
	('00000000-0000-0000-0000-000000000000', '2604a51e-c384-4573-8daf-6977d3c0ba34', '{"action":"user_signedup","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"team","traits":{"provider":"email"}}', '2025-11-05 15:08:36.626008+00', ''),
	('00000000-0000-0000-0000-000000000000', 'baa682e3-499c-40d0-b82e-65338ee0d3af', '{"action":"login","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-11-05 15:08:36.647112+00', ''),
	('00000000-0000-0000-0000-000000000000', 'f4dabe3c-1c29-4c97-83a8-3218f7c0fb6e', '{"action":"login","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-11-05 16:16:59.711764+00', ''),
	('00000000-0000-0000-0000-000000000000', '4fb4b2ae-79b5-45b5-b256-a4635eb7ac52', '{"action":"login","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-11-05 16:29:15.7499+00', ''),
	('00000000-0000-0000-0000-000000000000', '11a4dbfc-a2a1-4e54-b618-0cb3a66e9881', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-05 22:12:23.470907+00', ''),
	('00000000-0000-0000-0000-000000000000', '73a7448c-c54a-40fe-b7b2-a2a74e4ca957', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-05 22:12:23.491246+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b7c34684-d23a-4947-bd9d-e7294a587c3e', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-05 22:12:23.736303+00', ''),
	('00000000-0000-0000-0000-000000000000', 'c3915ec1-5ba7-46d6-8973-d1b387338bad', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-05 22:12:23.819482+00', ''),
	('00000000-0000-0000-0000-000000000000', 'defa3474-6d1d-48bb-a20f-01c31740a923', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 08:01:45.659748+00', ''),
	('00000000-0000-0000-0000-000000000000', '99da73d2-3efb-4f47-bd0c-1664b6184cc8', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 08:01:45.68374+00', ''),
	('00000000-0000-0000-0000-000000000000', 'dc634dc1-ffbb-4565-9ccc-abd6afb08886', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 08:01:46.013223+00', ''),
	('00000000-0000-0000-0000-000000000000', '2cdc2f93-c6b1-4104-81a7-2e02c60669d3', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 08:01:46.10454+00', ''),
	('00000000-0000-0000-0000-000000000000', '5c37f193-0c24-4e42-af08-272ef41264d3', '{"action":"login","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-11-06 08:46:26.172515+00', ''),
	('00000000-0000-0000-0000-000000000000', 'ba514e20-c9b5-41cc-a1d5-890a371f41e3', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 09:24:34.812363+00', ''),
	('00000000-0000-0000-0000-000000000000', 'bef83a12-f64b-4cbd-a700-546752131d4e', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 09:24:34.832554+00', ''),
	('00000000-0000-0000-0000-000000000000', '25ce50b6-b816-44b3-afb2-97593c85bc8b', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 09:24:35.289548+00', ''),
	('00000000-0000-0000-0000-000000000000', '68cdc889-a9a3-4c48-95da-916cb102bd6f', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 09:24:35.367461+00', ''),
	('00000000-0000-0000-0000-000000000000', '7bf8ef9d-dea7-477f-b877-6bc4327189db', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 09:41:27.619698+00', ''),
	('00000000-0000-0000-0000-000000000000', 'c8688d81-875d-46bb-aa74-d98ac51ad235', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 09:41:27.642857+00', ''),
	('00000000-0000-0000-0000-000000000000', '23b629c5-9f19-4f4b-90b0-a3425040f224', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 10:22:27.624543+00', ''),
	('00000000-0000-0000-0000-000000000000', '6caf0e80-7f02-463c-8c52-80d541b65d5d', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 10:22:27.639609+00', ''),
	('00000000-0000-0000-0000-000000000000', '3f8c2be2-0ed6-41e2-83bf-335ea1bace8f', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 10:36:28.637535+00', ''),
	('00000000-0000-0000-0000-000000000000', '748d3db0-1ded-4750-a49b-3d269c8cab14', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 10:36:28.64977+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a56bd507-de39-438a-938f-0e4220d24f7d', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 12:28:34.564645+00', ''),
	('00000000-0000-0000-0000-000000000000', '5395f9b8-5eb6-4e72-a7df-cd8a269b5b02', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 12:28:34.590847+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b6dc9c4d-c3ec-43f5-ad89-061ad59912bb', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 12:29:20.777083+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b381c989-baed-496b-a8df-6db6e5bd5f60', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 12:29:20.778445+00', ''),
	('00000000-0000-0000-0000-000000000000', '6e637c21-82e0-42a6-9fee-ec9f5c2a0c01', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 12:29:20.872072+00', ''),
	('00000000-0000-0000-0000-000000000000', 'cbeef933-a853-44ad-8e06-04a66495f9ff', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 12:29:21.643879+00', ''),
	('00000000-0000-0000-0000-000000000000', 'cc6eec74-e395-460a-9d4b-d40e2e2e8e2a', '{"action":"login","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-11-06 12:51:57.323066+00', ''),
	('00000000-0000-0000-0000-000000000000', 'd3ec5e4f-d138-4fb0-a824-ff166364c407', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 13:46:59.039969+00', ''),
	('00000000-0000-0000-0000-000000000000', '51b675fb-df07-405a-91d3-f68f027fee9e', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 13:46:59.062841+00', ''),
	('00000000-0000-0000-0000-000000000000', '6b51f673-f518-48b2-a8db-431d59e8abbc', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 14:16:33.305418+00', ''),
	('00000000-0000-0000-0000-000000000000', 'ff8293a2-6e2f-4024-b61d-cbf985d39ef4', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 14:16:33.323864+00', ''),
	('00000000-0000-0000-0000-000000000000', '64d08a22-19ce-46df-b6dd-fb2b0a2fc8c5', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 14:16:33.437516+00', ''),
	('00000000-0000-0000-0000-000000000000', '34cf7256-f3a8-4bf1-a262-080b318e6947', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 14:16:34.233334+00', ''),
	('00000000-0000-0000-0000-000000000000', '1861aaee-2b94-46ac-a1c6-cebab6ffe25a', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 14:42:00.73329+00', ''),
	('00000000-0000-0000-0000-000000000000', '6129edf7-0805-4ecf-b9f3-5f9d37a48c52', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 14:42:00.755979+00', ''),
	('00000000-0000-0000-0000-000000000000', 'f6f94d4f-545d-4026-8f7d-5802cd4dd80e', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 15:19:59.924732+00', ''),
	('00000000-0000-0000-0000-000000000000', '5169972b-a912-433d-bccf-56f266c860f3', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 15:19:59.95017+00', ''),
	('00000000-0000-0000-0000-000000000000', '48e751b1-4219-4c23-a48b-c4d82d1cd71a', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 15:20:00.099711+00', ''),
	('00000000-0000-0000-0000-000000000000', 'dc41fab8-8459-415b-ba86-b3b42114131d', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 15:37:01.756211+00', ''),
	('00000000-0000-0000-0000-000000000000', '69d8518b-eed4-420c-a4a7-13d318bd76e6', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 15:37:01.765852+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a26800d9-0f0d-4d83-a567-ce94e737ed27', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 16:24:19.356576+00', ''),
	('00000000-0000-0000-0000-000000000000', '6680b7c1-4edf-4fa8-a0d8-1d16ee3aa45f', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 16:24:19.380798+00', ''),
	('00000000-0000-0000-0000-000000000000', '94bd0bd7-03e0-4ff5-89db-47c0cb33aeaf', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 16:24:20.280049+00', ''),
	('00000000-0000-0000-0000-000000000000', '6ddd1c63-7559-402c-b56e-ddc6a6421297', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 16:32:02.794689+00', ''),
	('00000000-0000-0000-0000-000000000000', '2763a8c3-9363-48ff-9c2a-5915570947c6', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 16:32:02.796852+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b44e8e23-c0b5-4120-8dad-baa3e9719b4a', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 17:19:24.479309+00', ''),
	('00000000-0000-0000-0000-000000000000', '37e77a72-083b-46b0-b8b6-738664fb5827', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 17:19:24.496889+00', ''),
	('00000000-0000-0000-0000-000000000000', '4d72ea47-6dcd-4de0-8462-735d8612d16a', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 17:27:08.123732+00', ''),
	('00000000-0000-0000-0000-000000000000', 'c38070c8-0a03-44f8-ac78-b6c00f45ae78', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 17:27:08.13994+00', ''),
	('00000000-0000-0000-0000-000000000000', '69bcb129-d6f5-4291-ae8e-96725c756a59', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 21:17:05.837205+00', ''),
	('00000000-0000-0000-0000-000000000000', '836686dc-6515-4891-b9c5-62ed0e17a5f4', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-06 21:17:05.856384+00', ''),
	('00000000-0000-0000-0000-000000000000', '3e1e2e5e-4864-47fa-bf44-a160b31b0a78', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-07 08:02:09.881008+00', ''),
	('00000000-0000-0000-0000-000000000000', '79c6e274-1dca-451c-a920-686d1cd07c14', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-07 08:02:09.902671+00', ''),
	('00000000-0000-0000-0000-000000000000', 'de83c184-3640-4d72-be2b-491dfe6b4e66', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-07 08:25:47.2665+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a44e1bf6-6779-4805-b0f7-d0c995724edd', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-07 08:25:47.292458+00', ''),
	('00000000-0000-0000-0000-000000000000', '83a00f4f-17b9-4e93-836a-b5b5ed377d05', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-07 08:25:47.428921+00', ''),
	('00000000-0000-0000-0000-000000000000', 'ed5df914-02e5-448c-9a83-a111d05e5f9f', '{"action":"user_signedup","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"team","traits":{"provider":"email"}}', '2025-11-09 22:29:52.278643+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e761a212-13ac-4c74-94e5-23af78d3e3e1', '{"action":"login","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-11-09 22:29:52.297382+00', ''),
	('00000000-0000-0000-0000-000000000000', '198829d8-ea04-49d6-825b-8c4178e5b1ba', '{"action":"token_refreshed","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 09:08:13.406685+00', ''),
	('00000000-0000-0000-0000-000000000000', '5b657f10-1348-453a-af9f-75f23ab163dc', '{"action":"token_revoked","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 09:08:13.431888+00', ''),
	('00000000-0000-0000-0000-000000000000', '8e5e00cd-13ee-40f9-8a0a-d0a43228ef8d', '{"action":"token_refreshed","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 10:03:13.775314+00', ''),
	('00000000-0000-0000-0000-000000000000', '237b9a86-8bee-4e04-bbf1-297e5fa7d78a', '{"action":"token_revoked","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 10:03:13.788699+00', ''),
	('00000000-0000-0000-0000-000000000000', 'f04006e6-d85b-4575-8b3a-659646d04781', '{"action":"token_refreshed","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 11:10:25.012826+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e6d50b65-2098-4dcb-ae7e-3e60db3ab075', '{"action":"token_revoked","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 11:10:25.024571+00', ''),
	('00000000-0000-0000-0000-000000000000', '8d41a564-5582-45e0-b842-cc0cdb1c4746', '{"action":"user_repeated_signup","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"user","traits":{"provider":"email"}}', '2025-11-10 11:32:08.095158+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a77cfb54-ccb4-45ad-862a-685d1da4d794', '{"action":"login","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2025-11-10 11:32:57.666347+00', ''),
	('00000000-0000-0000-0000-000000000000', 'cf61f62f-cd4d-4151-8c41-04be2e0d0b1f', '{"action":"token_refreshed","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 12:09:29.793929+00', ''),
	('00000000-0000-0000-0000-000000000000', 'eab310b5-d616-40e1-a10c-3510d821e28d', '{"action":"token_revoked","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 12:09:29.825201+00', ''),
	('00000000-0000-0000-0000-000000000000', '7586f8ca-2344-4f4b-9b6f-668380dc89ec', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 12:13:37.351706+00', ''),
	('00000000-0000-0000-0000-000000000000', 'ec5577a6-ee65-4180-a0b1-2479bfb9aada', '{"action":"token_revoked","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 12:13:37.356004+00', ''),
	('00000000-0000-0000-0000-000000000000', '750bb96d-340f-4565-97ab-c9efa9c54636', '{"action":"token_refreshed","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 12:13:37.470576+00', ''),
	('00000000-0000-0000-0000-000000000000', '1b4d819a-db74-4a38-8dab-ed16113ad757', '{"action":"token_refreshed","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 13:09:01.936534+00', ''),
	('00000000-0000-0000-0000-000000000000', '4f602864-e985-4be9-9ff0-5576c58190e1', '{"action":"token_revoked","actor_id":"eff2a1fd-210c-4b44-9a6f-81af6534c3c8","actor_username":"quentin+1@jayd.ai","actor_via_sso":false,"log_type":"token"}', '2025-11-10 13:09:01.942902+00', ''),
	('00000000-0000-0000-0000-000000000000', 'd2dcc30e-f09b-4e20-891b-2d7557e82bb4', '{"action":"user_repeated_signup","actor_id":"478b7491-ff6c-490b-982c-a4dc866dcefc","actor_username":"vincent@jayd.ai","actor_via_sso":false,"log_type":"user","traits":{"provider":"email"}}', '2025-11-10 13:09:21.874416+00', '');


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."users" ("instance_id", "id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "invited_at", "confirmation_token", "confirmation_sent_at", "recovery_token", "recovery_sent_at", "email_change_token_new", "email_change", "email_change_sent_at", "last_sign_in_at", "raw_app_meta_data", "raw_user_meta_data", "is_super_admin", "created_at", "updated_at", "phone", "phone_confirmed_at", "phone_change", "phone_change_token", "phone_change_sent_at", "email_change_token_current", "email_change_confirm_status", "banned_until", "reauthentication_token", "reauthentication_sent_at", "is_sso_user", "deleted_at", "is_anonymous") VALUES
	('00000000-0000-0000-0000-000000000000', '0eaa7f45-1f7e-403b-84fc-f02d0f0e18a4', 'authenticated', 'authenticated', 'arthur@jayd.ai', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2024-12-05 16:08:02.088+00', '{"provider": "google", "providers": ["google"]}', '{"hd": "jayd.ai", "sub": "113451562904096463359", "name": "Arthur Bricout", "email": "arthur@jayd.ai", "picture": "https://lh3.googleusercontent.com/a/.../s96-c/photo.jpg", "given_name": "Arthur", "family_name": "Bricout", "email_verified": true}', false, '2024-12-05 16:07:59.785+00', '2025-01-07 14:17:08.394+00', NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'authenticated', 'authenticated', 'jean-baptiste@jayd.ai', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2024-12-05 16:13:36.023+00', '{"provider": "google", "providers": ["google"]}', '{"hd": "jayd.ai", "sub": "116884903631491222905", "name": "Jean-Baptiste", "email": "jean-baptiste@jayd.ai", "picture": "https://lh3.googleusercontent.com/a/.../s96-c/photo.jpg", "given_name": "Jean-Baptiste", "family_name": "", "email_verified": true}', false, '2024-12-05 16:13:34.624+00', '2024-12-05 16:13:36.025+00', NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'authenticated', 'authenticated', 'jean-baptiste+2@jayd.ai', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2024-12-05 16:36:53.874+00', '{"provider": "google", "providers": ["google"]}', '{"hd": "jayd.ai", "sub": "111282921288593876694", "name": "Jean-Baptiste", "email": "jean-baptiste+2@jayd.ai", "picture": "https://lh3.googleusercontent.com/a/.../s96-c/photo.jpg", "given_name": "Jean-Baptiste", "family_name": "", "email_verified": true}', false, '2024-12-05 16:36:52.386+00', '2025-06-05 10:53:39.257+00', NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 'authenticated', 'authenticated', 'quentin@jayd.ai', NULL, '2024-12-05 16:05:11.317+00', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-30 11:36:24.318+00', '{"provider": "email", "providers": ["email", "google"]}', '{"email": "quentin@jayd.ai"}', false, '2024-12-05 16:05:11.315+00', '2025-07-30 15:06:04.577+00', NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', '478b7491-ff6c-490b-982c-a4dc866dcefc', 'authenticated', 'authenticated', 'vincent@jayd.ai', '$2a$10$8yu9ablgdUc1NLHfIYPPPOIjul2vMpcXbTF3pGE3etdS3SeMC827y', '2025-11-05 15:08:36.634051+00', NULL, '', NULL, '', NULL, '', '', NULL, '2025-11-10 11:32:57.668989+00', '{"provider": "email", "providers": ["email"]}', '{"sub": "478b7491-ff6c-490b-982c-a4dc866dcefc", "name": "vincent barbier", "email": "vincent@jayd.ai", "origin": "webapp", "email_verified": true, "phone_verified": false}', NULL, '2025-11-05 15:08:36.572904+00', '2025-11-10 12:13:37.363054+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', 'eff2a1fd-210c-4b44-9a6f-81af6534c3c8', 'authenticated', 'authenticated', 'quentin+1@jayd.ai', '$2a$10$KeE2ESPmPBbPavfB6jkjT.b3AMS82NSjnami8ozwcSY/V9t54lOQu', '2025-11-09 22:29:52.285598+00', NULL, '', NULL, '', NULL, '', '', NULL, '2025-11-09 22:29:52.297999+00', '{"provider": "email", "providers": ["email"]}', '{"sub": "eff2a1fd-210c-4b44-9a6f-81af6534c3c8", "name": "Quentin Bragard", "email": "quentin+1@jayd.ai", "origin": "webapp", "email_verified": true, "phone_verified": false}', NULL, '2025-11-09 22:29:52.221988+00', '2025-11-10 13:09:01.954032+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', '51eee0a1-8f20-4403-b5f1-0566375db20b', 'authenticated', 'authenticated', 'test@jayd.ai', '$2a$10$Dd3Ba6R0TsaAxUXPKhOp/OEiNfF.hwK1cXBtWd3oZGy1Cm0bOwjo6', '2025-10-27 09:20:24.307179+00', NULL, '', NULL, '', NULL, '', '', NULL, '2025-11-05 09:15:31.339328+00', '{"provider": "email", "providers": ["email"]}', '{"sub": "51eee0a1-8f20-4403-b5f1-0566375db20b", "name": "Testing Account Jaydai", "email": "test@jayd.ai", "origin": "extension", "email_verified": true, "phone_verified": false}', NULL, '2025-10-27 09:20:24.297032+00', '2025-11-05 13:59:31.370202+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false);


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."identities" ("provider_id", "user_id", "identity_data", "provider", "last_sign_in_at", "created_at", "updated_at", "id") VALUES
	('51eee0a1-8f20-4403-b5f1-0566375db20b', '51eee0a1-8f20-4403-b5f1-0566375db20b', '{"sub": "51eee0a1-8f20-4403-b5f1-0566375db20b", "name": "Testing Account Jaydai", "email": "test@jayd.ai", "origin": "extension", "email_verified": false, "phone_verified": false}', 'email', '2025-10-27 09:20:24.302691+00', '2025-10-27 09:20:24.302743+00', '2025-10-27 09:20:24.302743+00', '1df81057-da84-4548-ba1b-2f75e9fa9e64'),
	('478b7491-ff6c-490b-982c-a4dc866dcefc', '478b7491-ff6c-490b-982c-a4dc866dcefc', '{"sub": "478b7491-ff6c-490b-982c-a4dc866dcefc", "name": "vincent barbier", "email": "vincent@jayd.ai", "origin": "webapp", "email_verified": false, "phone_verified": false}', 'email', '2025-11-05 15:08:36.614064+00', '2025-11-05 15:08:36.614118+00', '2025-11-05 15:08:36.614118+00', '834bb9cd-99ea-43b9-85c8-aed1c5920439'),
	('eff2a1fd-210c-4b44-9a6f-81af6534c3c8', 'eff2a1fd-210c-4b44-9a6f-81af6534c3c8', '{"sub": "eff2a1fd-210c-4b44-9a6f-81af6534c3c8", "name": "Quentin Bragard", "email": "quentin+1@jayd.ai", "origin": "webapp", "email_verified": false, "phone_verified": false}', 'email', '2025-11-09 22:29:52.26125+00', '2025-11-09 22:29:52.261709+00', '2025-11-09 22:29:52.261709+00', '8d6248c3-438c-4a8f-ad41-a4ff7d0fbd0c');


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: oauth_clients; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."sessions" ("id", "user_id", "created_at", "updated_at", "factor_id", "aal", "not_after", "refreshed_at", "user_agent", "ip", "tag", "oauth_client_id", "refresh_token_hmac_key", "refresh_token_counter") VALUES
	('8aea9a19-1d35-48ad-be74-510cb01bc3ac', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 09:20:24.31509+00', '2025-10-27 09:20:24.31509+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('642cb5a6-9086-4334-967e-f74b5c151124', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 09:28:57.762932+00', '2025-10-27 09:28:57.762932+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('a163fe55-df1f-4ef3-bd2b-60b0c060252a', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 09:32:01.957579+00', '2025-10-27 09:32:01.957579+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('11d5532b-0847-4fc9-869e-aa6e6df27828', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 09:32:37.28891+00', '2025-10-27 09:32:37.28891+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('834c7d9b-87b4-4786-a715-abc4b2cd807e', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 09:34:02.20382+00', '2025-10-27 09:34:02.20382+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('49939e2f-97d8-4b84-985c-4fd629e82cae', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 09:37:07.275065+00', '2025-10-27 09:37:07.275065+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('b742faeb-f9ff-412e-a695-a59d756efc04', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 09:41:01.806768+00', '2025-10-27 09:41:01.806768+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('3a9273f1-87f1-45d0-81e3-e834580cdf1f', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 11:44:32.018525+00', '2025-10-27 11:44:32.018525+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('c7becc29-a278-46b8-a2be-5e957e72ef18', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 11:46:16.911637+00', '2025-10-27 11:46:16.911637+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('973583d4-4aef-4530-b45f-b7f48497c108', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 16:25:37.946665+00', '2025-10-27 16:25:37.946665+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('d0e29fa6-51a0-499d-aa6c-0513bee7e5b3', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 16:25:50.66136+00', '2025-10-27 16:25:50.66136+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('17270fc1-3ef5-4918-8231-2584f755fcb5', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 17:50:53.970228+00', '2025-10-27 17:50:53.970228+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('e5aaa2fb-4ae5-4bc0-b15f-6681a51a23f0', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 17:52:06.66011+00', '2025-10-27 17:52:06.66011+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('990ceb39-d908-4c87-b1ab-78aaa2c4bb4c', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 17:56:34.843702+00', '2025-10-27 17:56:34.843702+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('7356b6d1-cb6c-41e6-8640-5a5f61f91f3a', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 17:57:17.299285+00', '2025-10-27 17:57:17.299285+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('4f4efa39-863a-4bbe-bfd0-5b8d903ec4d1', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 18:00:49.773973+00', '2025-10-27 18:00:49.773973+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('099fef53-3e30-49f1-9486-1127e197c929', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 19:18:42.235608+00', '2025-10-27 19:18:42.235608+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('60285b31-099d-431a-b2c7-1412224bfa15', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 19:19:01.609085+00', '2025-10-27 19:19:01.609085+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('19f1618c-bb7c-4513-ab60-048c5cf929e6', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 19:19:30.85841+00', '2025-10-27 19:19:30.85841+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.41.55', NULL, NULL, NULL, NULL),
	('7854db8f-dbac-4235-9134-809065c2cd2d', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 20:45:55.98727+00', '2025-10-27 20:45:55.98727+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.62.19', NULL, NULL, NULL, NULL),
	('ffeb3960-0df5-4d9f-a47e-556eb0fa449f', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 20:46:30.242483+00', '2025-10-27 20:46:30.242483+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.62.58', NULL, NULL, NULL, NULL),
	('2e6ddfc8-1b1f-46a8-bf9d-b5aebf650492', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 20:47:01.523995+00', '2025-10-27 20:47:01.523995+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.62.58', NULL, NULL, NULL, NULL),
	('7ffa088d-d1fc-40d8-8894-d9c59af522bf', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 22:33:48.37278+00', '2025-10-27 22:33:48.37278+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.62.94', NULL, NULL, NULL, NULL),
	('9a074506-26bb-4c25-bc88-d021e59076d4', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 22:35:14.080674+00', '2025-10-27 22:35:14.080674+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.62.94', NULL, NULL, NULL, NULL),
	('9f480a46-7622-46a5-9c5b-c86d99511194', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-27 22:36:03.943531+00', '2025-10-27 22:36:03.943531+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '34.96.62.94', NULL, NULL, NULL, NULL),
	('20fdafb4-06fb-439e-b995-2a1ae544f24a', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-10-28 14:09:09.402672+00', '2025-10-28 16:36:43.644552+00', NULL, 'aal1', NULL, '2025-10-28 16:36:43.644462', 'python-httpx/0.28.1', '34.96.62.94', NULL, NULL, NULL, NULL),
	('b637cb70-f39a-4bd4-b546-d8c10af3c522', '51eee0a1-8f20-4403-b5f1-0566375db20b', '2025-11-05 09:15:31.339425+00', '2025-11-05 13:59:31.379823+00', NULL, 'aal1', NULL, '2025-11-05 13:59:31.379171', 'python-httpx/0.28.1', '34.96.41.140', NULL, NULL, NULL, NULL),
	('a9284985-a7ba-41f0-976c-8f81392005e1', '478b7491-ff6c-490b-982c-a4dc866dcefc', '2025-11-05 15:08:36.650211+00', '2025-11-05 15:08:36.650211+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '195.154.25.58', NULL, NULL, NULL, NULL),
	('37eac534-7a27-4658-9d41-43954ebdee65', '478b7491-ff6c-490b-982c-a4dc866dcefc', '2025-11-05 16:16:59.739+00', '2025-11-05 16:16:59.739+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '195.154.25.58', NULL, NULL, NULL, NULL),
	('1c2afd2e-6c9c-4796-84a6-7a395fcc2001', '478b7491-ff6c-490b-982c-a4dc866dcefc', '2025-11-06 12:51:57.339899+00', '2025-11-07 08:02:09.956498+00', NULL, 'aal1', NULL, '2025-11-07 08:02:09.955965', 'python-httpx/0.28.1', '195.154.25.58', NULL, NULL, NULL, NULL),
	('cbebc32f-af3c-41f4-b8ac-56f9fa9e572d', '478b7491-ff6c-490b-982c-a4dc866dcefc', '2025-11-10 11:32:57.669123+00', '2025-11-10 11:32:57.669123+00', NULL, 'aal1', NULL, NULL, 'python-httpx/0.28.1', '195.154.25.58', NULL, NULL, NULL, NULL),
	('c0cb516b-b833-4b83-ac91-156e0c0b85fd', '478b7491-ff6c-490b-982c-a4dc866dcefc', '2025-11-06 08:46:26.191138+00', '2025-11-06 12:28:34.630062+00', NULL, 'aal1', NULL, '2025-11-06 12:28:34.629963', 'python-httpx/0.28.1', '195.154.25.58', NULL, NULL, NULL, NULL),
	('46628e2c-e3d9-436d-b2e6-f71ff2d123fc', '478b7491-ff6c-490b-982c-a4dc866dcefc', '2025-11-05 16:29:15.76006+00', '2025-11-10 12:13:37.473314+00', NULL, 'aal1', NULL, '2025-11-10 12:13:37.473221', 'python-httpx/0.28.1', '195.154.25.58', NULL, NULL, NULL, NULL),
	('365c7ac7-a124-4757-9c46-79778b9e9c2e', 'eff2a1fd-210c-4b44-9a6f-81af6534c3c8', '2025-11-09 22:29:52.298095+00', '2025-11-10 13:09:01.958197+00', NULL, 'aal1', NULL, '2025-11-10 13:09:01.9581', 'python-httpx/0.28.1', '34.96.62.33', NULL, NULL, NULL, NULL);


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."mfa_amr_claims" ("session_id", "created_at", "updated_at", "authentication_method", "id") VALUES
	('8aea9a19-1d35-48ad-be74-510cb01bc3ac', '2025-10-27 09:20:24.340913+00', '2025-10-27 09:20:24.340913+00', 'password', '9fa30515-4a8d-47b8-aefb-02e501bc2262'),
	('642cb5a6-9086-4334-967e-f74b5c151124', '2025-10-27 09:28:57.793255+00', '2025-10-27 09:28:57.793255+00', 'password', '1dd5ccf1-4680-49f3-83aa-8f544b031ce9'),
	('a163fe55-df1f-4ef3-bd2b-60b0c060252a', '2025-10-27 09:32:01.96123+00', '2025-10-27 09:32:01.96123+00', 'password', 'f5d74cfd-37a6-4c28-90ad-da53330c8d5f'),
	('11d5532b-0847-4fc9-869e-aa6e6df27828', '2025-10-27 09:32:37.291087+00', '2025-10-27 09:32:37.291087+00', 'password', 'a0279316-f72e-4a11-a164-365a44b6936b'),
	('834c7d9b-87b4-4786-a715-abc4b2cd807e', '2025-10-27 09:34:02.223683+00', '2025-10-27 09:34:02.223683+00', 'password', '40e2ca13-0454-4a03-bdae-8cd521db2143'),
	('49939e2f-97d8-4b84-985c-4fd629e82cae', '2025-10-27 09:37:07.27842+00', '2025-10-27 09:37:07.27842+00', 'password', '60f99eb5-11f6-47c8-a8b2-6a9bab3296c1'),
	('b742faeb-f9ff-412e-a695-a59d756efc04', '2025-10-27 09:41:01.811051+00', '2025-10-27 09:41:01.811051+00', 'password', 'fa5a31cc-a33f-43ce-9e28-a6a5c9dd63d3'),
	('3a9273f1-87f1-45d0-81e3-e834580cdf1f', '2025-10-27 11:44:32.067494+00', '2025-10-27 11:44:32.067494+00', 'password', 'dff910c4-9b68-4f64-a2d1-cc6f1d6eb896'),
	('c7becc29-a278-46b8-a2be-5e957e72ef18', '2025-10-27 11:46:16.918995+00', '2025-10-27 11:46:16.918995+00', 'password', '849d28fb-101b-49f8-868e-467ea84405d6'),
	('973583d4-4aef-4530-b45f-b7f48497c108', '2025-10-27 16:25:38.033083+00', '2025-10-27 16:25:38.033083+00', 'password', '1e80ec0b-dca5-47ba-9e11-28eb8aaf011f'),
	('d0e29fa6-51a0-499d-aa6c-0513bee7e5b3', '2025-10-27 16:25:50.663974+00', '2025-10-27 16:25:50.663974+00', 'password', 'ed967f4e-7a0c-4079-be45-6fd3a7aeca07'),
	('17270fc1-3ef5-4918-8231-2584f755fcb5', '2025-10-27 17:50:54.034249+00', '2025-10-27 17:50:54.034249+00', 'password', '26d535d4-bffb-49a4-9991-7108bd5a7b61'),
	('e5aaa2fb-4ae5-4bc0-b15f-6681a51a23f0', '2025-10-27 17:52:06.663534+00', '2025-10-27 17:52:06.663534+00', 'password', 'f4c476b3-1e2f-4ab3-a34d-d7644b86a7fe'),
	('990ceb39-d908-4c87-b1ab-78aaa2c4bb4c', '2025-10-27 17:56:34.85373+00', '2025-10-27 17:56:34.85373+00', 'password', '1fd7bdb1-d90f-493d-92c2-495416824c64'),
	('7356b6d1-cb6c-41e6-8640-5a5f61f91f3a', '2025-10-27 17:57:17.302179+00', '2025-10-27 17:57:17.302179+00', 'password', '71c38aef-85b6-4302-896d-abddf153249a'),
	('4f4efa39-863a-4bbe-bfd0-5b8d903ec4d1', '2025-10-27 18:00:49.778244+00', '2025-10-27 18:00:49.778244+00', 'password', 'e86107ef-96c7-490c-92e1-c024efeadf8c'),
	('099fef53-3e30-49f1-9486-1127e197c929', '2025-10-27 19:18:42.290705+00', '2025-10-27 19:18:42.290705+00', 'password', '6b3d3c7a-9385-43f6-b440-bff246b77b38'),
	('60285b31-099d-431a-b2c7-1412224bfa15', '2025-10-27 19:19:01.612238+00', '2025-10-27 19:19:01.612238+00', 'password', 'ab9fe04d-a944-4a3c-8321-cae5061e6ab3'),
	('19f1618c-bb7c-4513-ab60-048c5cf929e6', '2025-10-27 19:19:30.8634+00', '2025-10-27 19:19:30.8634+00', 'password', 'a9b89b71-ead8-484c-89e3-13b5be35579e'),
	('7854db8f-dbac-4235-9134-809065c2cd2d', '2025-10-27 20:45:56.048849+00', '2025-10-27 20:45:56.048849+00', 'password', 'b5afbf1c-fe12-4f74-b9d4-1f564b574147'),
	('ffeb3960-0df5-4d9f-a47e-556eb0fa449f', '2025-10-27 20:46:30.246519+00', '2025-10-27 20:46:30.246519+00', 'password', '0a42ea8c-86b0-4df5-b36d-9416603140b6'),
	('2e6ddfc8-1b1f-46a8-bf9d-b5aebf650492', '2025-10-27 20:47:01.526661+00', '2025-10-27 20:47:01.526661+00', 'password', '85d9c03d-1d12-4c7e-b6c2-7064c0a209ad'),
	('7ffa088d-d1fc-40d8-8894-d9c59af522bf', '2025-10-27 22:33:48.421895+00', '2025-10-27 22:33:48.421895+00', 'password', '349e7a6b-6889-4502-913b-814a1931454d'),
	('9a074506-26bb-4c25-bc88-d021e59076d4', '2025-10-27 22:35:14.087394+00', '2025-10-27 22:35:14.087394+00', 'password', 'ad50e0f4-7db6-4306-9263-fd4dd6e6e624'),
	('9f480a46-7622-46a5-9c5b-c86d99511194', '2025-10-27 22:36:03.948236+00', '2025-10-27 22:36:03.948236+00', 'password', 'd8aa29b8-cd19-438e-b53f-f4fa2c97527d'),
	('20fdafb4-06fb-439e-b995-2a1ae544f24a', '2025-10-28 14:09:09.479999+00', '2025-10-28 14:09:09.479999+00', 'password', '5a67fa35-da5b-4dec-8476-c17882d3707d'),
	('b637cb70-f39a-4bd4-b546-d8c10af3c522', '2025-11-05 09:15:31.418441+00', '2025-11-05 09:15:31.418441+00', 'password', 'd203e51e-9698-4f82-bce4-49f860cd85f1'),
	('a9284985-a7ba-41f0-976c-8f81392005e1', '2025-11-05 15:08:36.680348+00', '2025-11-05 15:08:36.680348+00', 'password', '54d821db-3b86-448a-91d0-46a7b2501af1'),
	('37eac534-7a27-4658-9d41-43954ebdee65', '2025-11-05 16:16:59.797238+00', '2025-11-05 16:16:59.797238+00', 'password', '81807e96-5a27-4bf6-b3b7-a7392248b4e6'),
	('46628e2c-e3d9-436d-b2e6-f71ff2d123fc', '2025-11-05 16:29:15.789923+00', '2025-11-05 16:29:15.789923+00', 'password', '88d81dd8-f8ee-4c17-92a6-f104de42bef0'),
	('c0cb516b-b833-4b83-ac91-156e0c0b85fd', '2025-11-06 08:46:26.258297+00', '2025-11-06 08:46:26.258297+00', 'password', '2721e3ae-674a-4561-9b0b-03f899f46778'),
	('1c2afd2e-6c9c-4796-84a6-7a395fcc2001', '2025-11-06 12:51:57.361779+00', '2025-11-06 12:51:57.361779+00', 'password', '014a99e8-da20-4938-984d-fda6efdf69e5'),
	('365c7ac7-a124-4757-9c46-79778b9e9c2e', '2025-11-09 22:29:52.347393+00', '2025-11-09 22:29:52.347393+00', 'password', '8f895e31-3eda-4ed6-8049-4f93735c926d'),
	('cbebc32f-af3c-41f4-b8ac-56f9fa9e572d', '2025-11-10 11:32:57.705797+00', '2025-11-10 11:32:57.705797+00', 'password', '19aa2159-65d9-40e7-8c7c-5e9fdec66a1b');


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: oauth_authorizations; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: oauth_consents; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."refresh_tokens" ("instance_id", "id", "token", "user_id", "revoked", "created_at", "updated_at", "parent", "session_id") VALUES
	('00000000-0000-0000-0000-000000000000', 1367, 'xhsdupqum3nh', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 09:20:24.326807+00', '2025-10-27 09:20:24.326807+00', NULL, '8aea9a19-1d35-48ad-be74-510cb01bc3ac'),
	('00000000-0000-0000-0000-000000000000', 1368, 'zitxm6lgjb4y', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 09:28:57.780056+00', '2025-10-27 09:28:57.780056+00', NULL, '642cb5a6-9086-4334-967e-f74b5c151124'),
	('00000000-0000-0000-0000-000000000000', 1369, '2gpasumcdzbd', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 09:32:01.958923+00', '2025-10-27 09:32:01.958923+00', NULL, 'a163fe55-df1f-4ef3-bd2b-60b0c060252a'),
	('00000000-0000-0000-0000-000000000000', 1370, 'fxykp5jxah44', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 09:32:37.289736+00', '2025-10-27 09:32:37.289736+00', NULL, '11d5532b-0847-4fc9-869e-aa6e6df27828'),
	('00000000-0000-0000-0000-000000000000', 1371, '7bwikyvtiqia', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 09:34:02.212812+00', '2025-10-27 09:34:02.212812+00', NULL, '834c7d9b-87b4-4786-a715-abc4b2cd807e'),
	('00000000-0000-0000-0000-000000000000', 1372, 'p6erkjmjbsva', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 09:37:07.276337+00', '2025-10-27 09:37:07.276337+00', NULL, '49939e2f-97d8-4b84-985c-4fd629e82cae'),
	('00000000-0000-0000-0000-000000000000', 1373, 'jlpuqubqnzul', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 09:41:01.808736+00', '2025-10-27 09:41:01.808736+00', NULL, 'b742faeb-f9ff-412e-a695-a59d756efc04'),
	('00000000-0000-0000-0000-000000000000', 1374, 'zgj3y6tt2ciq', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 11:44:32.046334+00', '2025-10-27 11:44:32.046334+00', NULL, '3a9273f1-87f1-45d0-81e3-e834580cdf1f'),
	('00000000-0000-0000-0000-000000000000', 1375, 'gsp675m5zltp', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 11:46:16.914774+00', '2025-10-27 11:46:16.914774+00', NULL, 'c7becc29-a278-46b8-a2be-5e957e72ef18'),
	('00000000-0000-0000-0000-000000000000', 1376, '472poflklac4', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 16:25:37.988767+00', '2025-10-27 16:25:37.988767+00', NULL, '973583d4-4aef-4530-b45f-b7f48497c108'),
	('00000000-0000-0000-0000-000000000000', 1377, 'de3czcnmaxge', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 16:25:50.662132+00', '2025-10-27 16:25:50.662132+00', NULL, 'd0e29fa6-51a0-499d-aa6c-0513bee7e5b3'),
	('00000000-0000-0000-0000-000000000000', 1378, '32pl7nch4xpw', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 17:50:53.999764+00', '2025-10-27 17:50:53.999764+00', NULL, '17270fc1-3ef5-4918-8231-2584f755fcb5'),
	('00000000-0000-0000-0000-000000000000', 1379, 'gp46f7weg4eb', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 17:52:06.661407+00', '2025-10-27 17:52:06.661407+00', NULL, 'e5aaa2fb-4ae5-4bc0-b15f-6681a51a23f0'),
	('00000000-0000-0000-0000-000000000000', 1380, '27qdk3ov7dki', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 17:56:34.847579+00', '2025-10-27 17:56:34.847579+00', NULL, '990ceb39-d908-4c87-b1ab-78aaa2c4bb4c'),
	('00000000-0000-0000-0000-000000000000', 1381, '6zgmhbxhnfkw', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 17:57:17.300967+00', '2025-10-27 17:57:17.300967+00', NULL, '7356b6d1-cb6c-41e6-8640-5a5f61f91f3a'),
	('00000000-0000-0000-0000-000000000000', 1382, 'pe3lhc3osgfv', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 18:00:49.776047+00', '2025-10-27 18:00:49.776047+00', NULL, '4f4efa39-863a-4bbe-bfd0-5b8d903ec4d1'),
	('00000000-0000-0000-0000-000000000000', 1383, 'vxudpncabbhj', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 19:18:42.266998+00', '2025-10-27 19:18:42.266998+00', NULL, '099fef53-3e30-49f1-9486-1127e197c929'),
	('00000000-0000-0000-0000-000000000000', 1384, 'wajtolvlvevl', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 19:19:01.610415+00', '2025-10-27 19:19:01.610415+00', NULL, '60285b31-099d-431a-b2c7-1412224bfa15'),
	('00000000-0000-0000-0000-000000000000', 1385, 'bzresfgqndll', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 19:19:30.861509+00', '2025-10-27 19:19:30.861509+00', NULL, '19f1618c-bb7c-4513-ab60-048c5cf929e6'),
	('00000000-0000-0000-0000-000000000000', 1386, 'ssjn7k4ppzoh', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 20:45:56.020255+00', '2025-10-27 20:45:56.020255+00', NULL, '7854db8f-dbac-4235-9134-809065c2cd2d'),
	('00000000-0000-0000-0000-000000000000', 1387, 'cmkrhtodcj44', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 20:46:30.2433+00', '2025-10-27 20:46:30.2433+00', NULL, 'ffeb3960-0df5-4d9f-a47e-556eb0fa449f'),
	('00000000-0000-0000-0000-000000000000', 1388, 'hziuqdhrbqew', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 20:47:01.524809+00', '2025-10-27 20:47:01.524809+00', NULL, '2e6ddfc8-1b1f-46a8-bf9d-b5aebf650492'),
	('00000000-0000-0000-0000-000000000000', 1389, 'rbsygzfknglv', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 22:33:48.398009+00', '2025-10-27 22:33:48.398009+00', NULL, '7ffa088d-d1fc-40d8-8894-d9c59af522bf'),
	('00000000-0000-0000-0000-000000000000', 1390, 'icgtdv2zdald', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 22:35:14.08418+00', '2025-10-27 22:35:14.08418+00', NULL, '9a074506-26bb-4c25-bc88-d021e59076d4'),
	('00000000-0000-0000-0000-000000000000', 1391, 'nr5bx7ywbue6', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-27 22:36:03.945288+00', '2025-10-27 22:36:03.945288+00', NULL, '9f480a46-7622-46a5-9c5b-c86d99511194'),
	('00000000-0000-0000-0000-000000000000', 1392, 'afeo7wctgmlg', '51eee0a1-8f20-4403-b5f1-0566375db20b', true, '2025-10-28 14:09:09.43658+00', '2025-10-28 16:36:43.448023+00', NULL, '20fdafb4-06fb-439e-b995-2a1ae544f24a'),
	('00000000-0000-0000-0000-000000000000', 1393, 'mga6btgrnsei', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-10-28 16:36:43.461806+00', '2025-10-28 16:36:43.461806+00', 'afeo7wctgmlg', '20fdafb4-06fb-439e-b995-2a1ae544f24a'),
	('00000000-0000-0000-0000-000000000000', 1394, '6btuk73wt7ro', '51eee0a1-8f20-4403-b5f1-0566375db20b', true, '2025-11-05 09:15:31.378652+00', '2025-11-05 13:59:31.352616+00', NULL, 'b637cb70-f39a-4bd4-b546-d8c10af3c522'),
	('00000000-0000-0000-0000-000000000000', 1395, '3w2pkyuxjueu', '51eee0a1-8f20-4403-b5f1-0566375db20b', false, '2025-11-05 13:59:31.364983+00', '2025-11-05 13:59:31.364983+00', '6btuk73wt7ro', 'b637cb70-f39a-4bd4-b546-d8c10af3c522'),
	('00000000-0000-0000-0000-000000000000', 1396, '4qgyzhymhg65', '478b7491-ff6c-490b-982c-a4dc866dcefc', false, '2025-11-05 15:08:36.662689+00', '2025-11-05 15:08:36.662689+00', NULL, 'a9284985-a7ba-41f0-976c-8f81392005e1'),
	('00000000-0000-0000-0000-000000000000', 1397, 'cwn3walpclo5', '478b7491-ff6c-490b-982c-a4dc866dcefc', false, '2025-11-05 16:16:59.76369+00', '2025-11-05 16:16:59.76369+00', NULL, '37eac534-7a27-4658-9d41-43954ebdee65'),
	('00000000-0000-0000-0000-000000000000', 1398, 'mkxpcwznfbkm', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-05 16:29:15.769267+00', '2025-11-05 22:12:23.491982+00', NULL, '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1399, 'eas4qfppqw5h', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-05 22:12:23.513175+00', '2025-11-06 08:01:45.685738+00', 'mkxpcwznfbkm', '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1400, 'rsmsqil7c3gv', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 08:01:45.708979+00', '2025-11-06 09:24:34.833873+00', 'eas4qfppqw5h', '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1401, 'rucbtt6ah3d3', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 08:46:26.2126+00', '2025-11-06 09:41:27.643662+00', NULL, 'c0cb516b-b833-4b83-ac91-156e0c0b85fd'),
	('00000000-0000-0000-0000-000000000000', 1402, 'hialpp2h7ccf', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 09:24:34.853708+00', '2025-11-06 10:22:27.641551+00', 'rsmsqil7c3gv', '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1403, '6hk6dz4w4lcq', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 09:41:27.664683+00', '2025-11-06 10:36:28.654707+00', 'rucbtt6ah3d3', 'c0cb516b-b833-4b83-ac91-156e0c0b85fd'),
	('00000000-0000-0000-0000-000000000000', 1405, 'apeclriuqjjm', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 10:36:28.661391+00', '2025-11-06 12:28:34.591607+00', '6hk6dz4w4lcq', 'c0cb516b-b833-4b83-ac91-156e0c0b85fd'),
	('00000000-0000-0000-0000-000000000000', 1406, 'imevdv3enqas', '478b7491-ff6c-490b-982c-a4dc866dcefc', false, '2025-11-06 12:28:34.612699+00', '2025-11-06 12:28:34.612699+00', 'apeclriuqjjm', 'c0cb516b-b833-4b83-ac91-156e0c0b85fd'),
	('00000000-0000-0000-0000-000000000000', 1404, 'uifyda4dm5fh', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 10:22:27.657497+00', '2025-11-06 12:29:20.77905+00', 'hialpp2h7ccf', '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1408, 'sqvqvbckouix', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 12:51:57.347311+00', '2025-11-06 13:46:59.063578+00', NULL, '1c2afd2e-6c9c-4796-84a6-7a395fcc2001'),
	('00000000-0000-0000-0000-000000000000', 1407, 'aeccdibseknk', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 12:29:20.779396+00', '2025-11-06 14:16:33.32457+00', 'uifyda4dm5fh', '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1409, 'hmlcycwg6xbh', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 13:46:59.08292+00', '2025-11-06 14:42:00.757264+00', 'sqvqvbckouix', '1c2afd2e-6c9c-4796-84a6-7a395fcc2001'),
	('00000000-0000-0000-0000-000000000000', 1410, 'c3bkuhr6syr7', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 14:16:33.334828+00', '2025-11-06 15:19:59.950839+00', 'aeccdibseknk', '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1411, 'mtlzpbvi7guv', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 14:42:00.782845+00', '2025-11-06 15:37:01.766581+00', 'hmlcycwg6xbh', '1c2afd2e-6c9c-4796-84a6-7a395fcc2001'),
	('00000000-0000-0000-0000-000000000000', 1412, '6fgn6h57doq4', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 15:19:59.974247+00', '2025-11-06 16:24:19.382106+00', 'c3bkuhr6syr7', '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1413, '35tlpms6rz3k', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 15:37:01.775282+00', '2025-11-06 16:32:02.797541+00', 'mtlzpbvi7guv', '1c2afd2e-6c9c-4796-84a6-7a395fcc2001'),
	('00000000-0000-0000-0000-000000000000', 1414, 'b7xg67f6lzuc', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 16:24:19.406499+00', '2025-11-06 17:19:24.497667+00', '6fgn6h57doq4', '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1415, '32xrsmi5zg5b', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 16:32:02.799438+00', '2025-11-06 17:27:08.141876+00', '35tlpms6rz3k', '1c2afd2e-6c9c-4796-84a6-7a395fcc2001'),
	('00000000-0000-0000-0000-000000000000', 1417, 'vz2r6gdnlq3z', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 17:27:08.161712+00', '2025-11-06 21:17:05.858753+00', '32xrsmi5zg5b', '1c2afd2e-6c9c-4796-84a6-7a395fcc2001'),
	('00000000-0000-0000-0000-000000000000', 1418, '22gjic6wvf3b', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 21:17:05.873062+00', '2025-11-07 08:02:09.90477+00', 'vz2r6gdnlq3z', '1c2afd2e-6c9c-4796-84a6-7a395fcc2001'),
	('00000000-0000-0000-0000-000000000000', 1416, 'ygedbzrbclmq', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-06 17:19:24.513161+00', '2025-11-07 08:25:47.295069+00', 'b7xg67f6lzuc', '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1419, 'llo46ynt4wth', '478b7491-ff6c-490b-982c-a4dc866dcefc', false, '2025-11-07 08:02:09.929617+00', '2025-11-07 08:02:09.929617+00', '22gjic6wvf3b', '1c2afd2e-6c9c-4796-84a6-7a395fcc2001'),
	('00000000-0000-0000-0000-000000000000', 1421, 'vixxk2wb7flv', 'eff2a1fd-210c-4b44-9a6f-81af6534c3c8', true, '2025-11-09 22:29:52.315607+00', '2025-11-10 09:08:13.433813+00', NULL, '365c7ac7-a124-4757-9c46-79778b9e9c2e'),
	('00000000-0000-0000-0000-000000000000', 1422, 'mnxeyla54jcc', 'eff2a1fd-210c-4b44-9a6f-81af6534c3c8', true, '2025-11-10 09:08:13.457166+00', '2025-11-10 10:03:13.789347+00', 'vixxk2wb7flv', '365c7ac7-a124-4757-9c46-79778b9e9c2e'),
	('00000000-0000-0000-0000-000000000000', 1423, '47v6jjntmi32', 'eff2a1fd-210c-4b44-9a6f-81af6534c3c8', true, '2025-11-10 10:03:13.800629+00', '2025-11-10 11:10:25.025378+00', 'mnxeyla54jcc', '365c7ac7-a124-4757-9c46-79778b9e9c2e'),
	('00000000-0000-0000-0000-000000000000', 1425, 't6mmplj5alau', '478b7491-ff6c-490b-982c-a4dc866dcefc', false, '2025-11-10 11:32:57.682493+00', '2025-11-10 11:32:57.682493+00', NULL, 'cbebc32f-af3c-41f4-b8ac-56f9fa9e572d'),
	('00000000-0000-0000-0000-000000000000', 1424, 'k3xrtcwj7nmw', 'eff2a1fd-210c-4b44-9a6f-81af6534c3c8', true, '2025-11-10 11:10:25.038091+00', '2025-11-10 12:09:29.825903+00', '47v6jjntmi32', '365c7ac7-a124-4757-9c46-79778b9e9c2e'),
	('00000000-0000-0000-0000-000000000000', 1420, '3r7cwwltfkco', '478b7491-ff6c-490b-982c-a4dc866dcefc', true, '2025-11-07 08:25:47.314248+00', '2025-11-10 12:13:37.356757+00', 'ygedbzrbclmq', '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1427, 'gmxj4wil4i5h', '478b7491-ff6c-490b-982c-a4dc866dcefc', false, '2025-11-10 12:13:37.360644+00', '2025-11-10 12:13:37.360644+00', '3r7cwwltfkco', '46628e2c-e3d9-436d-b2e6-f71ff2d123fc'),
	('00000000-0000-0000-0000-000000000000', 1426, '5x2ih6pkfncz', 'eff2a1fd-210c-4b44-9a6f-81af6534c3c8', true, '2025-11-10 12:09:29.852056+00', '2025-11-10 13:09:01.944183+00', 'k3xrtcwj7nmw', '365c7ac7-a124-4757-9c46-79778b9e9c2e'),
	('00000000-0000-0000-0000-000000000000', 1428, 'ezinrssyzq3o', 'eff2a1fd-210c-4b44-9a6f-81af6534c3c8', false, '2025-11-10 13:09:01.951419+00', '2025-11-10 13:09:01.951419+00', '5x2ih6pkfncz', '365c7ac7-a124-4757-9c46-79778b9e9c2e');


--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: blog_posts; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: chats; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."chats" ("id", "created_at", "user_id", "chat_provider_id", "provider_name", "title") VALUES
	(15957, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68e916d0-49ac-8325-9131-0f9a068b6bd8', 'ChatGPT', 'Vérifier permis automatique'),
	(15956, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68e8f110-96e8-8330-b90e-cddc15828dce', 'ChatGPT', 'Fonctionnement 4WD Outlander 2012'),
	(15954, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68ee5616-a5c0-8330-8b1a-35c234b104b0', 'ChatGPT', 'Correction lettre motivation'),
	(15960, '2025-11-06 17:19:10.472241+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', 'ChatGPT', 'Intérêt de Next.js avec backend'),
	(15959, '2025-11-06 14:38:52.963245+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cae83-c4ac-832b-82c5-ca4c9d2aa7bc', 'ChatGPT', 'Méthodes de communication backend'),
	(15958, '2025-11-05 16:33:59.527523+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690b7beb-9dec-832f-8c2e-ed7420e7ea5b', 'ChatGPT', 'Blocage Brave extensions'),
	(15930, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690b5bee-e7b8-8326-a477-517420207067', 'ChatGPT', 'Accéder fichiers WSL2 Ubuntu'),
	(15931, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690b4b54-699c-8332-a16f-d7fc7d04bc48', 'ChatGPT', 'Supprimer Docker complet'),
	(15932, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690b1017-7fd8-8329-8601-e9b61bee3f4b', 'ChatGPT', 'Bonnes pratiques GitHub'),
	(15933, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690a01ef-1d50-8329-8522-5432a781600b', 'ChatGPT', 'Server Actions Next.js'),
	(15934, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '6909c48b-1018-8333-9ce8-17168ded41e4', 'ChatGPT', 'Plateforme SaaS pléonasme'),
	(15935, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '6909109a-07dc-832d-ac27-184f8e9c8460', 'ChatGPT', 'Interdictions 4wd Australie'),
	(15940, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68fe139f-e4f0-832f-a599-d900d848b298', 'ChatGPT', 'Tarifs de taxi en France'),
	(15941, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68fb9b5a-a444-832a-b5c4-400c741b3713', 'ChatGPT', 'Minimum légal stage France'),
	(15942, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68fa8735-6340-8333-a640-cc2a86715bf1', 'ChatGPT', 'New chat'),
	(15943, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68f91ffb-2f48-8327-810a-3288c58de7c7', 'ChatGPT', 'Formulaire stage Markdown'),
	(15944, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68f78954-386c-8325-bc4b-9a73ae263f28', 'ChatGPT', 'Code d''invitation WoT'),
	(15945, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68f76312-f058-8328-b557-40fcdec5bbb7', 'ChatGPT', 'Brancher LED sur pile'),
	(15946, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68f67b5f-3140-8330-923c-c27a59e6b29c', 'ChatGPT', 'Annulation abonnement RED SFR'),
	(15955, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68eccb8b-11d4-8331-88df-981856a2aef6', 'ChatGPT', 'Cochez oui ou non'),
	(15947, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68f64017-b444-8326-b6ec-c3d316fafe18', 'ChatGPT', 'Applications pour comparer prix'),
	(15948, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68f63e30-dc04-832b-bb14-a0252d9899b4', 'ChatGPT', 'Salaire minimum stage Paris'),
	(15949, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68f62220-9f0c-832f-8652-bec129011408', 'ChatGPT', 'Refactoring backend MVC'),
	(15950, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68f281b4-aa38-832b-9bd0-04ef18b18277', 'ChatGPT', 'Coût aller-retour voiture'),
	(15951, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68f117d6-7444-832a-8b02-92a3ab07e7cd', 'ChatGPT', 'Reformuler message stage'),
	(15952, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68f106f4-2e90-8329-bf78-014ae1808c7b', 'ChatGPT', 'Find largest number JS'),
	(15953, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '68efcb1a-8780-832c-b97d-1ebf609f7c46', 'ChatGPT', 'Écrire un texte de 1000 tokens'),
	(15961, '2025-11-07 08:26:02.647325+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cd89c-a294-8327-bb7b-670bd58fad15', 'ChatGPT', 'Explorateur de fichiers'),
	(15936, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '69073f48-1e50-832e-996e-0523fbd9d44f', 'ChatGPT', 'Livret Bleu Crédit Mutuel'),
	(15937, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '6903aecc-cfcc-832f-97b6-bbb24b830e74', 'ChatGPT', 'Connecter Google Drive PC'),
	(15938, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '69038df6-6394-8326-9036-874ee08af995', 'ChatGPT', 'Restaurer saisie automatique mdp'),
	(15939, '2025-11-05 16:30:31.611874+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '6900e8a0-0504-8321-9269-d913eca5ede7', 'ChatGPT', 'Architectures backend principales');


--
-- Data for Name: companies; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: favorites; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: landing_page_blog_posts; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: landing_page_contact_form; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."messages" ("id", "created_at", "user_id", "chat_provider_id", "message_provider_id", "role", "model", "parent_message_provider_id", "tools", "content") VALUES
	(3327, '2025-11-06 14:19:57.251+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cae83-c4ac-832b-82c5-ca4c9d2aa7bc', '55859a90-fafe-4157-a7b1-e22ae19938ab', 'user', 'auto', 'client-created-root', NULL, 'comment s''appelle la méthode de travail de backend utilisé par frontend*'),
	(3328, '2025-11-06 14:19:59.937527+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cae83-c4ac-832b-82c5-ca4c9d2aa7bc', '388f17e4-a8cd-47ed-ba0b-eddaf423b115', 'assistant', 'gpt-5', '55859a90-fafe-4157-a7b1-e22ae19938ab', NULL, 'Ta question est intéressante, mais elle peut avoir **plusieurs réponses possibles** selon ce que tu veux dire par “méthode de travail de backend utilisée par le frontend”. Voici les cas les plus fréquents 👇  

---

### 🔹 1. Si tu parles de la **façon dont le frontend communique avec le backend**
➡️ On parle alors de **API (Application Programming Interface)**.  
Les principales **méthodes** ou **architectures d’API** sont :

| Méthode / Architecture | Description | Exemple |
|------------------------|--------------|----------|
| **REST (Representational State Transfer)** | La plus courante. Utilise HTTP (GET, POST, PUT, DELETE). Les données sont souvent au format JSON. | `fetch(''https://api.example.com/users'')` |
| **GraphQL** | Alternative moderne à REST : le frontend peut demander exactement les données dont il a besoin. | `query { user(id:1) { name, email } }` |
| **gRPC** | Basée sur Protocol Buffers (binaire, très rapide). Utilisée dans les systèmes distribués. | Utilisée entre microservices, moins pour frontend web. |
| **WebSocket** | Communication bidirectionnelle en temps réel (chat, jeux, notifications). | `new WebSocket(''wss://example.com/socket'')` |

👉 Donc, **la “méthode de travail” du backend utilisée par le frontend**, c’est souvent **une API REST ou GraphQL**.

---

### 🔹 2. Si tu parles du **modèle d’architecture générale**
Alors, on parle de :
- **Architecture client–serveur**
- **Architecture 3-tiers** (frontend, backend, base de données)
- **Architecture microservices** (backend découpé en plusieurs petits services)
- **Architecture serverless** (backend = fonctions hébergées dans le cloud)

---

### 🔹 3. Si tu veux parler du **mode d’échange de données**
- **JSON** (le plus courant)
- **XML** (plus ancien)
- **Protobuf** (utilisé avec gRPC)
- **FormData** (pour les formulaires ou fichiers)

---

👉 En résumé :  
> La méthode de travail du backend utilisée par le frontend, c’est **souvent une API REST** (ou parfois **GraphQL**) pour échanger des données via **HTTP** au format **JSON**.

---

Souhaites-tu que je t’explique **plus précisément comment le frontend appelle une API REST (avec exemple de code)** ?'),
	(3329, '2025-11-06 15:20:24.418+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cae83-c4ac-832b-82c5-ca4c9d2aa7bc', 'dc7544a6-dbd1-4a5d-b3f6-c1033b2790fc', 'user', 'auto', 'client-created-root', NULL, 'quel est l''interet d''un next avec partie server et partie client si j''ai d''un autre coté un backend ?'),
	(3330, '2025-11-06 15:20:26.326849+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', '082a797f-1b2c-46ce-9aaa-0558ee23057f', 'assistant', 'gpt-5', 'dc7544a6-dbd1-4a5d-b3f6-c1033b2790fc', NULL, 'Excellente question ! 👏  
C’est une interrogation fréquente chez les devs qui découvrent **Next.js** et qui ont déjà un **backend séparé** (par exemple en NestJS, Django, Spring Boot, etc.).  

Voyons ça en détail 👇  

---

## 🎯 Le rôle de Next.js

Next.js n’est **pas uniquement un framework frontend React** :  
c’est un **framework full-stack** (frontend + backend léger intégré).

Il te permet :
- de rendre tes pages côté serveur (SSR),
- d’avoir du rendu statique (SSG),
- d’utiliser des **API Routes** côté serveur si besoin,
- et de gérer l’hydratation React côté client.

---

## 🧩 Cas où tu as déjà un backend séparé

Supposons :
- ton backend = une API REST/GraphQL (par ex. `api.monsite.com`),
- ton frontend Next.js = `app.monsite.com`.

Tu peux **continuer à utiliser Next.js uniquement pour le rendu et le routing frontend**.  
Mais Next.js a quand même un intérêt, même si tu as déjà un backend complet 👇

---

## ✅ Les intérêts de Next.js dans ce cas

### 1. **Rendu côté serveur (SSR)**
Tu peux générer tes pages avec des données issues de ton backend au moment de la requête :
```js
export async function getServerSideProps() {
  const res = await fetch(''https://api.monsite.com/posts'')
  const posts = await res.json()
  return { props: { posts } }
}
```
➡️ Le HTML est pré-rempli côté serveur, ce qui améliore :
- le **SEO**,  
- la **vitesse du premier rendu**,  
- et l’**expérience utilisateur**.

---

### 2. **Protection de données / tokens côté serveur**
Tu peux garder certaines logiques sensibles côté serveur Next :
- appels API avec tokens secrets,
- vérification d’auth côté serveur avant de rendre une page.

➡️ Cela évite d’exposer des clés API au navigateur.

---

### 3. **Simplification du déploiement frontend**
Tu n’as pas besoin de séparer totalement “frontend React” et “SSR proxy” :
- Next peut faire office de couche de rendu,
- et ton backend reste purement “data”.

➡️ Tu peux héberger Next sur Vercel, Netlify ou en conteneur sans te soucier du SSR manuel.

---

### 4. **Possibilité d’un petit backend côté Next (API Routes)**
Même si tu as un “gros” backend principal, tu peux :
- créer des **API Routes** pour des besoins ponctuels (webhooks, proxy, middle-layer),
- ou des **actions server-side** (avec `server actions` dans App Router).

Cela évite de toucher ton backend principal pour des petits cas.

---

### 5. **Expérience dev unifiée**
Tu gardes une stack unique côté frontend :
- React + SSR + Routing + API intégration,
- code JS/TS homogène,
- facilité d’hébergement et de CI/CD.

---

## 🚫 Quand Next.js est *moins utile*
Si ton frontend est :
- 100 % SPA (pas besoin de SSR/SEO),
- et ton backend gère déjà le rendu HTML (par exemple Django Templates, PHP, etc.),  
alors Next.js t’apporte peu d’avantages.

---

## 🧠 En résumé

| Besoin | Est-ce que Next.js aide ? |
|--------|----------------------------|
| Rendu SSR/SEO | ✅ Oui |
| Appels API sécurisés côté serveur | ✅ Oui |
| Backend déjà complet | ⚙️ Oui, mais tu peux te limiter au rendu |
| Petit backend ou pas de backend | 🟢 Next.js peut tout faire |
| SPA pure sans SSR | 🚫 Peu d’intérêt |

---

Si tu veux, je peux te faire un petit **schéma d’architecture typique** :  
➡️ Next.js (frontend SSR) + backend séparé (API REST/GraphQL) + DB.  
Souhaites-tu que je te le génère ?'),
	(3331, '2025-11-06 15:24:33.883+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', 'dc42ab66-241a-49d2-8ad4-2060f49515b0', 'user', 'auto', '082a797f-1b2c-46ce-9aaa-0558ee23057f', NULL, 'peux tu me montrer un exemple de projet utilisant next clinet et server avec un be d''un autre coté en rest'),
	(3332, '2025-11-06 15:24:34.708762+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', '7af04298-6840-47e7-96ec-522249916794', 'assistant', 'gpt-5', 'dc42ab66-241a-49d2-8ad4-2060f49515b0', NULL, 'Excellent — tu veux donc un **exemple concret** d’architecture Next.js (client + server) qui **interagit avec un backend REST séparé**.  
Parfait 👍 je vais te montrer **une structure complète**, puis un **exemple de code minimal** côté Next.

---

## 🧱 1. Structure du projet

Voici l’idée globale :

```
📦 mon-projet/
├── 📁 backend/               # Ton backend REST (ex: NestJS, Express, Django, etc.)
│   ├── src/
│   ├── package.json
│   └── ...
│
├── 📁 frontend/              # App Next.js
│   ├── app/
│   │   ├── page.tsx          # Page principale (client)
│   │   ├── posts/
│   │   │   └── page.tsx      # Page affichant les posts (server)
│   │   └── api/
│   │       └── proxy/route.ts # (optionnel) route proxy server-side
│   ├── next.config.js
│   └── package.json
│
└── docker-compose.yml        # (optionnel) pour tout lancer ensemble
```

Le backend expose une API REST, par exemple :  
```
GET http://localhost:4000/posts
GET http://localhost:4000/posts/:id
```

Le frontend Next.js est sur :  
```
http://localhost:3000
```

---

## ⚙️ 2. Exemple minimal du **backend REST**

Ici, juste pour l’exemple, un backend Express simple :

```js
// backend/server.js
import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

const posts = [
  { id: 1, title: "Premier post", content: "Hello world" },
  { id: 2, title: "Deuxième post", content: "Next.js + REST" },
];

app.get("/posts", (req, res) => res.json(posts));

app.listen(4000, () => console.log("Backend running on port 4000"));
```

---

## 🖥️ 3. Côté **Next.js (frontend)**

### a. Rendu côté serveur (`app/posts/page.tsx`)

```tsx
// frontend/app/posts/page.tsx
export const dynamic = "force-dynamic"; // pour forcer SSR

type Post = { id: number; title: string; content: string };

export default async function PostsPage() {
  const res = await fetch("http://localhost:4000/posts", {
    cache: "no-store", // SSR pur
  });
  const posts: Post[] = await res.json();

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">Liste des posts</h1>
      <ul className="space-y-2">
        {posts.map((p) => (
          <li key={p.id} className="p-3 border rounded">
            <h2 className="font-semibold">{p.title}</h2>
            <p>{p.content}</p>
          </li>
        ))}
      </ul>
    </main>
  );
}
```

➡️ Ici, la page est rendue **côté serveur Next.js**, qui appelle le backend REST pour récupérer les données avant d’envoyer le HTML au client.

---

### b. Composant client (interactif)

```tsx
// frontend/app/page.tsx
"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [message, setMessage] = useState("Chargement...");

  useEffect(() => {
    fetch("http://localhost:4000/posts")
      .then((res) => res.json())
      .then((data) => setMessage(`Il y a ${data.length} posts`));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Accueil (Client Component)</h1>
      <p>{message}</p>
    </div>
  );
}
```

➡️ Ici, le rendu initial se fait côté client React, avec un `useEffect()` qui appelle directement le backend REST.

---

### c. (Optionnel) Route proxy côté serveur

Tu peux éviter le CORS ou cacher des tokens avec une **route API interne Next** :

```ts
// frontend/app/api/proxy/route.ts
export async function GET() {
  const res = await fetch("http://localhost:4000/posts");
  const data = await res.json();
  return Response.json(data);
}
```

Puis côté client :
```ts
fetch("/api/proxy") // au lieu de http://localhost:4000/posts
```

➡️ Cela passe par le serveur Next, donc pas de problème de CORS ni d’expo de secrets.

---

## 🔁 4. Déroulement

| Étape | Qui agit ? | Détails |
|-------|-------------|---------|
| 1 | L’utilisateur ouvre `/posts` | Next.js fait un `fetch()` côté serveur vers le backend REST |
| 2 | Backend renvoie les données | JSON |
| 3 | Next.js génère du HTML SSR avec les données |
| 4 | Le navigateur reçoit la page déjà remplie |
| 5 | Hydratation React côté client | Les interactions deviennent dynamiques |

---

## 🚀 5. Avantages de cette approche

✅ Rendu rapide + SEO-friendly (SSR)  
✅ Logique métier dans ton backend REST existant  
✅ Facile à déployer séparément  
✅ Possibilité d’ajouter des composants client interactifs  
✅ Pas de duplication de logique entre frontend et backend  

---

Souhaites-tu que je te montre la **même architecture mais en version “production” avec un proxy (Nginx ou Vercel)**, pour voir comment Next et le backend peuvent cohabiter proprement en déploiement ?'),
	(3333, '2025-11-06 15:28:27.126+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', 'e6ddf7ed-9b16-47ff-a679-56a7ac658dce', 'user', 'auto', '7af04298-6840-47e7-96ec-522249916794', NULL, 'dans ton 3 entre a et B c''est l''un ou l''autre, ou les 2 ?'),
	(3334, '2025-11-06 15:28:27.733018+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', 'bdcaeaff-11e1-4455-8ce7-32c04593eb66', 'assistant', 'gpt-5', 'e6ddf7ed-9b16-47ff-a679-56a7ac658dce', NULL, 'Excellente remarque 💡  
La réponse est : **tu peux faire les deux**, mais **chacun a un rôle différent** selon le besoin.  

Je t’explique 👇  

---

## 🧩 A. Composant "Server" (`page.tsx` sans `"use client"`)
C’est du **rendu côté serveur (SSR)**.  
- Next exécute ton code sur le serveur,  
- fait les `fetch()` vers ton backend REST,  
- puis renvoie une **page HTML déjà remplie** au navigateur.  

👉 **Avantages :**
- Meilleur SEO (le HTML contient déjà les données)
- Chargement initial rapide
- Données sécurisées (les requêtes passent par le serveur Next)
- Idéal pour les pages de contenu, les listes, les produits, etc.

---

## 🧠 B. Composant "Client" (`"use client"`)
C’est du **rendu côté navigateur** (React classique).  
- Le HTML initial arrive presque vide,  
- puis le navigateur charge React, exécute `useEffect()`, et appelle le backend REST.

👉 **Avantages :**
- Interactivité complète (formulaires, filtres, etc.)
- Réactivité sans rechargement de page
- Idéal pour les parties dynamiques ou interactives de l’app.

---

## ⚙️ En pratique, tu fais **les deux ensemble**

C’est d’ailleurs la **philosophie de Next.js 13+ (App Router)** :
> Tu mélanges des composants server et client dans la même hiérarchie.

Exemple concret :
```tsx
// app/posts/page.tsx  → Server Component
import PostsList from "./PostsList";

export default async function PostsPage() {
  const res = await fetch("http://localhost:4000/posts", { cache: "no-store" });
  const posts = await res.json();

  return (
    <main className="p-6">
      <h1>Liste des posts</h1>
      <PostsList initialPosts={posts} />
    </main>
  );
}
```

```tsx
// app/posts/PostsList.tsx → Client Component
"use client";
import { useState } from "react";

export default function PostsList({ initialPosts }) {
  const [posts, setPosts] = useState(initialPosts);

  return (
    <ul>
      {posts.map((p) => (
        <li key={p.id}>{p.title}</li>
      ))}
    </ul>
  );
}
```

🟢 **Résultat :**
- Le serveur Next.js fait le premier rendu avec les données (`SSR`)  
- Ensuite React prend la main côté client (`hydratation`) pour gérer l’interactivité.  

---

## 🔍 En résumé

| Cas d’usage | Type de composant | Où le code s’exécute ? |
|--------------|------------------|-------------------------|
| Charger des données depuis ton backend REST avant affichage | 🖥️ **Server component** | Serveur Next.js |
| Interagir dynamiquement avec les données (clic, filtre, form...) | ⚙️ **Client component** | Navigateur |
| Combiner les deux | ✅ **SSR + hydratation** | Les deux |

---

Donc :  
➡️ Ce n’est **pas “l’un ou l’autre”**,  
➡️ C’est **souvent les deux ensemble**, selon la partie de ta page.  

---

Souhaites-tu que je te montre **un exemple complet “page SSR + composant client interactif”**, avec un petit champ de recherche qui filtre les posts ?'),
	(3335, '2025-11-06 15:31:29.52+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', 'a199be86-2af2-43f6-bec9-de31f1d9277e', 'user', 'auto', 'bdcaeaff-11e1-4455-8ce7-32c04593eb66', NULL, 'montre moi un exemple avec les 2 ensemble'),
	(3336, '2025-11-06 15:31:30.005798+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', 'b4049270-b7da-4751-ae40-a6b126193765', 'assistant', 'gpt-5', 'a199be86-2af2-43f6-bec9-de31f1d9277e', NULL, 'Parfait 👌  
Voici un **exemple complet et concret** d’une page **Next.js** (App Router) qui utilise à la fois :  

- une **partie serveur** (pour récupérer les données depuis ton backend REST avant le rendu),  
- une **partie client** (pour rendre la page interactive — ici, un champ de recherche côté navigateur).  

---

## 🧱 Structure du dossier

```
frontend/
├── app/
│   ├── posts/
│   │   ├── page.tsx          # => Composant serveur
│   │   └── PostsList.tsx     # => Composant client
│   └── layout.tsx
├── package.json
└── next.config.js
```

Ton backend REST (ex: `http://localhost:4000/posts`) renvoie :
```json
[
  { "id": 1, "title": "Apprendre Next.js", "content": "SSR et Client Components" },
  { "id": 2, "title": "Découvrir React", "content": "Hooks et composants" },
  { "id": 3, "title": "API REST avec Express", "content": "Backend simple et rapide" }
]
```

---

## 🖥️ `app/posts/page.tsx` → **Composant Serveur**

```tsx
// app/posts/page.tsx
import PostsList from "./PostsList";

export const dynamic = "force-dynamic"; // Force SSR à chaque requête

export default async function PostsPage() {
  // On récupère les données du backend REST
  const res = await fetch("http://localhost:4000/posts", { cache: "no-store" });
  const posts = await res.json();

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">Liste des posts</h1>
      {/* On passe les données initiales à un composant client */}
      <PostsList initialPosts={posts} />
    </main>
  );
}
```

💡 Ici :
- le code s’exécute **côté serveur Next** avant d’envoyer le HTML au navigateur,  
- la page est déjà remplie au moment du chargement (SEO + performance),  
- ensuite, React hydrate la page côté client pour l’interactivité.

---

## ⚙️ `app/posts/PostsList.tsx` → **Composant Client**

```tsx
// app/posts/PostsList.tsx
"use client";
import { useState } from "react";

type Post = { id: number; title: string; content: string };

export default function PostsList({ initialPosts }: { initialPosts: Post[] }) {
  const [search, setSearch] = useState("");
  const [posts] = useState(initialPosts);

  const filtered = posts.filter((p) =>
    p.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        placeholder="Rechercher un post..."
        className="border p-2 rounded mb-4 w-full"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {filtered.length === 0 && <p>Aucun post trouvé.</p>}

      <ul className="space-y-2">
        {filtered.map((p) => (
          <li key={p.id} className="p-3 border rounded">
            <h2 className="font-semibold">{p.title}</h2>
            <p>{p.content}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

💡 Ici :
- c’est un **composant client** (`"use client"`), donc exécuté dans le navigateur,  
- il reçoit les données initiales du serveur,  
- il ajoute une **interactivité** (filtrage en temps réel avec `useState`).

---

## 🧠 Ce qu’il se passe au runtime

1. **Requête utilisateur :**
   → `/posts`  
2. **Next.js (server)**  
   → fait `fetch("http://localhost:4000/posts")`  
   → construit le HTML avec les posts  
3. **Navigateur**  
   → reçoit du HTML déjà rempli  
   → React “hydrate” la page et active le composant `PostsList`  
4. **Utilisateur tape dans la barre de recherche**  
   → filtrage instantané côté client (aucun appel API supplémentaire)  

---

## 🚀 Résultat

- Chargement ultra rapide ✅  
- Page SEO-friendly (HTML déjà généré côté serveur) ✅  
- Interactivité fluide (barre de recherche dynamique) ✅  
- Séparation claire : SSR pour les données, client pour l’UI ✅  

---

Souhaites-tu que je t’ajoute à cet exemple :
- un **bouton "recharger depuis le backend"** (donc un `fetch()` côté client),  
pour te montrer comment mélanger SSR initial + appels API client ?'),
	(3337, '2025-11-06 16:24:56.592+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', '40b6984a-a0ea-4a1e-9917-af7c91fd358e', 'user', 'auto', 'b4049270-b7da-4751-ae40-a6b126193765', NULL, 'donc dans cette logique, il n''y a plus besoin de faire des call depuis la partie client vers le backend custom ?'),
	(3338, '2025-11-06 16:25:00.631336+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', 'c6bd2710-249f-444b-b9c4-963f42f93122', 'assistant', 'gpt-5', '5e4154a0-eb64-4176-a31b-5fcdda3a9c4c', NULL, 'Excellente observation 👏  
Et ta question touche un **point clé de la logique Next.js moderne (App Router)**.

La réponse courte est :  
➡️ **dans beaucoup de cas, non, tu n’as plus besoin de faire des appels directs au backend depuis le client.**  
Mais il y a **des exceptions**, et c’est là que la nuance compte 👇  

---

## 🧠 1. Quand tu *n’as plus besoin* d’appels client → backend

Si ton objectif est :
- juste **afficher des données** (liste, page, profil, etc.),
- **précharger** ces données avant le rendu,
- et que ces données ne changent pas *en direct*,

alors ✅ tu peux **tout faire côté serveur (SSR)** dans Next.js.

👉 Exemple :
```tsx
// app/posts/page.tsx
export default async function Page() {
  const res = await fetch("http://localhost:4000/posts", { cache: "no-store" });
  const posts = await res.json();
  return <PostsList initialPosts={posts} />;
}
```

➡️ Ici, Next s’occupe d’appeler le backend à chaque chargement de page,  
le navigateur ne fait **aucune requête directe** vers le backend REST.

**Avantage :**
- Pas de CORS à gérer
- Pas d’exposition d’URL ou de tokens API
- SEO et performances excellentes

---

## ⚙️ 2. Quand tu *as encore besoin* d’appels client → backend

Certaines situations nécessitent toujours des appels API côté navigateur :

### 🧾 a. Actions utilisateur dynamiques
Quand tu veux **modifier ou recharger** des données sans recharger toute la page :
- création / mise à jour d’un post,
- bouton “recharger” ou “charger plus”,
- formulaires, like, etc.

Exemple :
```tsx
"use client";
async function recharger() {
  const res = await fetch("http://localhost:4000/posts");
  const data = await res.json();
  setPosts(data);
}
```

➡️ Ici, c’est **nécessaire** car l’utilisateur interagit avec la page après le rendu initial.

---

### 🔒 b. Actions nécessitant authentification côté navigateur
Si ton backend utilise un token JWT côté client ou un cookie d’auth :
- tu peux continuer à faire des `fetch()` depuis le client,
- ou passer par une **API Route Next.js** qui fait le proxy :

```tsx
// app/api/posts/route.ts
export async function GET(req: Request) {
  const res = await fetch("http://localhost:4000/posts", {
    headers: { Authorization: req.headers.get("authorization") || "" },
  });
  return Response.json(await res.json());
}
```

➡️ Le client appelle ensuite `/api/posts` sans connaître l’URL du backend.

---

## 📊 En résumé

| Cas d’usage | Où faire le `fetch` ? | Pourquoi |
|--------------|----------------------|-----------|
| Charger les données au premier rendu | 🖥️ **Serveur (SSR)** | Meilleur SEO, pas d’appel client |
| Filtrer / trier côté client (local) | ⚙️ **Client (React)** | Pas besoin d’appel backend |
| Recharger ou modifier des données | ⚙️ **Client** (direct ou via `/api`) | Interaction utilisateur |
| Auth ou proxy API | 🖥️ **Route API Next** | Sécurité, cacher les tokens |

---

## 🧩 Philosophie moderne Next.js

> L’idée est de **déplacer autant que possible la logique de données côté serveur**,  
et de **laisser le client gérer uniquement l’interactivité**.

---

Souhaites-tu que je te montre un petit exemple complet :  
➡️ **page SSR initiale + bouton "recharger" client** qui refait un appel vers ton backend ?  
(c’est souvent le mix parfait en pratique)'),
	(3339, '2025-11-06 16:30:12.875+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', 'f58b7313-3dfa-4679-b331-18bfaad4aa46', 'user', 'auto', 'c6bd2710-249f-444b-b9c4-963f42f93122', NULL, 'si je fais le chargement d''une page de donnée coté serveur
ensuite je veux pouvoir modifier cette donnée, de quel coté je dois faire ?'),
	(3340, '2025-11-06 16:30:13.5794+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', '20ecfd2e-7bb2-4ac0-976c-2a2422d84f52', 'assistant', 'gpt-5', 'f58b7313-3dfa-4679-b331-18bfaad4aa46', NULL, 'Excellent réflexe 👏 — tu touches là **le cœur du design d’une app Next.js moderne** :  
👉 *“Qui doit gérer la modification des données : le client, le serveur Next, ou le backend custom ?”*

La réponse dépend **de ce que tu veux faire exactement**, mais on peut dégager une règle claire :

---

## 🧭 Principe général

> 🔹 **Lecture** → côté serveur (Next.js SSR / Server Component)  
> 🔹 **Écriture / modification** → côté client (ou via une Server Action / API Route)

Pourquoi ?
- Le SSR ne sert qu’à **préparer l’affichage initial**.  
- Les modifications nécessitent souvent une **interaction utilisateur** → donc c’est **du côté client**.  
- Mais tu peux **faire passer la requête par Next.js** (API Route ou Server Action) au lieu d’appeler directement ton backend REST.

---

## ⚙️ 1. Exemple concret

Disons que tu as une page qui charge un “post” depuis ton backend :
```tsx
// app/posts/[id]/page.tsx
import EditPostForm from "./EditPostForm";

export default async function PostPage({ params }) {
  const res = await fetch(`http://localhost:4000/posts/${params.id}`, { cache: "no-store" });
  const post = await res.json();

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">Éditer le post</h1>
      <EditPostForm post={post} />
    </main>
  );
}
```

➡️ Ici, la **lecture** se fait côté serveur (SSR).

---

## 🧠 2. Modification côté client

Tu veux modifier le post (par ex. changer le titre).  
Tu le fais dans un **composant client**, car c’est une interaction utilisateur.

```tsx
// app/posts/[id]/EditPostForm.tsx
"use client";
import { useState } from "react";

export default function EditPostForm({ post }) {
  const [title, setTitle] = useState(post.title);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setSaving(true);

    const res = await fetch("/api/posts/" + post.id, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });

    setSaving(false);
    setMessage(res.ok ? "Sauvegardé ✅" : "Erreur ❌");
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <input
        className="border p-2 w-full rounded"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <button
        disabled={saving}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {saving ? "Sauvegarde..." : "Sauvegarder"}
      </button>
      {message && <p>{message}</p>}
    </form>
  );
}
```

---

## 🛡️ 3. Route proxy côté serveur (optionnel, recommandé)

Tu veux éviter d’exposer ton backend directement (`localhost:4000` ou `api.monsite.com`) →  
tu fais passer la requête via une **API Route Next.js** :

```ts
// app/api/posts/[id]/route.ts
export async function PUT(req, { params }) {
  const body = await req.json();
  const res = await fetch(`http://localhost:4000/posts/${params.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  return Response.json(data, { status: res.status });
}
```

➡️ Le navigateur appelle `/api/posts/:id`,  
➡️ Next.js transmet la requête à ton backend REST,  
➡️ et tu gardes la **sécurité** + la **souplesse du SSR**.

---

## 🔁 4. Cycle complet

| Étape | Où ? | Description |
|-------|------|-------------|
| 1 | Serveur Next.js | `fetch()` initial vers le backend REST → SSR de la page |
| 2 | Client | L’utilisateur modifie le formulaire |
| 3 | Client | Le composant client envoie un `PUT` vers `/api/posts/:id` |
| 4 | Serveur Next.js (API Route) | Transmet au backend REST |
| 5 | Backend REST | Met à jour la donnée en DB |
| 6 | Client | Affiche confirmation / recharge la donnée si besoin |

---

## 🧩 Variante moderne : Server Actions (Next.js 14+)

Next propose aussi une autre approche :  
👉 **les Server Actions**, qui te permettent de faire la mise à jour directement côté serveur *sans route API dédiée* :

```tsx
// app/posts/[id]/EditPostForm.tsx
"use client";

export default function EditPostForm({ post }) {
  async function saveAction(formData: FormData) {
    "use server";
    const title = formData.get("title");
    await fetch(`http://localhost:4000/posts/${post.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
  }

  return (
    <form action={saveAction}>
      <input name="title" defaultValue={post.title} />
      <button type="submit">Sauvegarder</button>
    </form>
  );
}
```

➡️ Ici, l’action de sauvegarde est **côté serveur Next**, appelée directement par le formulaire.  
Pas besoin de route `/api`, ni d’appel client manuel.

---

## ✅ En résumé

| Type d’opération | Où exécuter ? | Comment |
|------------------|----------------|---------|
| Lecture initiale (rendu de page) | 🖥️ **Serveur Next** | `fetch()` dans page.tsx |
| Interaction utilisateur (modifier, ajouter, supprimer) | ⚙️ **Client React** | `fetch()` vers `/api/...` ou Server Action |
| Communication backend | 🔒 **Next.js → backend REST** | Proxy via route API ou Server Action |
| Données sensibles / token secret | 🚫 Jamais côté client | Toujours dans code serveur Next |

---

Souhaites-tu que je te montre une version **Server Actions** complète (sans `/api`), pour voir la différence entre cette approche et la route API classique ?'),
	(3341, '2025-11-06 16:33:48.924+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', '1e052dfc-a081-486d-9ef5-ac4d795482e6', 'user', 'auto', '20ecfd2e-7bb2-4ac0-976c-2a2422d84f52', NULL, 'explique moi plus les serveur actions'),
	(3342, '2025-11-06 16:33:49.695281+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cbca7-5538-832a-9188-be618349aa57', 'b902126b-c06e-4088-93e4-08ed4254cf8f', 'assistant', 'gpt-5', '1e052dfc-a081-486d-9ef5-ac4d795482e6', NULL, 'Excellent 👏 — les **Server Actions** sont *une des plus grandes nouveautés* de **Next.js 13+ (et encore plus en 14/15)**.  
Elles changent profondément **comment tu fais interagir ton frontend et ton backend**.

---

## 🧠 En résumé simple

> 🔹 Les **Server Actions** te permettent d’exécuter du code **serveur** (Node.js)  
> depuis un **composant React**, *sans passer par une route API ni un fetch manuel.*

Tu écris une fonction **dans ton composant React**,  
tu y mets `"use server"`,  
et **Next.js l’exécute sur le serveur** au moment où tu l’appelles depuis le navigateur.

---

## 🧩 1. Pourquoi ça existe ?

Avant les Server Actions :

- Tu faisais une requête HTTP :
  ```tsx
  fetch("/api/posts", { method: "POST", body: ... })
  ```
- Il fallait créer une **API Route** `/api/posts/route.ts`
- Puis ton code backend appelait ta vraie API ou DB

➡️ C’était verbeux, dupliqué et pas typé.

Avec les **Server Actions**,  
➡️ tu supprimes l’étape “API Route”,  
➡️ tu appelles directement une **fonction serveur** depuis ton composant.

---

## ⚙️ 2. Exemple de base

Imaginons une page qui affiche une liste de posts, et un formulaire pour en ajouter un.

```tsx
// app/posts/page.tsx
import { revalidatePath } from "next/cache";

export default async function PostsPage() {
  const res = await fetch("http://localhost:4000/posts", { cache: "no-store" });
  const posts = await res.json();

  // 💡 Définition de l''action serveur
  async function addPost(formData: FormData) {
    "use server"; // indique à Next que cette fonction s''exécute côté serveur
    const title = formData.get("title");
    await fetch("http://localhost:4000/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    revalidatePath("/posts"); // force Next à recharger la page (SSR)
  }

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">Liste des posts</h1>
      <ul className="mb-6 space-y-2">
        {posts.map((p: any) => (
          <li key={p.id} className="p-3 border rounded">
            {p.title}
          </li>
        ))}
      </ul>

      <form action={addPost} className="space-x-2">
        <input
          type="text"
          name="title"
          placeholder="Nouveau post"
          className="border p-2 rounded"
        />
        <button className="bg-blue-600 text-white px-3 py-2 rounded">
          Ajouter
        </button>
      </form>
    </main>
  );
}
```

---

## 🔍 Ce qu’il se passe en coulisses

1. **Tu cliques sur le bouton “Ajouter”**
2. React envoie automatiquement le `FormData` au serveur Next (pas via `fetch()`)
3. Next appelle la fonction `addPost()` **sur le serveur**
4. Elle exécute du code Node.js (donc peut utiliser `fetch()`, Prisma, Mongo, etc.)
5. `revalidatePath("/posts")` force le rechargement de la page SSR → tu vois le nouveau post

---

## 🛡️ 3. Avantages clés

| Avantage | Détail |
|-----------|---------|
| 🔒 **Sécurité** | Le code s’exécute sur le serveur, donc tu peux y mettre des tokens, secrets, etc. |
| ⚡ **Moins de boilerplate** | Plus besoin de créer une route `/api/...` juste pour une action simple |
| 🧩 **Intégré à React** | Tu l’appelles via `<form action={maFonction}>` ou `useTransition()` |
| 🧱 **Typage TypeScript** | C’est du code local, donc les types sont partagés |
| 🔄 **Revalidation intégrée** | `revalidatePath()` ou `revalidateTag()` pour rafraîchir les données SSR |

---

## 💬 4. Appeler une Server Action sans formulaire

Tu peux aussi les appeler **depuis un événement React** (clic, etc.) :

```tsx
"use client";
import { experimental_useActionState } from "react";

export default function DeleteButton({ id, deleteAction }) {
  const [state, formAction] = experimental_useActionState(deleteAction, null);

  return (
    <form action={formAction}>
      <button type="submit" className="text-red-500">
        Supprimer
      </button>
    </form>
  );
}
```

Et côté serveur :

```tsx
// app/posts/actions.ts
"use server";

export async function deleteAction(formData: FormData) {
  const id = formData.get("id");
  await fetch("http://localhost:4000/posts/" + id, { method: "DELETE" });
  revalidatePath("/posts");
}
```

---

## 🧠 5. Quand préférer Server Actions ou API Routes ?

| Cas d’usage | Mieux avec… | Pourquoi |
|--------------|--------------|-----------|
| Action simple liée à un formulaire | ⚡ **Server Action** | Code direct, typé, SSR friendly |
| Appel depuis un client externe (mobile, front séparé) | 🌐 **API Route** | Besoin d’un endpoint HTTP public |
| Opération complexe ou multi-routes | ⚙️ **API Route ou backend custom** | Mieux pour séparer les responsabilités |
| Accès DB ou fetch avec secret | ✅ **Server Action** | Exécutée côté serveur sécurisé |

---

## 🚀 En résumé

| Tu veux... | Ce qu’il faut faire |
|-------------|---------------------|
| Charger des données → SSR | `fetch()` côté serveur |
| Modifier des données via formulaire | `async function action() { "use server" }` |
| Rafraîchir la page après update | `revalidatePath("/...")` |
| Garder compatibilité REST classique | `/api/...` |

---

En gros :  
> 🔥 Les Server Actions te permettent de **fusionner la logique frontend et backend léger** directement dans tes composants,  
> sans perdre la sécurité ni le typage.

---

Souhaites-tu que je te montre un **exemple complet CRUD (Create, Update, Delete)** utilisant **uniquement des Server Actions**, sans aucune route `/api` ?'),
	(3343, '2025-11-06 17:19:48.477658+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', '690cd89c-a294-8327-bb7b-670bd58fad15', 'd61b05c6-1c85-4b8d-a317-f1634aa369b1', 'assistant', 'gpt-5', 'ab7dd1c9-0b48-4bb3-b100-7cdf40155efe', NULL, 'Le style de composant que tu montres correspond à un **explorateur de fichiers hiérarchique** (ou **file tree / file explorer UI component**).  
C’est typiquement ce qu’on retrouve dans des environnements comme **VS Code**, **Notion**, ou **ChatGPT avec les projets**, où les fichiers et dossiers sont imbriqués.

---

### 💡 En termes techniques / design system :
Ce composant est souvent appelé :
- **Tree View** ou **Tree Component**
- **File Browser / File Explorer**
- **Nested Folder Structure**
- **Collapsible Sidebar Navigation**

---

### 🧩 Si tu veux le recréer (par ex. en React) :
Tu peux t’appuyer sur :
- **Radix UI / shadcn/ui** → avec le composant `Tree` ou une combinaison de `Accordion` et `List`
- **React Aria TreeView** (accessibilité complète)
- **MUI TreeView** (facile à intégrer)
- Ou le coder toi-même avec :
  ```jsx
  <ul>
    <li>📁 Personal
      <ul>
        <li>📁 Test
          <ul>
            <li>📄 Météo ?</li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
  ```

---

### ⚙️ Fonctions typiques de ce type de composant :
- Ouverture / fermeture de dossiers (toggle)
- Icônes dynamiques (📁 / 📄)
- Sélection d’un élément actif
- Drag & Drop (pour déplacer des fichiers)
- État de “draft” ou de “modifié”

---

Souhaites-tu que je te montre **un exemple de code React** (avec Tailwind + shadcn) pour reproduire exactement ce style visuel sombre et hiérarchique ?');


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."notifications" ("id", "created_at", "user_id", "read_at", "type", "title", "body", "metadata") VALUES
	(89, '2025-10-27 09:20:25.197166+00', '51eee0a1-8f20-4403-b5f1-0566375db20b', NULL, 'welcome_new_user', 'welcome_notification_title', 'welcome_notification_body', '{"action_url": "https://www.linkedin.com/company/104914264/admin/dashboard/", "action_type": "openUrl", "action_title_key": "followOnLinkedIn"}'),
	(91, '2025-11-09 22:29:53.376462+00', 'eff2a1fd-210c-4b44-9a6f-81af6534c3c8', NULL, 'welcome_new_user', 'welcome_notification_title', 'welcome_notification_body', '{"action_url": "https://www.linkedin.com/company/104914264/admin/dashboard/", "action_type": "openUrl", "action_title_key": "followOnLinkedIn"}');


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."organizations" ("id", "created_at", "name", "banner_url", "image_url", "website_url", "description") VALUES
	('19864b30-936d-4a8d-996a-27d17f11f00f', '2025-06-30 10:03:46.852824+00', 'Jaydai', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/organizations/jaydai_banner.png', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/organizations/jaydai_org_logo.png', 'https://jayd.ai', NULL),
	('45806a10-926d-4364-96a7-fd8ea5a09097', '2025-07-03 14:02:41.000394+00', 'Ai sister', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/organizations/Ai_sister_banner.jpg', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/organizations/ai_sisters_logo.jpg', 'https://www.aisisters.ai/', NULL),
	('b20a4e48-c968-440b-b31f-3e7bf6410265', '2025-07-06 18:59:13.655147+00', 'LNA SANTE ', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/organizations/lan-sante_banner.png', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/organizations/lna_sante_logo.png', 'https://www.lna-sante.com/', NULL),
	('b6321925-1998-4356-b352-1f23a7e79331', '2025-07-07 07:14:20.457586+00', 'Noovimo', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images//noovimo_brand.png', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images//noovimo_logo.png', 'https://www.noovimo.fr/', NULL),
	('f17ed11d-d5d4-4d0f-a4a5-afb49154e8bb', '2025-07-16 06:36:39.952391+00', 'Optimhome', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/organizations/banner_optimhomme.png', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/organizations/logo%20Optimhome.png', 'https://www.optimhome.com/fr', NULL),
	('f8d0fe34-32ff-4d90-87ed-28e83c50f953', '2025-07-17 14:50:37.287242+00', 'SFAF', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/organizations/sfaf_banner.png', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/organizations/SFAF_Logo.png', 'https://www.sfaf.com/', NULL),
	('a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '2025-09-07 08:29:12.996584+00', 'Paris Business Angels', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/pba_banner.png', 'https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/pba_logo.png', NULL, NULL);


--
-- Data for Name: prompt_blocks; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."prompt_blocks" ("id", "created_at", "company_id", "organization_id", "user_id", "type", "content", "title", "description", "published", "status", "team_ids", "workspace_type", "usage_count", "updated_at") VALUES
	('787c8164-4343-4340-8f31-e15323cd15e3', '2025-10-03 17:17:08.21494+00', NULL, NULL, '6d90f22e-dfa0-4b34-a88f-c4a533dc85ab', 'custom', '{"fr": "ddede"}', '{"fr": "ded"}', '{}', true, NULL, NULL, 'user', 0, NULL),
	('36904c65-0485-4867-899f-57a35e6d06fc', '2025-10-09 15:00:45.427876+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un directeur juridique avec plus de 30 ans d’expérience et une expertise unique en droit des affaires, gouvernance et conformité.\nTu es capable d’anticiper les risques, sécuriser les contrats et défendre les intérêts de l’entreprise."}', '{"custom": "Directeur Juridique"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('d16165c6-3b16-4bfe-b7af-3ffe09298485', '2025-10-03 17:16:37.017768+00', NULL, NULL, '6d90f22e-dfa0-4b34-a88f-c4a533dc85ab', 'example', '{"fr": "ceci est un test"}', '{"fr": "Test jbh"}', '{}', true, NULL, NULL, 'user', 0, NULL),
	('d9fbeca0-9ce7-4635-9bc8-b5dac94d056a', '2025-10-03 17:17:20.580673+00', NULL, NULL, '6d90f22e-dfa0-4b34-a88f-c4a533dc85ab', 'role', '{"fr": "dede"}', '{"fr": "ded"}', '{}', true, NULL, NULL, 'user', 0, NULL),
	('c3c5537b-fcae-4eff-b572-e606757cd7e3', '2025-10-05 13:49:11.121919+00', NULL, NULL, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 'role', '{"fr": "Quentoche p p p p p. p"}', '{"fr": "Teeest QB"}', '{"fr": "opopopop"}', true, NULL, NULL, 'user', 0, NULL),
	('66d31d06-a2d7-46ec-91a6-042f92564543', '2025-10-09 07:20:57.804889+00', NULL, NULL, '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un directeur stratégie avec plus de 30 ans d’expérience et une expertise unique en planification stratégique, transformation digitale et pilotage de la performance.\nTu es capable de définir une vision long terme, d’aligner les ressources et de transformer les ambitions en plans d’exécution concrets."}', '{"custom": "Directeur Stratégie"}', '{"custom": ""}', true, NULL, NULL, 'user', 0, NULL),
	('48900c7f-3ccf-46ca-a198-19b158438bc3', '2025-10-09 07:23:13.61055+00', NULL, NULL, '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un directeur commercial avec plus de 30 ans d’expérience et une expertise unique en stratégie de vente, management des équipes commerciales et développement de portefeuilles clients.\nTu es capable de concevoir et exécuter des stratégies de croissance rentables et durables."}', '{"custom": "Directeur commercial"}', '{"custom": ""}', true, NULL, NULL, 'user', 0, NULL),
	('1bcffbe1-b5d9-4774-ac35-0505ee4d2865', '2025-10-09 07:23:43.182478+00', NULL, NULL, '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un expert en communication et image de marque avec plus de 30 ans d’expérience et une expertise unique en storytelling, relations publiques et communication de crise.\nTu es capable de construire une identité forte, cohérente et inspirante à travers tous les canaux."}', '{"custom": "Directeur Communication"}', '{"custom": ""}', true, NULL, NULL, 'user', 0, NULL),
	('915a454b-335a-48ea-a91a-e248603102ee', '2025-10-09 14:54:44.665205+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un directeur stratégie avec plus de 30 ans d’expérience et une expertise unique en planification stratégique, transformation digitale et pilotage de la performance.\nTu es capable de définir une vision long terme, d’aligner les ressources et de transformer les ambitions en plans d’exécution concrets."}', '{"custom": "Directeur stratégie"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('3d80434f-d62a-47ce-817a-0d8375fa9344', '2025-10-09 14:55:12.173284+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un directeur commercial avec plus de 30 ans d’expérience et une expertise unique en stratégie de vente, management des équipes commerciales et développement de portefeuilles clients.\nTu es capable de concevoir et exécuter des stratégies de croissance rentables et durables."}', '{"custom": "Directeur Commercial"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('7cc6787d-0ca2-4c67-b55e-0181d8c55875', '2025-10-09 14:55:35.548323+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un expert en communication et image de marque avec plus de 30 ans d’expérience et une expertise unique en storytelling, relations publiques et communication de crise.\nTu es capable de construire une identité forte, cohérente et inspirante à travers tous les canaux."}', '{"custom": "Directeur communication "}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('b7b1b97d-2db8-40cf-823a-5b48438debf6', '2025-10-09 14:58:47.352518+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un Chief Technology Officer avec plus de 30 ans d’expérience et une expertise unique en architecture logicielle, IA et transformation numérique.\nTu es capable de concevoir des solutions technologiques robustes, évolutives et alignées sur la stratégie business."}', '{"custom": "CTO "}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('156616d8-1a84-42ef-95e4-04c09fcc0e20', '2025-10-09 14:59:52.26268+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un expert en ressources humaines avec plus de 30 ans d’expérience et une expertise unique en gestion des talents, leadership, culture d’entreprise et transformation organisationnelle.\nTu es capable d’aligner les dynamiques humaines avec la stratégie globale, en favorisant l’engagement, la performance et le bien-être au travail."}', '{"custom": "Directeur RH "}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('50fec40f-9685-4b55-9a36-148429fd9c80', '2025-10-09 15:00:22.21948+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un expert data avec plus de 30 ans d’expérience et une expertise unique en analyse de données, modélisation prédictive et stratégie data-driven.\nTu es capable d’extraire des insights à fort impact, d’optimiser la prise de décision et de transformer les données en leviers de croissance mesurables"}', '{"custom": "Directeur DATA"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('25c76f74-5d71-4465-adff-fc6e43d09be2', '2025-10-09 15:01:09.143383+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un directeur RSE avec plus de 30 ans d’expérience et une expertise unique en responsabilité sociétale, stratégie climat et innovation durable.\nTu es capable d’aligner la performance économique avec les objectifs environnementaux et sociaux."}', '{"custom": "Directeur RSE"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('7489dc2f-337d-48ae-822a-7097e8f579e2', '2025-10-09 15:06:54.990499+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'tone_style', '{"custom": "Utilise un ton professionnel, formel et objectif, sans prise de position émotionnelle. Le langage doit rester neutre et adapté à un contexte d’entreprise."}', '{"custom": "Professionnel & neutre "}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('a14e4aef-e03f-4a2e-ae75-970719f029f7', '2025-10-05 13:49:57.939151+00', NULL, NULL, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 'role', '{"fr": "loooool"}', '{"fr": "Toi"}', '{"fr": "oioio"}', true, NULL, NULL, 'user', 0, NULL),
	('cadfba85-ec55-4386-8f6d-86ea889c004d', '2025-10-09 14:56:00.327218+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'custom', '{"fr": "Jaydai est une solution xxxxxxx"}', '{"fr": "Jaydai"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('95c10148-bf35-4a9b-93fc-01bd328db368', '2025-10-09 15:07:36.562476+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'tone_style', '{"custom": "Adopte un ton pédagogique et clair, comme si tu devais expliquer le sujet à quelqu’un qui découvre le sujet pour la première fois. Utilise un langage simple, structuré et illustratif."}', '{"custom": "Pédagogique & clair"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('b1b27423-2e1f-498d-91a0-09d1af8e5209', '2025-10-09 15:08:11.259513+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'tone_style', '{"custom": "Utilise un ton dynamique et positif pour capter l’attention et motiver à passer à l’action. Sois inspirant et mets l’accent sur les bénéfices."}', '{"custom": "Engageant & motivant"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('71eee123-3164-4abf-857f-90013541499e', '2025-10-09 15:09:08.597875+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'tone_style', '{"custom": "Va droit au but avec un ton concis, clair et structuré. Supprime les détours et concentre-toi uniquement sur les points clés utiles à la prise de décision. "}', '{"custom": "Synthétique & direct"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('ee034505-8722-4488-860e-e30cc23efc44', '2025-10-09 15:09:40.476312+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'tone_style', '{"custom": "Utilise un ton bienveillant, humain et à l’écoute. Rassure l’interlocuteur, montre que tu comprends ses préoccupations et propose des réponses posées et apaisantes."}', '{"custom": "Empathique & rassurant"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('90f2dc5f-a0fc-4b50-9c49-5084286e02cd', '2025-10-09 15:10:23.815756+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'tone_style', '{"custom": "Adopte un ton formel, structuré et rigoureux. Le langage doit être précis, factuel et conforme aux codes du monde juridique ou réglementaire."}', '{"custom": "Sérieux & juridique"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('bfe40bbb-fa5a-4303-9dea-38fe62550f19', '2025-10-09 15:10:48.757814+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'tone_style', '{"custom": "Utilise un ton orienté “bénéfices client”. Sois persuasif sans être insistant. Mets en avant les avantages de manière claire et attractive."}', '{"custom": "Commercial & convaincant"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('7803025d-d35e-4f91-b76b-c4ebd86d054e', '2025-10-09 14:59:20.327883+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'custom', '{"fr": "Tu es un expert en cybersécurité avec plus de 30 ans d’expérience et une expertise unique en gestion des risques, conformité et sécurité des systèmes d’information.\nTu es capable de protéger les actifs numériques de l’entreprise et d’assurer la continuité de ses opérations."}', '{"fr": "Expert Cybersécurité"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('87f53df2-49d3-4393-90e4-fedbe5234300', '2025-10-10 09:54:43.742555+00', NULL, NULL, '0eaa7f45-1f7e-403b-84fc-f02d0f0e18a4', 'role', '{"custom": "test"}', '{"custom": "test"}', '{"custom": "test"}', true, NULL, NULL, 'user', 0, NULL),
	('0bf59be5-70a9-4331-ab9f-86badd2b77db', '2025-10-10 09:55:03.57154+00', NULL, NULL, '0eaa7f45-1f7e-403b-84fc-f02d0f0e18a4', 'role', '{"custom": "test"}', '{"custom": "test"}', '{"custom": "test"}', true, NULL, NULL, 'user', 0, NULL),
	('8f30821f-99f0-43d1-9733-bffae3689342', '2025-10-10 09:55:25.561145+00', NULL, NULL, '0eaa7f45-1f7e-403b-84fc-f02d0f0e18a4', 'context', '{"custom": "test"}', '{"custom": "test"}', '{"custom": "test"}', true, NULL, NULL, 'user', 0, NULL),
	('c645b312-b4cc-436d-9818-8a9a2acedde2', '2025-10-10 09:55:52.023862+00', NULL, NULL, '0eaa7f45-1f7e-403b-84fc-f02d0f0e18a4', 'constraint', '{"custom": "test"}', '{"custom": "test"}', '{"custom": "test"}', true, NULL, NULL, 'user', 0, NULL),
	('c5b64e68-b59b-435b-971d-cd8505a8dd5d', '2025-10-10 09:57:38.672783+00', NULL, NULL, '0eaa7f45-1f7e-403b-84fc-f02d0f0e18a4', 'audience', '{"custom": "test"}', '{"custom": "test"}', '{"custom": "test"}', true, NULL, NULL, 'user', 0, NULL),
	('fa263455-6c8f-42fc-9c76-c63d81519be4', '2025-10-10 13:37:32.082298+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'output_format', '{"custom": "Fournis un résumé exécutif en une page, destiné à un comité de direction ou un décideur. Va droit au but avec les faits, chiffres clés, recommandations et impacts business."}', '{"custom": "Mémo exécutif"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('7d9cf245-da59-44e3-8a97-2f83793b08c1', '2025-10-10 13:38:13.439959+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'output_format', '{"custom": "Présente la réponse sous forme de roadmap projet (par trimestre, mois ou étape). Pour chaque phase, détaille les objectifs, livrables et ressources nécessaires."}', '{"custom": "Roadmap "}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('4b429bd9-08bd-4889-b12a-90b19e8b0ccc', '2025-10-10 13:38:47.889163+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'output_format', '{"custom": "Donne une analyse comparative entre plusieurs acteurs ou solutions, structurée en tableau avec critères clés (prix, fonctionnalités, différenciateurs, etc.). Ajoute une interprétation synthétique en conclusion."}', '{"custom": "Benchmark"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('6aab3164-f1dc-4d40-a814-90100dc0345c', '2025-10-10 13:39:24.854625+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'output_format', '{"custom": "Structure ta réponse sous forme de plan logique (I., II., III., etc.) avec des sous-parties claires. Chaque partie doit traiter un aspect distinct du sujet."}', '{"custom": "Plan détaillé"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('1fd35e96-fa89-4f84-921b-e0d54f291920', '2025-10-10 13:39:46.333188+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'output_format', '{"custom": "Structure ta réponse en bullet points clairs, concis et organisés par thème. Chaque point doit apporter une information utile sans phrase inutile."}', '{"custom": "Bullet points synthétiques"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('3379bf84-2c5b-4c89-ba4f-a80c1ebaf108', '2025-10-10 13:41:11.462644+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'output_format', '{"custom": "Organise ta réponse sous forme de tableau clair et lisible, avec des colonnes bien définies (critères, options, évaluations, données clés) pour permettre une lecture rapide et une comparaison efficace."}', '{"custom": "Tableau structuré"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('0ff50400-07bb-4cd6-92aa-b167833cb0d9', '2025-10-10 13:42:40.665428+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'audience', '{"custom": "La réponse est destinée à un comité de direction. Utilise un langage clair, stratégique et concis, avec une mise en avant des enjeux, impacts business et décisions à prendre."}', '{"custom": "Comité de direction"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('5616b329-effb-48cd-a212-0254c4b19ee0', '2025-10-10 13:43:11.562733+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'audience', '{"custom": "Adresse-toi à un manager qui doit prendre des décisions concrètes rapidement. Mets l’accent sur les actions, les résultats attendus et les ressources nécessaires."}', '{"custom": "Manager opérationnel"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('185ed816-834d-463c-95ab-a9b9012dae34', '2025-10-10 13:43:29.954734+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'audience', '{"custom": "Rédige une réponse orientée collaboration. Utilise un ton clair, structuré et inclusif. Mets en évidence les étapes, les rôles, les dépendances et les livrables."}', '{"custom": "Équipe projet"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('ae178054-b4c4-457a-a8bd-2ff65fd6eccd', '2025-10-10 13:43:54.051075+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'audience', '{"custom": "Utilise un ton pédagogique, bienveillant et accessible. Prends le temps d’expliquer les concepts clés et les attentes sans complexité inutile."}', '{"custom": "Collaborateur junior"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('8eaae545-133b-49c3-9ce3-d033c00761c5', '2025-10-10 13:44:37.829947+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'audience', '{"custom": "Adresse-toi à un acteur externe impliqué dans un projet commun. Sois clair sur les objectifs, les responsabilités partagées, les délais et les livrables attendus."}', '{"custom": "Partenaire ou prestataire"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('3c996e72-e336-40c0-8ebe-7854c8554b28', '2025-10-10 14:08:27.375069+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'custom', '{"custom": "Critères\tHubSpot\tSalesforce\tPipedrive\nPrix mensuel\t50 €/utilisateur\t75 €/utilisateur\t25 €/utilisateur\nFacilité d’utilisation\t⭐⭐⭐⭐\t⭐⭐⭐\t⭐⭐⭐⭐\nIntégrations\t+ de 500\tTrès nombreuses\tMoins de 200\nPersonnalisation\tMoyenne\tÉlevée\tMoyenne\nSupport client\tChat & Email\t24/7 téléphone\tChat uniquement"}', '{"custom": "Exemple de tableau comparatif"}', '{"custom": null}', true, NULL, NULL, 'organization', 10, NULL),
	('74c5a23f-0b29-425d-b58a-364b11ac4d82', '2025-10-10 13:48:20.244568+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'constraint', '{"custom": "- Utilise uniquement des sources officielles et reconnus : texte de loi, communiqués de presse officiels , site spécialisé et reconnu, site web des entreprises\n- Utilise des sources d''information reconnues en fonction du pays de la recherche\n- Pour l''actualité, préfère les articles datant de moins de 12 mois (utilise des sources plus vieilles uniquement si cela est pertinant)\n- Évite les blogs personnels, forums ou sources non vérifiables\n- N''utilise pas Wikipédia comme source principale, mais seulement comme point de départ\n- Vérifie systématique la cohérence des informations entre plusieurs sources quand c''est possible"}', '{"custom": "Validation des sources web "}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('618e3a04-0027-44d2-8672-40cf92af1d52', '2025-10-10 13:49:40.935569+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'custom', '{"custom": "- Cite l''ensemble des sources utilisés à chaque moment de ton analyse \n- Assure toi que l''ensemble des liens soit cliquable et qu''il existe \n- N''invente rien "}', '{"custom": "Citation des sources web "}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('33c41f8f-2e0d-43fe-a6e8-b309c34edc1c', '2025-10-10 13:50:05.340212+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'constraint', '{"custom": "- Cite l''ensemble des sources utilisés à chaque moment de ton analyse \n- Assure toi que l''ensemble des liens soit cliquable et qu''il existe \n- N''invente rien "}', '{"custom": "Citation des sources"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('faf5ef0d-d9f0-41e1-a6f0-8b909238a784', '2025-10-10 13:54:13.102235+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'constraint', '{"custom": "Évite les formulations vagues ou génériques. Chaque point évoqué doit être concret, argumenté ou illustré par un exemple précis."}', '{"custom": "Pas de généralités"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('0e39ebf4-c32e-4f93-bb3c-012e0ddd4621', '2025-10-10 13:55:02.789823+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'constraint', '{"custom": "N’inclus aucun scénario hypothétique ou spéculatif non étayé. Reste strictement factuel."}', '{"custom": "Pas de contenu spéculatif"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('f61eb78f-bb37-4d44-8eca-0dd685742109', '2025-10-10 13:56:16.321849+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'constraint', '{"custom": "Si des limites, incertitudes ou zones grises existent, mentionne-les pour une lecture transparente."}', '{"custom": "Inclure les limites de la réponse"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('5decc657-7b34-4ac8-9e6b-e55b33e794c9', '2025-10-10 13:58:27.776576+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'goal', '{"custom": "Ton objectif est de m''aider à organiser mes idées de façon logique, hiérarchisée et synthétique pour faciliter leur expression ou présentation."}', '{"custom": "Structurer mes idées efficacement"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('96cf0a60-2bb4-4886-a09e-bc811eb51d18', '2025-10-10 14:06:58.83802+00', NULL, NULL, 'e1e08a40-7482-46e0-87dc-890212ff9148', 'example', '{"custom": "Objet : Relance – Proposition de collaboration\n\nBonjour Madame Lefèvre,\n\nJe me permets de revenir vers vous concernant notre proposition envoyée le 25 septembre. Nous serions ravis d’échanger avec vous pour approfondir les besoins de votre équipe et adapter notre offre en conséquence.\n\nSeriez-vous disponible cette semaine pour un court échange de 15 minutes ?  \nDans l’attente de votre retour, je reste à votre disposition.\n\nBien cordialement,  \nThomas Dubois  \nResponsable Commercial – Axiom Solutions"}', '{"custom": "Exemple : Mail de relance client "}', '{"custom": null}', true, NULL, NULL, 'user', 0, NULL),
	('451bdc86-a0bc-458e-abf7-37a5f2e3d059', '2025-10-10 15:45:38.501685+00', NULL, NULL, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 'context', '{"custom": "okkk"}', '{"custom": "okkkk"}', '{"custom": ""}', true, NULL, NULL, 'user', 0, NULL),
	('0e3a5a47-5bad-46c8-ab0a-9f7c2859f532', '2025-10-10 15:45:53.175654+00', NULL, NULL, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 'custom', '{"custom": "dfzbzdf"}', '{"custom": "dfhzd"}', '{"custom": ""}', true, NULL, NULL, 'user', 0, NULL),
	('79dd67f4-ebed-4171-8076-23126aaa4157', '2025-10-10 14:07:39.111399+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'example', '{"custom": "Objet : Relance – Proposition de collaboration\n\nBonjour Madame Lefèvre,\n\nJe me permets de revenir vers vous concernant notre proposition envoyée le 25 septembre. Nous serions ravis d’échanger avec vous pour approfondir les besoins de votre équipe et adapter notre offre en conséquence.\n\nSeriez-vous disponible cette semaine pour un court échange de 15 minutes ?  \nDans l’attente de votre retour, je reste à votre disposition.\n\nBien cordialement,  \nThomas Dubois  \nResponsable Commercial – Axiom Solutions"}', '{"custom": "Mail de relance - Client "}', '{"custom": null}', true, NULL, NULL, 'organization', 10, NULL),
	('02f1da5a-f189-4bd0-8db2-5c1994716a99', '2025-10-10 14:03:30.361767+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'context', '{"custom": "Je travaille dans l''entreprise suivante : \n[Indique le nom de ton entreprise et décris là le plus précisément possible]"}', '{"custom": "Description de mon entreprise"}', '{"custom": null}', true, NULL, NULL, 'organization', 10, NULL),
	('df83a4d7-5725-4c40-a0f8-8b4723d6d238', '2025-10-10 14:01:03.051271+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'custom', '{"custom": "Ton objectif est de me fournir une synthèse des dernières tendances, chiffres et articles fiables sur le sujet suivant : [à compléter]."}', '{"custom": "Faire une veille sur un sujet donné"}', '{"custom": null}', true, NULL, NULL, 'organization', 10, NULL),
	('7b92fabf-9861-4a78-af9a-f41515c9b399', '2025-10-10 14:00:26.22043+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'goal', '{"custom": "Aide-moi à rédiger un compte-rendu professionnel, clair et structuré avec décisions, actions et responsables associés."}', '{"custom": "Structurer un compte-rendu de réunion"}', '{"custom": null}', true, NULL, NULL, 'organization', 11, NULL),
	('9cc1b4f3-78e7-427d-bf39-a5990301215a', '2025-10-10 14:00:02.074714+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'goal', '{"custom": "Ton objectif est de m’aider à rédiger une réponse claire, professionnelle et adaptée au contexte de l’email reçu."}', '{"custom": "Rédiger une réponse professionnelle à un email"}', '{"custom": null}', true, NULL, NULL, 'organization', 212, NULL),
	('04633619-c97b-4d88-a127-9d351f68642e', '2025-10-10 13:59:05.980902+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'custom', '{"custom": "Ton objectif est de m’aider à préparer un discours ou une présentation impactante et bien structurée."}', '{"custom": "Préparer une prise de parole "}', '{"custom": null}', true, NULL, NULL, 'organization', 2, NULL),
	('036aa0d0-e4b8-427b-a449-775214567ced', '2025-10-14 23:58:34.552106+00', NULL, NULL, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 'custom', '{"custom": "fwerferf"}', '{"custom": "frefre"}', '{"custom": "erfref"}', true, NULL, NULL, 'user', 0, NULL),
	('112ff459-e400-4d0b-a6ed-6bc95e5ec2ca', '2025-10-15 11:50:51.474352+00', NULL, 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un Business Angel expérimenté, avec plusieurs années d’expérience, un large portefeuille d’investissements et un œil affûté pour repérer les 0,1 % de startups les plus prometteuses. Tu évalues chaque projet avec un haut niveau d’exigence, en recherchant : une équipe exceptionnelle, une traction démontrée, un marché immense, une différenciation claire et une capacité d’exécution rare. Ton rôle est d’aider à distinguer les projets d’exception de ceux simplement “bons”."}', '{"custom": "Business Angel expérimenté (top 0,1 %)"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('ce24fbac-5814-4b76-aafd-e1b1ffba0d1e', '2025-10-15 11:51:29.711932+00', NULL, 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un expert en modèles économiques de startups. Ton rôle est d’évaluer la viabilité, la scalabilité et la rentabilité du business model en fonction du marché et de la stratégie."}', '{"custom": "Expert en business model startup"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('e6e1bc64-022d-4843-bd8e-61f66aedc8d1', '2025-10-15 11:52:19.434078+00', NULL, 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'role', '{"custom": "Tu es un analyste en capital-risque spécialisé dans l’évaluation de startups early-stage. Tu maîtrises la lecture critique de pitch decks, de business plans financiers et de plans de croissance. Ton rôle est de fournir une analyse claire et rationnelle du potentiel du projet."}', '{"custom": "Analyste expérimenté early-stage"}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('9350d8c0-9323-4a4c-8e25-6311bcbedbe9', '2025-10-15 11:56:12.962274+00', NULL, 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'audience', '{"custom": "La réponse est adressée au fondateur d’une startup en levée de fonds. Elle doit être constructive, claire, professionnelle, sans jugement définitif."}', '{"custom": "Porteur de projet "}', '{"custom": null}', true, NULL, NULL, 'organization', 0, NULL),
	('df6d9113-7701-4cb7-a8e7-8d0a0c0d508b', '2025-11-05 17:05:20.92368+00', NULL, NULL, '478b7491-ff6c-490b-982c-a4dc866dcefc', 'tone_style', '{"custom": "COmbien fait -il a [ville] ?"}', '{"custom": "BLoqué"}', '{"custom": ""}', true, NULL, NULL, 'user', 0, NULL);


--
-- Data for Name: prompt_folders; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."prompt_folders" ("created_at", "user_id", "organization_id", "parent_folder_id", "title", "description", "company_id", "workspace_type", "id") VALUES
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Startup", "fr": "Startup"}', '{}', NULL, 'organization', '6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Starter", "fr": "Starter"}', '{}', NULL, 'organization', '7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Daily", "fr": "Daily"}', '{}', NULL, 'organization', '22b1127d-b4e0-4153-94b5-78155021e8a4'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Marketing", "fr": "Marketing"}', '{}', NULL, 'organization', '6adffa50-59c0-4d85-9b35-9a7e20e69126'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Investment", "fr": "Investissement"}', '{}', NULL, 'organization', 'd1563751-2b27-4902-a364-291348bbb4ad'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "HR", "fr": "RH"}', '{}', NULL, 'organization', '0a1409da-eb89-41f1-b835-247b14f1dd5c'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Personal Development", "fr": "Développement personnel"}', '{}', NULL, 'organization', 'dc3fbf96-3401-44a3-ac6c-1ff26e462727'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Image", "fr": "Image"}', '{}', NULL, 'organization', '58ac2937-c229-488d-a8fb-f995f8665e49'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Real Estate", "fr": "Immobilier"}', '{}', NULL, 'organization', 'd8be3245-7cf4-4425-9f7c-bde74bf8b91c'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Training", "fr": "Formation"}', '{}', NULL, 'organization', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Decision Making", "fr": "Prise de décision"}', '{}', NULL, 'organization', '6ddb4752-d985-412c-9cb9-173b86f2b45c'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "LinkedIn", "fr": "Linkedin"}', '{}', NULL, 'organization', '0cf52ff6-0b38-4710-a754-b86fd2c9982a'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Legal", "fr": "Juridique"}', '{}', NULL, 'organization', '555b372f-12c1-47d5-8026-aed205b5b5b8'),
	('2025-09-16 14:41:01.452614+00', NULL, '19864b30-936d-4a8d-996a-27d17f11f00f', NULL, '{"en": "Job Search", "fr": "Trouver un emploi"}', '{}', NULL, 'organization', '560f56ff-2086-4cf2-b78c-cad246d5cb51'),
	('2025-09-16 21:23:19.184417+00', NULL, 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', NULL, '{"en": "Business Model & Finance"}', '{}', NULL, 'organization', 'd522f0f3-e893-4bd5-b2e4-d28dfbbb298b'),
	('2025-09-16 21:20:25.216869+00', NULL, 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', NULL, '{"en": "Equipe fondatrice"}', '{}', NULL, 'organization', 'a330b6ac-47f8-4a26-9871-7d0937241049'),
	('2025-09-16 20:59:33.044523+00', NULL, 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', NULL, '{"en": "Analyse du Produit"}', '{}', NULL, 'organization', '78812c7e-254f-4031-90d8-fe123691b65b'),
	('2025-09-16 17:14:36.4582+00', NULL, 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', NULL, '{"fr": "Marché & Concurrence"}', '{"fr": "Dossier regroupant les prompts permettant de réaliser des études de marché et concurrence"}', NULL, 'organization', 'c37fb64a-e55c-4a39-a734-a5590d1d8192'),
	('2025-09-16 17:13:22.090548+00', NULL, 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', NULL, '{"en": "Etude approfondie"}', '{"fr": "Dossier regroupant les prompts à utiliser dans le mode \"Deep Research\" de ChatGPT"}', NULL, 'organization', '6c5ca58d-d07e-4db7-bc3f-8083c8f5a0c4'),
	('2025-10-10 08:19:23.296746+00', '0eaa7f45-1f7e-403b-84fc-f02d0f0e18a4', NULL, NULL, '{"fr": "Test Test Gotti"}', '{"fr": "test test gotti"}', NULL, 'user', '96090891-edb7-4145-a658-d3b6d39b8cb1'),
	('2025-10-10 12:51:53.448222+00', 'e1e08a40-7482-46e0-87dc-890212ff9148', NULL, NULL, '{"fr": "Bonjour"}', '{}', NULL, 'user', '3f52fc38-251e-464f-a851-d645850f43f8'),
	('2025-10-10 12:52:12.00789+00', 'e1e08a40-7482-46e0-87dc-890212ff9148', NULL, NULL, '{"fr": "Dossier"}', '{"fr": "yes"}', NULL, 'user', '735f1b02-e8bc-49f6-abb6-92d17e0c29c5'),
	('2025-10-10 12:57:22.28672+00', 'e1e08a40-7482-46e0-87dc-890212ff9148', NULL, NULL, '{"fr": "Jaydai"}', '{}', NULL, 'user', '8d88474c-dbd0-4e72-af83-a891a46f3430'),
	('2025-10-10 13:27:15.566552+00', 'e1e08a40-7482-46e0-87dc-890212ff9148', NULL, NULL, '{"fr": "Quentin"}', '{}', NULL, 'user', 'b937047a-0054-4f46-b5dc-4d62432f1e6e'),
	('2025-10-10 13:28:26.832005+00', 'e1e08a40-7482-46e0-87dc-890212ff9148', NULL, NULL, '{"fr": "rfrfr"}', '{}', NULL, 'user', 'a9fe4054-69d1-4ee3-9d5f-f74515d4d849'),
	('2025-10-10 16:58:13.787021+00', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, NULL, '{"fr": "ooo"}', '{"fr": "ko"}', NULL, 'user', '58ad39f3-96c8-4a20-b949-7ae831d8f8a1'),
	('2025-10-10 16:59:56.141189+00', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, NULL, '{"fr": "k;"}', '{}', NULL, 'user', 'ff410f0d-0646-4cdf-8449-f8e4327b4a15'),
	('2025-10-10 09:47:41.123631+00', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, NULL, '{"fr": "alsl"}', '{}', NULL, 'user', '6a9b3dd6-ae83-44f5-baca-e4a5ae3339ad'),
	('2025-10-15 06:33:40.395455+00', '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, NULL, '{"fr": "Bonjour"}', '{}', NULL, 'user', '6d5ffe97-39b0-4c8f-a461-aca582a52644'),
	('2025-10-15 10:34:54.92354+00', '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, NULL, '{"fr": "Jaydai"}', '{}', NULL, 'user', 'b9a5ca95-8a46-40ba-aee6-44d5b19191ea'),
	('2025-10-15 10:47:03.208729+00', '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, NULL, '{"en": "Perso"}', '{}', NULL, 'user', '3be04320-9714-4794-a8fc-9143eecc8225'),
	('2025-10-15 15:36:15.340476+00', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, NULL, '{"fr": "Invest AI"}', '{}', NULL, 'user', '843cd560-d50e-4c31-bb7d-9bd38da1b117'),
	('2025-10-15 15:40:09.513134+00', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', NULL, '{"en": "test"}', '{}', NULL, 'organization', '69d989da-b8bb-42b2-8329-4a7ce2cac53c'),
	('2025-10-16 08:04:27.605602+00', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'f8d0fe34-32ff-4d90-87ed-28e83c50f953', NULL, '{"fr": "Analyse financière"}', '{}', NULL, 'organization', '955c551e-f7e1-4950-a87c-7f4b57578bd5'),
	('2025-10-16 09:28:06.317675+00', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'f8d0fe34-32ff-4d90-87ed-28e83c50f953', NULL, '{"en": "ESG & finance durable"}', '{}', NULL, 'organization', '12ac27d9-7b89-4e2a-9a23-083a84d503c1'),
	('2025-10-16 09:39:58.611475+00', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'f8d0fe34-32ff-4d90-87ed-28e83c50f953', NULL, '{"en": "Analyse sectorielle"}', '{}', NULL, 'organization', 'f4e4127b-6d44-40d6-830b-db326e0c03a1'),
	('2025-10-27 09:41:37.187018+00', '51eee0a1-8f20-4403-b5f1-0566375db20b', NULL, NULL, '{"fr": "test"}', '{}', NULL, 'user', '04332fbf-3ade-4941-a9bc-079687d63ec7'),
	('2025-11-05 16:51:50.516304+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', NULL, NULL, '{"fr": "Test"}', '{"fr": "il fait beau dehors"}', NULL, 'user', '156e6146-9aa7-488a-ba08-828e31ff7023');


--
-- Data for Name: prompt_templates; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."prompt_templates" ("created_at", "tags", "last_used_at", "path", "workspace_type", "usage_count", "user_id", "company_id", "description", "organization_id", "title", "team_ids", "is_free", "updated_at", "id", "folder_id", "author_id", "current_version_id") VALUES
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "SEO content", "fr": "Contenu SEO "}', NULL, true, '2025-09-25 13:25:46.642239+00', 'bd51517d-a8af-4f04-ae3e-40546d00df26', '6adffa50-59c0-4d85-9b35-9a7e20e69126', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "KPI Business", "fr": "KPI Business"}', NULL, true, '2025-09-25 13:25:18.266228+00', 'ad93408f-a7ea-49eb-9ddb-b2f2307347bc', '6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Cooking recipes", "fr": "Recettes de cuisine"}', NULL, true, '2025-09-25 13:25:26.761626+00', 'a85a49a7-68e2-4bd6-96fd-108cbd90acbc', '22b1127d-b4e0-4153-94b5-78155021e8a4', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Find a restaurant", "fr": "Trouver un restaurant "}', NULL, true, '2025-09-25 13:25:28.144961+00', '4586c776-517b-429d-b65d-452d30bb822e', '22b1127d-b4e0-4153-94b5-78155021e8a4', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Find a movie or TV show", "fr": "Trouver un film ou une série "}', NULL, true, '2025-09-25 13:25:29.363479+00', 'cc101322-76e3-4b6e-9f07-7f2ae1cd776e', '22b1127d-b4e0-4153-94b5-78155021e8a4', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Audit Marketing ", "fr": "Audit Marketing "}', NULL, true, '2025-09-25 13:25:30.691216+00', '4f1d934b-9cce-4528-98c0-0b8cb94a733e', '6adffa50-59c0-4d85-9b35-9a7e20e69126', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Analyse d''audience ", "fr": "Analyse d''audience "}', NULL, true, '2025-09-25 13:25:31.911942+00', '7d0df14e-92cf-425c-8f9f-742055205d6d', '6adffa50-59c0-4d85-9b35-9a7e20e69126', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Investor questions", "fr": "Interrogations Investisseurs"}', NULL, true, '2025-09-25 13:25:33.183796+00', '6a579ca5-8484-4a1e-aaa6-544ed0a8df51', '6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Positionnement de marque ", "fr": "Positionnement de marque "}', NULL, true, '2025-09-25 13:25:37.964561+00', '632ce61c-c362-4818-9760-037e648dda9b', '6adffa50-59c0-4d85-9b35-9a7e20e69126', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Defining your personas", "fr": "Définir ses personas "}', NULL, true, '2025-09-25 13:25:49.052966+00', 'a693f2f7-c30b-43ca-af9a-a129ded254c9', '6adffa50-59c0-4d85-9b35-9a7e20e69126', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Idées de noms & slogans", "fr": "Idées de noms & slogans"}', NULL, true, '2025-09-25 13:26:54.001277+00', 'fd4e3c39-c920-4671-89f3-f9266b482b16', '6adffa50-59c0-4d85-9b35-9a7e20e69126', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Market trends", "fr": "Tendances d''un marché "}', NULL, true, '2025-09-25 13:26:54.001277+00', '9cd57bf9-a161-4ef4-a97b-e2d83442dcb2', 'd1563751-2b27-4902-a364-291348bbb4ad', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Stock performance", "fr": "Performance d''une action "}', NULL, true, '2025-09-25 13:26:54.001277+00', '1371c1fe-e643-4b6b-b1f1-c326946782f8', 'd1563751-2b27-4902-a364-291348bbb4ad', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Market risk analysis", "fr": "Analyse de risque d''un marché"}', NULL, true, '2025-09-25 13:26:54.001277+00', '2b358b90-5817-49dd-bb43-a401ca347cec', 'd1563751-2b27-4902-a364-291348bbb4ad', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "LinkedIn content strategy", "fr": "Stratégie de contenu LinkedIn"}', NULL, false, '2025-09-25 13:25:10.160267+00', '9b76e349-6060-4703-beb8-881063e4bca5', '0cf52ff6-0b38-4710-a754-b86fd2c9982a', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "SEO optimization of images", "fr": "Optimisation SEO d''images"}', NULL, true, '2025-09-25 13:26:15.18616+00', 'e9ce5553-6df9-4b49-b5f8-4fe57bb1c072', '58ac2937-c229-488d-a8fb-f995f8665e49', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Creating visuals for social media", "fr": "Création de visuels pour réseaux sociaux"}', NULL, true, '2025-09-25 13:26:17.187307+00', 'd2db080f-39ba-437e-89be-daf175bbd18e', '58ac2937-c229-488d-a8fb-f995f8665e49', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Créer un support psychoéducatif", "fr": "Créer un support psychoéducatif"}', NULL, true, '2025-09-25 13:26:54.001277+00', '5b77609c-96d1-45fb-bf95-a0552b364e19', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "E-commerce product photography", "fr": "Photographie produit e-commerce"}', NULL, true, '2025-09-25 13:26:54.001277+00', '5625c1ed-3754-4fbf-b41b-4a2df7123595', '58ac2937-c229-488d-a8fb-f995f8665e49', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "LinkedIn for recruiters", "fr": "LinkedIn pour recruteurs"}', NULL, false, '2025-09-25 13:26:54.001277+00', 'f6b5702e-293d-459b-97e1-294070f765bc', '0cf52ff6-0b38-4710-a754-b86fd2c9982a', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Impact of current events on an industry", "fr": "Impact d''une actualité sur une industrie "}', NULL, true, '2025-09-25 13:26:54.001277+00', '5172d621-46af-45c5-ba5a-a6d147f00330', 'd1563751-2b27-4902-a364-291348bbb4ad', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Job offer promise", "fr": "Promesse d''embauche "}', NULL, true, '2025-09-25 13:26:54.001277+00', 'f389a60f-9669-4d8c-9241-edd0693ac307', '0a1409da-eb89-41f1-b835-247b14f1dd5c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Case study - Job interview", "fr": "Etude de cas - entretien d''embauche "}', NULL, true, '2025-09-25 13:26:54.001277+00', 'afcbeb81-fa5b-4960-a2c3-b6da445ca375', '0a1409da-eb89-41f1-b835-247b14f1dd5c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Annual review framework", "fr": "Trame entretien annuel "}', NULL, true, '2025-09-25 13:26:54.001277+00', '2cd6d38d-fc47-4ca1-8933-72ffef158b57', '0a1409da-eb89-41f1-b835-247b14f1dd5c', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, '2025-10-21 13:21:16.471943+00', NULL, 'organization', 1, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Documentary research", "fr": "Recherche documentaire "}', NULL, true, '2025-10-21 13:21:16.471943+00', '585316ae-62ab-490f-a422-e79d3fab6f3b', '7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, '2025-10-15 09:38:12.364954+00', NULL, 'organization', 1, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Plan my vacation", "fr": "Planifier mes vacances"}', NULL, true, '2025-10-15 09:38:12.364954+00', '0848ae99-bf62-4652-a64c-8b9a2051cf7c', '22b1127d-b4e0-4153-94b5-78155021e8a4', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, '2025-10-10 06:34:35.462062+00', NULL, 'organization', 1, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Professional training network", "fr": "Réseau professionnel formation"}', NULL, true, '2025-10-10 06:34:35.462062+00', '83829da5-294a-4199-96f3-101518e323f3', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, '2025-10-10 07:27:42.045475+00', NULL, 'organization', 1, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Explain a complex subject", "fr": "Expliquer un sujet complexe "}', NULL, true, '2025-10-10 07:27:42.045475+00', 'b4c419ca-e935-4036-b5a1-c8e1e2043684', '7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, '2025-10-22 16:03:23.073183+00', NULL, 'organization', 14, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Prospect / client profile", "fr": "Fiche prospect / client"}', NULL, true, '2025-10-22 16:03:23.073183+00', '92e61ff0-69a7-48b2-b118-4e6b065b67b5', '6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, '2025-10-14 08:15:16.082322+00', NULL, 'organization', 2, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Legal Analysis", "fr": "Analyse juridique"}', NULL, true, '2025-10-14 08:15:16.082322+00', 'f968318e-bcf5-426c-8e69-1deba4dad748', '6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, '2025-10-15 09:45:08.212096+00', NULL, 'organization', 1, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Document Analysis", "fr": "Analyse d''un document"}', NULL, true, '2025-10-15 09:45:08.212096+00', '84f09be6-bf52-4654-b984-13e8c98cf275', '7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, '2025-10-21 09:03:08.227761+00', NULL, 'organization', 2, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Customer FAQ", "fr": "FAQ Client "}', NULL, true, '2025-10-21 09:03:08.227761+00', '0e0be45b-b2e1-4e97-8c7e-d159767314d4', '6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64', NULL, NULL),
	('2025-07-23 15:09:40.207746+00', NULL, '2025-10-22 16:03:12.108688+00', NULL, 'organization', 4, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Deck challenge", "fr": "Challenger son deck "}', NULL, true, '2025-10-22 16:03:12.108688+00', '5712dd34-0245-4908-810b-753761ba9d21', '6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Job offer", "fr": "Offre de job "}', NULL, true, '2025-09-25 13:26:54.001277+00', 'aa5a06e9-0c56-4ba7-8fd5-7931806378a0', '0a1409da-eb89-41f1-b835-247b14f1dd5c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Preparing for a job interview", "fr": "Préparer un entretien d''embauche "}', NULL, true, '2025-09-25 13:26:54.001277+00', '1a1002b6-5838-4420-ac33-568e4050a5ca', '0a1409da-eb89-41f1-b835-247b14f1dd5c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Overcoming limiting beliefs", "fr": "Surmonter une croyance limitante "}', NULL, false, '2025-09-25 13:26:54.001277+00', '2a4bbcca-4db8-48da-84f9-0fd4ca99782e', 'dc3fbf96-3401-44a3-ac6c-1ff26e462727', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Stress management", "fr": "Gestion du stress "}', NULL, false, '2025-09-25 13:26:54.001277+00', 'c156565f-32b8-4e87-8681-39769103ed6c', 'dc3fbf96-3401-44a3-ac6c-1ff26e462727', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Managing conflicts", "fr": "Gérer un conflit "}', NULL, false, '2025-09-25 13:26:54.001277+00', '3e1804a2-1ddd-498a-ba45-7614c3418dc5', 'dc3fbf96-3401-44a3-ac6c-1ff26e462727', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Personality analysis", "fr": "Analyse de sa personnalité "}', NULL, false, '2025-09-25 13:26:54.001277+00', '74f8c44a-2679-4264-ba95-bc6d3c759d53', 'dc3fbf96-3401-44a3-ac6c-1ff26e462727', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Generate your starter pack", "fr": "Générer son starter Pack "}', NULL, true, '2025-09-25 13:26:54.001277+00', 'afb00565-cb04-40ab-b320-cbe98523098c', '58ac2937-c229-488d-a8fb-f995f8665e49', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Generate your Chinese portrait", "fr": "Générer son portrait chinois "}', NULL, true, '2025-09-25 13:26:54.001277+00', '594c3aae-32d0-4f0a-bfba-c14f7a4076d9', '58ac2937-c229-488d-a8fb-f995f8665e49', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Checklist pour une visite ", "fr": "Checklist pour une visite "}', NULL, true, '2025-09-25 13:26:54.001277+00', '6e5c6a43-18db-403b-a836-71d3d9ee8323', 'd8be3245-7cf4-4425-9f7c-bde74bf8b91c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Estimation d''un bien ", "fr": "Estimation d''un bien "}', NULL, true, '2025-09-25 13:26:54.001277+00', '239ad25f-5a42-4869-9be7-f138ce087d26', 'd8be3245-7cf4-4425-9f7c-bde74bf8b91c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Documents pr vendre", "fr": "Documents pr vendre"}', NULL, true, '2025-09-25 13:26:54.001277+00', '2df29be7-09fe-400b-a095-2e27bec10a05', 'd8be3245-7cf4-4425-9f7c-bde74bf8b91c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Real estate advertisement", "fr": "Annonce immobilière "}', NULL, true, '2025-09-25 13:26:54.001277+00', 'a771a158-4a9e-4e67-9170-d8024fd7f31c', 'd8be3245-7cf4-4425-9f7c-bde74bf8b91c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Plan de financement ", "fr": "Plan de financement "}', NULL, true, '2025-09-25 13:26:54.001277+00', '4a65480f-6f3c-4727-abab-824a79d7a8b5', 'd8be3245-7cf4-4425-9f7c-bde74bf8b91c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Calcul des frais annexes ", "fr": "Calcul des frais annexes "}', NULL, true, '2025-09-25 13:26:54.001277+00', '4180407f-b356-47ed-92f1-91de74ebc239', 'd8be3245-7cf4-4425-9f7c-bde74bf8b91c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Créer un programme de formation", "fr": "Créer un programme de formation"}', NULL, true, '2025-09-25 13:26:54.001277+00', '4880c551-785a-4b79-a8e0-716ef385a1b6', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Approfondir un sujet ", "fr": "Approfondir un sujet "}', NULL, true, '2025-09-25 13:26:54.001277+00', '7fe75d8c-0ef9-4f0f-90a8-e63cf0b8515f', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Vulgariser un sujet complexe", "fr": "Vulgariser un sujet complexe"}', NULL, true, '2025-09-25 13:26:54.001277+00', '7beec953-43b5-4d44-8a29-ddec813f271f', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Faire une fiche de révision d''un cours ", "fr": "Faire une fiche de révision d''un cours "}', NULL, true, '2025-09-25 13:26:54.001277+00', 'ae0f06eb-5862-40ec-b456-f2c1c8138a45', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Créer un examen sur un sujet ", "fr": "Créer un examen sur un sujet "}', NULL, true, '2025-09-25 13:26:54.001277+00', 'a10f9249-c4d0-438b-b7d9-a7bac6a52355', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Etude de scénarios ", "fr": "Etude de scénarios "}', NULL, true, '2025-09-25 13:26:54.001277+00', 'd70a8dd1-75ca-479d-aa67-41f1023733f4', '6ddb4752-d985-412c-9cb9-173b86f2b45c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Grille d’analyse d’un dilemme", "fr": "Grille d’analyse d’un dilemme"}', NULL, true, '2025-09-25 13:26:54.001277+00', 'b9f742cb-afdd-4012-a251-cec14dca4786', '6ddb4752-d985-412c-9cb9-173b86f2b45c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Matrice : Arbre décisionnel", "fr": "Matrice : Arbre décisionnel"}', NULL, true, '2025-09-25 13:26:54.001277+00', '6c0428d0-a156-4df2-a871-87ae64096d1a', '6ddb4752-d985-412c-9cb9-173b86f2b45c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Matrice des valeurs personnelles", "fr": "Matrice des valeurs personnelles"}', NULL, true, '2025-09-25 13:26:54.001277+00', 'b5d7a2b2-fdd3-4fee-8d87-9616a4a570b8', '6ddb4752-d985-412c-9cb9-173b86f2b45c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Matrice de décision - Avantage / Inconvénient ", "fr": "Matrice de décision - Avantage / Inconvénient "}', NULL, true, '2025-09-25 13:26:54.001277+00', '9f34d43e-ebd2-435e-b64f-bcd3f655a000', '6ddb4752-d985-412c-9cb9-173b86f2b45c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Notation d''une idée ", "fr": "Notation d''une idée "}', NULL, true, '2025-09-25 13:26:54.001277+00', 'a1400330-15f3-4067-a285-621fd06def4f', '6ddb4752-d985-412c-9cb9-173b86f2b45c', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Création d''accroche ", "fr": "Création d''accroche "}', NULL, false, '2025-09-25 13:26:54.001277+00', '9b0a0cb6-f9d6-4052-8f14-115820331537', '0cf52ff6-0b38-4710-a754-b86fd2c9982a', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Idées de contenu ", "fr": "Idées de contenu "}', NULL, false, '2025-09-25 13:26:54.001277+00', '3cb83671-8abe-4df1-b734-f47b3930415b', '0cf52ff6-0b38-4710-a754-b86fd2c9982a', NULL, NULL),
	('2025-07-23 15:09:40.840438+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Créer sa biographie ", "fr": "Créer sa biographie "}', NULL, false, '2025-09-25 13:26:54.001277+00', '13225c9b-7ec1-47df-8478-ab5322a633d2', '0cf52ff6-0b38-4710-a754-b86fd2c9982a', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Simuler un litige et les options", "fr": "Simuler un litige et les options"}', NULL, true, '2025-09-25 13:26:54.001277+00', '05b1aa1e-1749-4fc5-869a-86d311db22b5', '555b372f-12c1-47d5-8026-aed205b5b5b8', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Comprendre un concept juridique ", "fr": "Comprendre un concept juridique "}', NULL, true, '2025-09-25 13:26:54.001277+00', '5ecbab93-15c3-4d56-84e2-c71143706a75', '555b372f-12c1-47d5-8026-aed205b5b5b8', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Clause de confidentialité", "fr": "Clause de confidentialité"}', NULL, true, '2025-09-25 13:26:54.001277+00', '6fcc03f5-bc38-4b57-98ea-8b494a088e43', '555b372f-12c1-47d5-8026-aed205b5b5b8', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Comprendre un texte de loi ", "fr": "Comprendre un texte de loi "}', NULL, true, '2025-09-25 13:26:54.001277+00', '80404d59-14d0-427c-a64d-070cd553d4be', '555b372f-12c1-47d5-8026-aed205b5b5b8', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Simulation entretien", "fr": "Simulation entretien"}', NULL, true, '2025-09-25 13:26:54.001277+00', 'c95cd97f-2e6e-4a03-9256-66a20bf93982', '560f56ff-2086-4cf2-b78c-cad246d5cb51', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Challenger un CV ", "fr": "Challenger un CV "}', NULL, true, '2025-09-25 13:26:54.001277+00', 'e8883123-c7e1-4ba1-9fe3-decd0b0f96cd', '560f56ff-2086-4cf2-b78c-cad246d5cb51', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Rédiger une lettre de motivation ", "fr": "Rédiger une lettre de motivation "}', NULL, true, '2025-09-25 13:26:54.001277+00', '974964d2-a0a4-449c-afd2-f3b921bcbf1e', '560f56ff-2086-4cf2-b78c-cad246d5cb51', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Actualité de l''entreprise", "fr": "Actualité de l''entreprise"}', NULL, true, '2025-09-25 13:26:54.001277+00', '08a8d10b-783a-4f97-864c-2704de49ebe5', '560f56ff-2086-4cf2-b78c-cad246d5cb51', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Match CV - OFFRE", "fr": "Match CV - OFFRE"}', NULL, true, '2025-09-25 13:26:54.001277+00', 'c120ec49-7bc9-442d-9c8b-66ac61abfdca', '560f56ff-2086-4cf2-b78c-cad246d5cb51', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Préparer un oral de plaidoirie", "fr": "Préparer un oral de plaidoirie"}', NULL, true, '2025-09-25 13:26:54.001277+00', '390d6693-897c-4eee-a170-f84e3bb48be7', '555b372f-12c1-47d5-8026-aed205b5b5b8', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Synthétiser un arrêt juridique", "fr": "Synthétiser un arrêt juridique"}', NULL, true, '2025-09-25 13:26:54.001277+00', '837f9e57-3509-4a83-bf99-2fad9d99d32e', '555b372f-12c1-47d5-8026-aed205b5b5b8', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Designing e-learning modules", "fr": "Conception de modules e-learning"}', NULL, true, '2025-09-25 13:26:54.001277+00', '8c79a773-7769-4b36-b6bd-3b2a89b501d6', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Evaluating training effectiveness", "fr": "Évaluation de l''efficacité formation"}', NULL, true, '2025-09-25 13:26:54.001277+00', '80c564f5-e0ad-48b6-8f32-ca191323e547', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Decision-making in uncertain situations", "fr": "Décisions en situation d''incertitude"}', NULL, true, '2025-09-25 13:26:54.001277+00', '9cea0c85-2eb5-4dd9-8cc1-53d195de131f', '6ddb4752-d985-412c-9cb9-173b86f2b45c', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Effective collective decision-making", "fr": "Décisions collectives efficaces"}', NULL, true, '2025-09-25 13:26:54.001277+00', 'df82ee4e-97e9-4fad-811d-892ff184e8e2', '6ddb4752-d985-412c-9cb9-173b86f2b45c', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Job searching on social media", "fr": "Recherche d''emploi sur les réseaux sociaux"}', NULL, true, '2025-09-25 13:26:54.001277+00', '955e7299-a5b3-442e-8d63-7120ac77dab3', '560f56ff-2086-4cf2-b78c-cad246d5cb51', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Tracking job applications", "fr": "Suivi des candidatures"}', NULL, true, '2025-09-25 13:26:54.001277+00', '3e12e3ce-3b2b-430e-a781-427c4f4f5f5e', '560f56ff-2086-4cf2-b78c-cad246d5cb51', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Personal skills assessment", "fr": "Bilan de compétences personnel"}', NULL, true, '2025-09-25 13:26:54.001277+00', 'f266cdab-3649-476f-b4e8-784b308d98b0', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Professional monitoring", "fr": "Veille professionnelle"}', NULL, true, '2025-09-25 13:26:54.001277+00', '431b5454-1af4-456d-9a54-d81b8ce212cd', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Effective online learning", "fr": "Apprentissage en ligne efficace"}', NULL, true, '2025-09-25 13:26:54.001277+00', '714a06be-e76a-48ba-9bf7-cf924994b891', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Funding training", "fr": "Financement de formation"}', NULL, true, '2025-09-25 13:26:54.001277+00', 'b4374b80-c33e-4a98-b1c1-848a483b91d5', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-07-23 15:09:41.841118+00', NULL, NULL, NULL, 'organization', 0, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Transfer of learning", "fr": "Transfert des acquis"}', NULL, true, '2025-09-25 13:26:54.001277+00', '4aba847f-17d5-4a4c-99a2-e96aa832d0b1', 'ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3', NULL, NULL),
	('2025-10-03 17:18:53.104186+00', NULL, NULL, NULL, 'user', 0, '6d90f22e-dfa0-4b34-a88f-c4a533dc85ab', NULL, NULL, NULL, '{"en": "ded"}', NULL, false, '2025-10-03 17:18:53.227211+00', '4b4a6748-ec31-4ba2-998c-4ed3cc406f3a', NULL, NULL, 131),
	('2025-10-06 09:19:13.097268+00', NULL, '2025-10-15 06:29:26.509372+00', NULL, 'organization', 4, NULL, NULL, '{"en": "Prompt à utiliser pour lancer tous les aspects préalables à l''analyse d''opportunité. Recommande pour le mode \"Deep Research\" de ChatGPT"}', 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '{"en": "Analyse d’opportunité ( recherche approfondie)"}', NULL, false, '2025-10-15 06:29:26.509372+00', '0685171e-a4d7-4bfc-bd8c-6cfc671372bc', '6c5ca58d-d07e-4db7-bc3f-8083c8f5a0c4', NULL, 132),
	('2025-10-06 12:38:21.976917+00', NULL, '2025-10-10 09:47:27.984267+00', NULL, 'user', 2, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{"en": "jjjj"}', NULL, '{"en": "jjujjj"}', NULL, false, '2025-10-10 09:47:27.984267+00', '070f86ec-249e-41b8-81e1-6fe59a85d671', NULL, NULL, 138),
	('2025-10-06 09:38:59.193826+00', NULL, '2025-10-14 19:02:51.789897+00', NULL, 'organization', 17, NULL, NULL, '{"en": "Prompt à utiliser afin d''identifier via les ressources disponibles sur le web les concurrents d''une start-up"}', 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '{"en": "Identification des concurrents"}', NULL, false, '2025-10-14 19:02:51.789897+00', '59973450-0554-405f-8cbd-d19657713faf', 'c37fb64a-e55c-4a39-a734-a5590d1d8192', NULL, 135),
	('2025-10-06 09:25:05.292715+00', NULL, '2025-10-15 10:56:09.404741+00', NULL, 'organization', 9, NULL, NULL, '{"en": "Prompt à utiliser pour obtenir un tableau récap synthétique d''une analyse d''opportunité faite via le prompt optimisé pour la \"Deep Research\""}', 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '{"en": "Tableau Récap"}', NULL, false, '2025-10-15 10:56:09.404741+00', 'ca402200-d312-4cb5-9bc6-f826c0695c36', '6c5ca58d-d07e-4db7-bc3f-8083c8f5a0c4', NULL, 133),
	('2025-07-23 15:09:40.840438+00', NULL, '2025-10-09 12:08:01.60294+00', NULL, 'organization', 1, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Impact of indicator variations on an industry", "fr": "Impact des variations d''un indicateur sur une industrie "}', NULL, true, '2025-10-09 12:08:01.60294+00', 'af54544c-a1f7-4e72-8640-3c9c1d5f6064', 'd1563751-2b27-4902-a364-291348bbb4ad', NULL, NULL),
	('2025-07-23 15:09:41.324192+00', NULL, '2025-10-09 12:11:48.15458+00', NULL, 'organization', 1, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Analyse de CGU ", "fr": "Analyse de CGU "}', NULL, true, '2025-10-09 12:11:48.15458+00', 'd0c49a04-18f5-46cb-8ffa-a6062c9c514b', '555b372f-12c1-47d5-8026-aed205b5b5b8', NULL, NULL),
	('2025-10-09 14:04:51.953638+00', NULL, '2025-10-15 12:37:13.431053+00', NULL, 'organization', 24, NULL, NULL, '{}', 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '{"en": "Analyse produit"}', NULL, true, '2025-10-15 12:37:13.431053+00', '0afc4cba-f28b-4bdb-b5ed-c557c6cb9a3e', '78812c7e-254f-4031-90d8-fe123691b65b', NULL, 147),
	('2025-10-10 09:47:51.02832+00', NULL, '2025-10-10 09:48:12.204961+00', NULL, 'user', 2, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{}', NULL, '{"fr": "Quentinou"}', NULL, true, '2025-10-10 09:48:12.204961+00', '87facb94-d114-40eb-b360-c2e35d2f5ca3', '6a9b3dd6-ae83-44f5-baca-e4a5ae3339ad', NULL, 154),
	('2025-10-10 12:06:35.938736+00', NULL, NULL, NULL, 'user', 0, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{}', NULL, '{"fr": "test"}', NULL, true, '2025-10-10 12:06:36.098185+00', 'cd209b7b-63d3-4b48-bf67-cdac876d5be3', NULL, NULL, 155),
	('2025-10-10 08:14:01.828711+00', NULL, '2025-10-10 08:58:31.148425+00', NULL, 'user', 2, '0eaa7f45-1f7e-403b-84fc-f02d0f0e18a4', NULL, '{"fr": "test test gotti"}', NULL, '{"fr": "test test Gotti"}', NULL, true, '2025-10-10 08:58:31.148425+00', 'ce830523-21c3-4a0b-b4e2-d71983e8c6e9', NULL, NULL, 153),
	('2025-10-10 12:52:17.529862+00', NULL, '2025-10-10 12:52:22.723745+00', NULL, 'user', 1, 'e1e08a40-7482-46e0-87dc-890212ff9148', NULL, '{}', NULL, '{"fr": "Dossier"}', NULL, true, '2025-10-10 12:52:22.723745+00', 'a7cf8be2-99f8-4a9e-a33c-1d9a23accc9a', '735f1b02-e8bc-49f6-abb6-92d17e0c29c5', NULL, 156),
	('2025-10-10 12:58:12.750915+00', NULL, NULL, NULL, 'user', 0, 'e1e08a40-7482-46e0-87dc-890212ff9148', NULL, '{}', NULL, '{"fr": "Jaydai"}', NULL, true, '2025-10-10 12:58:12.878953+00', '33228ff7-e420-4895-8d0f-9dc6cebd5035', '8d88474c-dbd0-4e72-af83-a891a46f3430', NULL, 157),
	('2025-10-09 13:35:27.983459+00', NULL, '2025-10-16 09:17:06.759771+00', NULL, 'organization', 7, NULL, NULL, '{}', 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '{"en": "Analyse des KPI Business"}', NULL, true, '2025-10-16 09:17:06.759771+00', '622ab07c-6458-4b61-82f6-e58ef6daf859', 'd522f0f3-e893-4bd5-b2e4-d28dfbbb298b', NULL, 145),
	('2025-10-10 13:51:47.418326+00', NULL, NULL, NULL, 'user', 0, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{"en": "trtrtr"}', NULL, '{"en": "teteteet"}', NULL, true, '2025-10-10 13:51:47.587015+00', '5b86cffa-add1-4a7b-a23b-9472113e43a6', '6a9b3dd6-ae83-44f5-baca-e4a5ae3339ad', NULL, 162),
	('2025-10-10 13:52:56.67019+00', NULL, NULL, NULL, 'user', 0, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{"en": "opop"}', NULL, '{"en": "opopo"}', NULL, true, '2025-10-10 13:52:56.794878+00', '3607085e-470e-4afc-8ece-7cbffb97a4d6', '6a9b3dd6-ae83-44f5-baca-e4a5ae3339ad', NULL, 163),
	('2025-10-10 13:36:16.992349+00', NULL, '2025-10-10 15:03:42.81268+00', NULL, 'user', 1, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{}', NULL, '{"fr": "test"}', NULL, true, '2025-10-10 15:03:42.81268+00', 'e3bbb2f6-ce97-4f48-98cd-f95cff21147e', NULL, NULL, 158),
	('2025-10-10 17:08:24.148765+00', NULL, NULL, NULL, 'user', 0, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{}', NULL, '{"fr": "kp"}', NULL, true, '2025-10-10 17:08:24.379464+00', '040e8df9-b946-4687-9439-74348696a827', NULL, NULL, 178),
	('2025-10-10 17:00:18.585141+00', NULL, '2025-10-10 18:14:28.559982+00', NULL, 'user', 2, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{}', NULL, '{"fr": ";k;okpkoko"}', NULL, true, '2025-10-10 18:14:28.559982+00', '34818e00-b00a-442b-a4e3-cb25daec5545', NULL, NULL, 177),
	('2025-10-14 17:58:20.58849+00', NULL, '2025-10-14 17:58:24.047178+00', NULL, 'user', 1, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{}', NULL, '{"fr": "je veux etre vu"}', NULL, true, '2025-10-14 17:58:24.047178+00', 'c5aa2046-a945-4056-b067-bbe8feafe99c', '58ad39f3-96c8-4a20-b949-7ae831d8f8a1', NULL, 199),
	('2025-10-10 13:37:30.404114+00', NULL, '2025-10-15 09:58:04.749473+00', NULL, 'user', 2, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{}', NULL, '{"fr": "encore"}', NULL, true, '2025-10-15 09:58:04.749473+00', '9a31e620-baaf-4bd3-8034-56c2c0065b1f', NULL, NULL, 159),
	('2025-10-09 14:22:15.354322+00', NULL, '2025-10-15 07:45:37.040098+00', NULL, 'organization', 16, NULL, NULL, '{}', 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '{"en": "Analyse des brevets"}', NULL, true, '2025-10-15 07:45:37.040098+00', 'cc34c21c-f673-4d85-b0bc-b412e7a7b877', '78812c7e-254f-4031-90d8-fe123691b65b', NULL, 148),
	('2025-10-14 17:58:44.922822+00', NULL, NULL, NULL, 'user', 0, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{}', NULL, '{"fr": "blablab"}', NULL, true, '2025-10-14 17:58:45.024675+00', 'b391445b-0a14-471a-81a9-bef9465c5aba', '6a9b3dd6-ae83-44f5-baca-e4a5ae3339ad', NULL, 200),
	('2025-10-10 13:37:55.098022+00', NULL, '2025-10-14 18:11:34.950879+00', NULL, 'user', 1, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{"en": "oioio"}', NULL, '{"en": "ioi"}', NULL, true, '2025-10-14 18:11:34.950879+00', 'dd5a5376-a3df-4568-acbc-b29cf30eed58', NULL, NULL, 160),
	('2025-10-06 09:41:36.859916+00', NULL, '2025-10-15 00:29:32.337807+00', NULL, 'organization', 10, NULL, NULL, '{"en": "Identifier les différents éléments financiers importants à prendre en compte"}', 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '{"en": "Levée de fonds, exits, faillites"}', NULL, false, '2025-10-15 00:29:32.337807+00', 'd873afad-f570-4f6c-993f-cc0d1e8dc9c3', 'c37fb64a-e55c-4a39-a734-a5590d1d8192', NULL, 136),
	('2025-10-15 00:41:40.255006+00', NULL, NULL, NULL, 'user', 0, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{"en": "fefr"}', NULL, '{"en": "refer"}', NULL, true, '2025-10-15 00:41:40.744743+00', 'dc04e22e-b225-4d65-b53d-17320c29252c', NULL, NULL, 218),
	('2025-10-15 00:47:38.932802+00', NULL, NULL, NULL, 'user', 0, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{"en": "fewfww"}', NULL, '{"en": "teeest"}', NULL, true, '2025-10-15 00:47:39.012733+00', '0bc77942-a134-4baf-866b-763df0ba162b', NULL, NULL, 219),
	('2025-10-15 00:50:14.84399+00', NULL, NULL, NULL, 'user', 0, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{"en": "eddd"}', NULL, '{"en": "okkk"}', NULL, true, '2025-10-15 00:50:14.919346+00', '6bcdf33e-1ea1-47bf-ad2d-5df88b8fe676', '6a9b3dd6-ae83-44f5-baca-e4a5ae3339ad', NULL, 220),
	('2025-10-15 00:51:33.612596+00', NULL, NULL, NULL, 'user', 0, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{"en": "rtehhth"}', NULL, '{"en": "uht"}', NULL, true, '2025-10-15 00:51:33.737632+00', '0bb3ce7f-894a-46de-a336-6ce6b4b71deb', NULL, NULL, 221),
	('2025-10-15 00:54:17.325103+00', NULL, NULL, NULL, 'user', 0, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{"en": "trehrthh"}', NULL, '{"en": "trertht"}', NULL, true, '2025-10-15 00:54:17.413445+00', '3023e64e-cbab-44b6-88f5-4c920f8af179', NULL, NULL, 222),
	('2025-10-16 08:18:14.916406+00', NULL, '2025-10-20 14:41:23.869894+00', NULL, 'organization', 5, '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, '{}', 'f8d0fe34-32ff-4d90-87ed-28e83c50f953', '{"en": "Analyse financière société côtée - Style Vernimmen"}', NULL, true, '2025-10-20 14:41:23.869894+00', '942db23b-28b3-45bf-bef0-8a0749753ed6', '955c551e-f7e1-4950-a87c-7f4b57578bd5', NULL, 240),
	('2025-10-15 01:04:31.570608+00', NULL, NULL, NULL, 'organization', 0, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{"en": "yth"}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "ytehtyh"}', NULL, true, '2025-10-15 01:04:31.755087+00', '59947887-15e4-4fc4-a565-07aad53831ae', NULL, NULL, 224),
	('2025-10-15 06:33:59.84527+00', NULL, '2025-10-15 06:35:17.418327+00', NULL, 'user', 1, '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, '{}', NULL, '{"fr": "Test"}', NULL, true, '2025-10-15 06:35:17.418327+00', '26878071-a631-49c6-872b-da4386f9270e', '6d5ffe97-39b0-4c8f-a461-aca582a52644', NULL, 228),
	('2025-10-15 10:44:55.691721+00', NULL, '2025-10-21 13:34:52.194035+00', NULL, 'organization', 10, '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, '{}', 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '{"en": "Analyse des dirigeants"}', NULL, true, '2025-10-21 13:34:52.194035+00', '8d7f1d84-aacb-49f9-9fd2-f7b2a912d776', 'a330b6ac-47f8-4a26-9871-7d0937241049', NULL, 231),
	('2025-10-15 15:41:12.828197+00', NULL, '2025-10-15 15:42:09.066272+00', NULL, 'organization', 1, '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', NULL, '{"en": "kpokpko"}', 'a0a0e03a-fdbe-4924-83fd-8d4a547c5892', '{"en": "test"}', NULL, true, '2025-10-15 15:42:09.066272+00', '57735546-1b3c-4272-9f42-339e4a4c28bd', '69d989da-b8bb-42b2-8329-4a7ce2cac53c', NULL, 238),
	('2025-10-15 10:35:16.46969+00', NULL, NULL, NULL, 'user', 0, '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, '{}', NULL, '{"fr": "TEst"}', NULL, true, '2025-10-15 10:35:16.617702+00', '960ea9e0-f9d1-47b3-a2cf-ab6c39959710', 'b9a5ca95-8a46-40ba-aee6-44d5b19191ea', NULL, 230),
	('2025-10-16 08:38:10.979913+00', NULL, NULL, NULL, 'organization', 0, '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, '{}', 'f8d0fe34-32ff-4d90-87ed-28e83c50f953', '{"en": "Synthèse financière pour un board"}', NULL, true, '2025-10-16 08:38:11.179044+00', '1c2589b0-0670-4cf2-a312-012cd9adbd50', '955c551e-f7e1-4950-a87c-7f4b57578bd5', NULL, 241),
	('2025-10-15 10:47:46.429431+00', NULL, '2025-10-15 10:56:05.5815+00', NULL, 'user', 2, '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, '{}', NULL, '{"fr": "Développement perso"}', NULL, true, '2025-10-15 10:56:05.5815+00', '8cdd2c93-6ae4-4d84-b345-94c9f4a568f1', '3be04320-9714-4794-a8fc-9143eecc8225', NULL, 232),
	('2025-10-16 09:32:26.725016+00', NULL, NULL, NULL, 'organization', 0, '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, '{}', 'f8d0fe34-32ff-4d90-87ed-28e83c50f953', '{"en": "Comparaison ESG 2 entreprises"}', NULL, true, '2025-10-16 09:32:26.854824+00', '88568fe8-7687-44db-a337-fe0dfa5e9ef3', '12ac27d9-7b89-4e2a-9a23-083a84d503c1', NULL, 244),
	('2025-10-16 09:31:30.197723+00', NULL, '2025-10-16 13:44:27.516018+00', NULL, 'organization', 4, '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, '{}', 'f8d0fe34-32ff-4d90-87ed-28e83c50f953', '{"en": "performance ESG"}', NULL, true, '2025-10-16 13:44:27.516018+00', '0dfabe1c-848a-47b7-b333-e54106839e7d', '12ac27d9-7b89-4e2a-9a23-083a84d503c1', NULL, 243),
	('2025-10-16 13:46:39.214292+00', NULL, NULL, NULL, 'organization', 0, '95fec575-147d-49ba-bd8d-d8c1295159e6', NULL, '{}', 'f8d0fe34-32ff-4d90-87ed-28e83c50f953', '{"en": "Analyse de marché"}', NULL, true, '2025-10-16 13:46:39.396499+00', '11691eaa-85a7-4010-bad3-a8594672c7c9', 'f4e4127b-6d44-40d6-830b-db326e0c03a1', NULL, 245),
	('2025-07-23 15:09:40.207746+00', NULL, '2025-11-05 16:47:31.173203+00', NULL, 'organization', 2, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Sent a mail", "fr": "Envoyer un mail "}', NULL, true, '2025-11-05 16:47:31.173203+00', '02a3f1bb-fdf4-4212-8e2f-505f42138a70', '7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138', NULL, NULL),
	('2025-11-05 17:04:05.995741+00', NULL, '2025-11-05 17:05:35.098366+00', NULL, 'user', 1, '478b7491-ff6c-490b-982c-a4dc866dcefc', NULL, '{"fr": "a"}', NULL, '{"fr": "oui"}', NULL, true, '2025-11-05 17:05:35.098366+00', 'f1fca1b9-8e72-43b0-8907-4fa8a5f3bf52', NULL, NULL, 248),
	('2025-07-23 15:09:40.207746+00', NULL, '2025-11-06 09:42:08.036424+00', NULL, 'organization', 1, NULL, NULL, '{}', '19864b30-936d-4a8d-996a-27d17f11f00f', '{"en": "Learn a new topic", "fr": "Apprendre un nouveau sujet"}', NULL, true, '2025-11-06 09:42:08.036424+00', '4ccd8560-98df-4ab7-af7d-f3d3568352b2', '7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138', NULL, NULL),
	('2025-11-05 17:01:26.66939+00', NULL, '2025-11-06 16:57:28.529824+00', NULL, 'user', 5, '478b7491-ff6c-490b-982c-a4dc866dcefc', NULL, '{}', NULL, '{"fr": "Météo ?"}', NULL, true, '2025-11-06 16:57:28.529824+00', '512ec0bc-7961-43b0-a91c-b4876428641c', '156e6146-9aa7-488a-ba08-828e31ff7023', NULL, 247);


--
-- Data for Name: prompt_templates_versions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."prompt_templates_versions" ("id", "created_at", "updated_at", "version_number", "content", "author_id", "usage_count", "parent_version_id", "change_notes", "status", "template_id", "is_current", "optimized_for", "is_published") VALUES
	(131, '2025-10-03 17:18:53.167229+00', '2025-10-03 17:20:14.964478+00', '1.0', '{"en": "**geegege**\n**role:**"}', '6d90f22e-dfa0-4b34-a88f-c4a533dc85ab', 0, NULL, '{"en": "Initial version of ded", "fr": "Version initiale de ded"}', 'draft', '4b4a6748-ec31-4ba2-998c-4ed3cc406f3a', true, '{copilot,mistral}', false),
	(156, '2025-10-10 12:52:17.597672+00', '2025-10-10 12:52:17.597672+00', '1.0', '{"fr": "dezfs"}', 'e1e08a40-7482-46e0-87dc-890212ff9148', 0, NULL, '{"en": "", "fr": ""}', 'draft', 'a7cf8be2-99f8-4a9e-a33c-1d9a23accc9a', false, NULL, true),
	(173, '2025-10-10 16:22:39.802316+00', '2025-10-10 16:22:39.802316+00', 'test', '{"en": "Tu es un expert reconnu et un excellent vulgarisateur. Ton objectif est d''expliquer à un jeune adulte de 18 ans ce qu''est [Indiquer le sujet à expliquer] \nCommence par expliquer le **contexte général** du sujet : pourquoi on en parle aujourd’hui, quelles sont les bases à connaître. Puis présente les **enjeux principaux** de manière simple, comme si tu parlais à un ami curieux. Utilise des **exemples concrets**. \n\nEnsuite, fais un **point sur l’actualité récente** liée à ce sujet : qu’est-ce qui a changé ou est en train de changer ? Pourquoi c’est important pour le futur ?\n\nAdopte un **ton accessible**. N’utilise pas de jargon, ou alors explique chaque mot compliqué comme si tu faisais une pause pour clarifier. \n\nStructure ta réponse en 3 parties :\n1. **Définition?** \n2. **Pourquoi c’est important ?**\n3. **Ce qu’il faut savoir aujourd’hui (et demain)**\n4. Réalise une conclusion en essayant d''inclure la personne"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "poop"}', 'draft', 'b4c419ca-e935-4036-b5a1-c8e1e2043684', false, '{copilot}', false),
	(219, '2025-10-15 00:47:38.973629+00', '2025-10-15 00:47:38.973629+00', '1.0', '{"en": "gtgtgtg"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '0bc77942-a134-4baf-866b-763df0ba162b', false, NULL, true),
	(222, '2025-10-15 00:54:17.367508+00', '2025-10-15 00:54:17.367508+00', '1.0', '{"en": "rthrthrt"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '3023e64e-cbab-44b6-88f5-4c920f8af179', false, NULL, true),
	(224, '2025-10-15 01:04:31.629239+00', '2025-10-15 01:04:31.629239+00', '1.0', '{"en": "trhrheh"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '59947887-15e4-4fc4-a565-07aad53831ae', false, '{chatgpt,copilot,gemini}', false),
	(221, '2025-10-15 00:51:33.713126+00', '2025-10-15 01:12:13.255582+00', '1.0', '{"fr": "rhthrth\nsdfs\nf\nfs\ndfds\nfds\nfsd\nfs\nd\ndsg\ndsg\nds\ngdsg"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '0bb3ce7f-894a-46de-a336-6ce6b4b71deb', false, NULL, true),
	(174, '2025-10-10 16:22:45.570888+00', '2025-10-15 08:13:21.1625+00', 'ojjojoj', '{"en": "", "fr": ""}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', 'b4c419ca-e935-4036-b5a1-c8e1e2043684', false, '{}', false),
	(175, '2025-10-10 16:26:28.573225+00', '2025-10-10 16:32:47.28842+00', 'okok', '{"en": "**Rôle:** \nTu es un expert en marketing, en ventes et en copywriting avec plus de 30 d''expérience sur mon domaine d''activité.  \n\n**Contexte:**\nJe dois réaliser une FAQ sur mon entreprise et mes services / produits. Les variables à prendre en compte sont les suivantes : \n- Nom de mon entreprise : [Indique le nom de ton entreprise]\n- Site web : [Indique le lien de ton site web]\n- Type de produit : [Type de produit : SaaS / Bien de consommation / Application mobile / autre]\n- Marché : [Marché : B2B / B2C / les deux]\n- Autre points importants : [Indique les autres points importants : cible, tarif, avantages, etc.]\n\n**Objectif:**\nTon rôle est de générer une FAQ ultra pertinente à destination des potentiels clients d''une solution.\n\n**Format de sortie:**\nGénère une FAQ marketing claire, rassurante et engageante qui couvre :\n- Les fonctionnalités principales\n- La valeur ajoutée pour l’utilisateur\n- Les questions fréquentes (prix, sécurité, compatibilité, support, RGPD, etc.)\n- Les objections possibles et les réponses adaptées\n- La crédibilité et la preuve sociale (si pertinentes)\n\n**Ton & Style:**\nUtilise un ton à la fois professionnel, simple, direct et pédagogique. Organise la FAQ avec des questions en gras et des réponses claires, avec parfois des exemples concrets.\n\n"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "okok"}', 'draft', '0e0be45b-b2e1-4e97-8c7e-d159767314d4', false, '{chatgpt}', true),
	(199, '2025-10-14 17:58:20.642202+00', '2025-10-14 17:58:20.642202+00', '1.0', '{"fr": "opopopop"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', 'c5aa2046-a945-4056-b067-bbe8feafe99c', false, NULL, true),
	(200, '2025-10-14 17:58:44.969054+00', '2025-10-14 17:58:44.969054+00', '1.0', '{"fr": "opopopo"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', 'b391445b-0a14-471a-81a9-bef9465c5aba', false, NULL, true),
	(220, '2025-10-15 00:50:14.877901+00', '2025-10-15 00:50:14.877901+00', '1.0', '{"en": "ededed"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '6bcdf33e-1ea1-47bf-ad2d-5df88b8fe676', false, NULL, true),
	(132, '2025-10-06 09:19:13.178154+00', '2025-10-15 10:40:45.287586+00', 'Défaut', '{"en": "**Rôle :**\nTu es un investisseur expérimenté (business angel / VC / analyste stratégique) avec plus de 30 ans d’expérience.\n\n**Contexte :**\nJ''étudie une opportunité d’investissement et j’ai besoin d’avoir accès à une analyse de qualité pour me positionner sur le sujet.\n- La startup à analyser est la suivante : biomere**[Indique le nom de la startup]**\n- Le site web de la startup est le suivant : **[Insère le lien du site web]**\n- Indique ici les éléments de contexte importants si nécessaire : **[Indique les éléments de contexte importants à prendre en compte]**\n\n**Objectif :**\nTon objectif est de réaliser une analyse experte afin de me donner l’ensemble des clés de compréhension pour évaluer la position, le potentiel et les risques d’une startup dans son secteur et me permettre de me positionner.\n\n**Format de sortie souhaité :**\nRéalise une analyse détaillée et structurée selon les 6 grandes catégories suivantes :\n**1 - Marché & Positionnement**\n- **1.1 - Segment de marché ciblé**\n    - Quels besoins ou problèmes la startup adresse-t-elle ?\n    - Analyse du marché (Historique, taille, croissance, tendances, drivers, freins, TAM, SAM, SOM)\n    - Maturité du marché et dynamique d’adoption (early adopters, mass market, corporate adoption)\n    - Évaluation de la maturité du marché et scoring de l’ouverture à l’innovation d’un marché (analyse médias, publications académiques, subventions publiques).\n    - Niveau d’urgence / besoins non satisfaits ?\n    - Anticipation des évolutions du marché\n- **1.2 - Degré de différenciation**\n    - Principaux chiffres récents de la startup (CA, effectif, offre, etc.). Sois le plus précis possible\n    - La startup se différencie-t-elle par une technologie, un business model, une distribution ou un pricing innovant ?\n    - Positionnement prix / accessibilité future ?\n- **1.3 - Avantage concurrentiel défendable**\n    - Brevets solides, algorithmes propriétaires, data unique, effet réseau ?\n    - Premier acteur sur son segment ou suiveur ?\n- **1.4 Analyse du business model et des Finances**\n    - Analyse de sensibilité du business plan (CAC, churn, ARR…)\n    - Revue du pricing concurrentiel\n---\n**2. Technologie / Produit & Propriété intellectuelle**\n- **2.1 Maturité technologique / produit**\n    - Stade : idée, prototype, MVP, traction, scale ?\n    - Résultats ou preuves de concept solides (clients pilotes, validation marché, brevets, publications…) ?\n- **2.2 Méthodologie / différenciation technique**\n    - Quelle est la technologie clé ? Analyse de la stack technologique\n    - Facilité de mise à l’échelle / industrialisation ?\n- **2.3 Propriété intellectuelle**\n    - Nombre et type de brevets déposés ?\n    - Étendue géographique ?\n    - Liberté d’exploitation (FTO - Freedom to Operate) ?\n    - Exclusivité de licences (si issue d’un laboratoire ou institut public) ?\n    - Évaluation de la différenciation réelle\n---\n**3. Analyse des concurrents directs et indirects**\n- **3.1 Cartographie des acteurs existants**\n    - Concurrents directs\n    - Grands groupes et ETI\n    - Startups\n    - Concurrents indirects\n- **3.2 Comparaison des offres / pipelines**\n    - Avancement produit (MVP)\n    - Types de clients ou marchés visés ?\n    - Stratégie différenciante (prix, UX, scalabilité, partenariat…) ?\n- **3.3 Accords stratégiques et financements**\n    - Partenariats stratégiques avec grandes entreprises ?\n    - Montants levés, investisseurs clés ?\n    - Subventions / aides publiques ?\n- **3.4 Analyse approfondie des stratégies**\n    - Business model & Pricing\n    - Cible et clients\n    - Distribution et partenariats\n    - Différenciations produits\n- **3.5 Tableau récapitulatif**\n    - Les concurrents directs\n    - Les concurrents indirects\n    - Leur stade de développement\n    - Leurs financements\n    - Leur différenciation\n    - Leur Business model et leur tarification\n    - La différence avec la startup analysée et l''avantage concurrentiel par rapport à cette startup\n---\n**4. Industrialisation & Scalabilité**\n- **4.1 Capacité de production / exécution**\n    - Volume de production ou capacité à délivrer à grande échelle ?\n    - Outils, infrastructures, supply chain, automatisation ?\n- **4.2 Respect des normes & standards**\n    - Certifications, normes réglementaires (ISO, GDPR, FDA, EMA, SOC2, etc.) ?\n    - Préparation à la conformité réglementaire ?\n- **4.3 Barrières à l’entrée**\n    - Coûts fixes élevés ?\n    - Difficulté technique ou technologique de reproduction ?\n    - Effets de réseau / lock-in utilisateur ?\n---\n**5. Stratégie de développement**\n- **5.1 Vision produit & go-to-market**\n    - Business model (B2B, B2C, SaaS, marketplace, hardware, etc.) ?\n    - Plan de développement clair et milestones de valorisation ?\n    - Partenariats envisagés ou stratégie d’indépendance ?\n- **5.2 Pipeline & diversification**\n    - Un seul produit ou plusieurs ?\n    - Diversification technologique ou sectorielle prévue ?\n    - Capacité à pivoter ?\n---\n**6. Analyse de l’équipe dirigeante**\n\n**6.1 Identification des fondateurs**\n- Noms des cofondateurs\n- Répartition du capital (si public)\n- Date de fondation et ancienneté du partenariat\n    👉 Présentation en **tableau clair à deux colonnes**.\n**6.2 Profils individuels (par fondateur, en tableau deux colonnes)**\n**Formation** : diplômes, écoles/universités, spécialisation, prestige académique.\n**Expérience professionnelle** : postes précédents, progression de carrière, secteurs, responsabilités clés.\n**Expertise technique/sectorielle** : compétences spécifiques, connaissance du marché ciblé.\n**Expérience entrepreneuriale** : startups précédentes, succès/échecs, rôles dans l’écosystème.\n**6.3 Fit fondateurs-projet**\n- **Légitimité sectorielle** : années d’expérience, réseau, compréhension du problème.\n- **Adéquation compétences-besoins** : couverture des compétences critiques, expertise sur les défis clés.\n- **Historique de collaboration** : travail commun préalable, clarté des responsabilités.\n**6.4 Crédibilité & signaux**\n- **Track record** : succès mesurables, prix, reconnaissance.\n- **Réputation écosystème** : presse, événements, mentions par d’autres investisseurs, réseaux sociaux.\n- **Réseau professionnel** : advisors, mentors, investisseurs précédents, partenaires stratégiques.\n- **Signaux d’alarme** : conflits d’intérêts, litiges, incohérences, turnover.\n**6.5 Synthèse exécutive fondateurs**\n- **Tableau de synthèse** : note sur 5 (étoiles ⭐) par critère avec justification.\n---\n**7. Environnement réglementaire & macro**\n- **7.1 Réglementation applicable au secteur**\n    - Cadre clair ou en construction ?\n    - Risques de changements réglementaires ?\n    - Précédents d’autorisations ou d’interdictions ?\n- **7.2 Tendances sectorielles**\n    - Croissance du marché global ?\n    - Intérêt croissant des investisseurs et corporates ?\n    - Risque de hype non justifiée ?\n**8. Environnement réglementaire & macro**\n- Overview de la réglementation en cours\n- Liste des tendances\n- Risques réglementaires à prendre en compte\n- Risques macro à prendre en compte\n**9. Exit potentiel**\n- Liste les différentes typologies d''acteurs qui pourraient être intéressés par un exit\n- Identifie les exits d''entreprises sur le même marché et donne toutes les informations relatives à ces exits sous le format suivant :\n- *Intro (3–5 lignes).* Précise la nature des exits, profils d’acquéreurs, éventuels multiples publics.\n\n| Entreprise | Pays | Sous-segment | Description de l''entreprise | Type d’exit | Acquéreur / Bourse | Date | Valeur/Valo (si public) | Raison stratégique (si disponible) | Lien source 1 | Lien source 2  |\n\n|---|---|---|---|---|---|---|---|---|---|\n\n- Trouve un maximum de cas à présenter.\n1. **Conclusion**\n- 10.1 Prise de position finale\n    - Conclus par une position claire :\n    - Niveau de risque Opportunité ou menace\n    - Pourquoi tu investirais (ou pas)\n    - Sizing de la valorisation de la startup sur la base des metrics que tu connais\n- **11 Annexe demandée (nouvelle section)**\n    Fiches détaillées des 15 concurrents directs\n    Pour chaque concurrent :\n    - Nom & site web\n    - Positionnement (marché, client cible)\n    - Produit / technologie clé\n    - Modèle économique (pricing, SaaS, marketplace, etc.)\n    - Clients / traction connus\n    - Financements (montants levés, investisseurs, subventions)\n    - Partenariats stratégiques\n    - Différenciation perçue (UX, technologie, data, distribution)\n    - Forces / faiblesses\n    - Stade de maturité (MVP, croissance, scale, exit)\n\n**Contrainte:**\n- Sources à prioriser : sites web d''entreprise, interviews, articles de presse spécialisés, réseaux sociaux professionnels, papers\n- Vérification croisée : Confirme les informations importantes avec plusieurs sources\n- Objectivité : Reste factuel et équilibré, signale les manques d''information et n’invente rien\n- Fais attention aux homonymes. Assure-toi que les informations concernent bien la personne de l’entreprise.\n- Cite l’ensemble de tes sources à chaque fois\n- Mise en forme : le document doit être rédigé, professionnel et agréable\n- Tu es un top Business Angel qui n''investit que dans les projets les plus prometteurs. Sois le plus critique possible dans ton analyse. Tu investis uniquement dans le TOP 0,1% des startups. Cela doit se ressentir quand tu prends position."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "Initial version of Analyse d’opportunité ( recherche approfondie)", "fr": "Version initiale de Analyse d’opportunité ( recherche approfondie)"}', 'certified', '0685171e-a4d7-4bfc-bd8c-6cfc671372bc', true, '{chatgpt}', true),
	(157, '2025-10-10 12:58:12.807314+00', '2025-10-10 12:58:12.807314+00', '1.0', '{"fr": "Bonjour \nJe fais un test"}', 'e1e08a40-7482-46e0-87dc-890212ff9148', 0, NULL, '{"en": "", "fr": ""}', 'draft', '33228ff7-e420-4895-8d0f-9dc6cebd5035', false, NULL, true),
	(238, '2025-10-15 15:41:12.880503+00', '2025-10-15 15:41:54.729348+00', '1.0', '{"en": "efwasdV\n\n**ROLE:**\nTu es un analyste en capital-risque spécialisé dans l’évaluation de startups early-stage. Tu maîtrises la lecture critique de pitch decks, de business plans financiers et de plans de croissance. Ton rôle est de fournir une analyse claire et rationnelle du potentiel du projet."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '57735546-1b3c-4272-9f42-339e4a4c28bd', false, '{chatgpt,mistral,claude}', true),
	(239, '2025-10-15 15:42:18.354347+00', '2025-10-15 15:42:21.719912+00', 'jij', '{"en": "efwasdV\n\n**ROLE:**\nTu es un analyste en capital-risque spécialisé dans l’évaluation de startups early-stage. Tu maîtrises la lecture critique de pitch decks, de business plans financiers et de plans de croissance. Ton rôle est de fournir une analyse claire et rationnelle du potentiel du projet."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '57735546-1b3c-4272-9f42-339e4a4c28bd', false, '{}', true),
	(6, '2025-09-16 15:43:55.64655+00', '2025-10-10 13:18:48.921491+00', '1', '{"fr": "**Rôle:** \nTu es un expert en marketing, en ventes et en copywriting avec plus de 30 d''expérience sur mon domaine d''activité.  \n\n**Contexte:**\nJe dois réaliser une FAQ sur mon entreprise et mes services / produits. Les variables à prendre en compte sont les suivantes : \n- Nom de mon entreprise : [Indique le nom de ton entreprise]\n- Site web : [Indique le lien de ton site web]\n- Type de produit : [Type de produit : SaaS / Bien de consommation / Application mobile / autre]\n- Marché : [Marché : B2B / B2C / les deux]\n- Autre points importants : [Indique les autres points importants : cible, tarif, avantages, etc.]\n\n**Objectif:**\nTon rôle est de générer une FAQ ultra pertinente à destination des potentiels clients d''une solution.\n\n**Format de sortie:**\nGénère une FAQ marketing claire, rassurante et engageante qui couvre :\n- Les fonctionnalités principales\n- La valeur ajoutée pour l’utilisateur\n- Les questions fréquentes (prix, sécurité, compatibilité, support, RGPD, etc.)\n- Les objections possibles et les réponses adaptées\n- La crédibilité et la preuve sociale (si pertinentes)\n\n**Ton & Style:**\nUtilise un ton à la fois professionnel, simple, direct et pédagogique. Organise la FAQ avec des questions en gras et des réponses claires, avec parfois des exemples concrets.\n\n"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '0e0be45b-b2e1-4e97-8c7e-d159767314d4', false, NULL, false),
	(158, '2025-10-10 13:36:17.097358+00', '2025-10-10 13:36:17.097358+00', '1.0', '{"fr": "test"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', 'e3bbb2f6-ce97-4f48-98cd-f95cff21147e', false, NULL, true),
	(159, '2025-10-10 13:37:30.484088+00', '2025-10-10 13:37:30.484088+00', '1.0', '{"fr": "envore"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '9a31e620-baaf-4bd3-8034-56c2c0065b1f', false, NULL, true),
	(4, '2025-09-16 15:43:55.64655+00', '2025-10-10 13:06:26.400033+00', '1', '{"fr": "**Rôle:**\nTu es un investisseur VC expérimenté avec plus de 30 d''expérience, spécialisé dans l’évaluation de startups early-stage. Tu n''investis que dans le Top 0,1% des projets. \n\n**Contexte:**\nJe souhaite analyser le deck de l''entreprise [Indiquer le nom de la société] pour évaluer l''opportunité d''investir dans cette entreprise. \nLe site web de l''entreprise est le suivant [Indiquer le site web de l''entreprise].\n\n**Objectif:**\nTa mission est d’analyser un deck de startup et d’en évaluer la qualité, la clarté et le potentiel d’investissement.\n\n**Format de sortie:**\n🧾 Ta réponse doit être structurée comme suit :\n\n1. Note globale sur 100\n2. Évaluation détaillée de chaque critère (note sur 10 + analyse critique)\n3. Points forts du deck\n4. Axes d’amélioration et points faibles\n5. Recommandations finales pour maximiser l’impact et convaincre les investisseurs\n\n📊 Critères d’évaluation (note sur 10 chacun) :\n\n---\n\n### 1️⃣ Problème & Opportunité de marché (sur 10)\n\n✅ Points à vérifier :\n- Le problème est-il clair, urgent et important ?\n- Est-il universel ou niche ?\n- Est-ce un vrai pain point ?\n- Le deck montre-t-il une opportunité de marché chiffrée et crédible ?\n- Y a-t-il un angle différenciant ou une vision unique ?\n⚠️ Challenge :\n- Pourquoi ce problème n’a-t-il pas encore été résolu ?\n- Que devient la startup si le problème disparaît ?\n- Est-ce un problème suffisamment gros pour justifier une levée ?\n🎯 Note : __/10\n📝 Analyse détaillée :\n\n---\n\n### 2️⃣ Solution & Proposition de valeur (sur 10)\n✅ Points à vérifier :\n- La solution répond-elle directement au problème ?\n- Est-elle 10x meilleure que ce qui existe ?\n- L’innovation est-elle mise en avant (tech, UX, modèle…) ?\n- Y a-t-il des preuves d’intérêt marché ?\n⚠️ Challenge :\n- Qu’est-ce qui rend la solution vraiment unique ?\n- Est-elle copiable facilement ?\n- Comment résiste-t-elle à un concurrent bien financé ?\n🎯 Note : __/10\n📝 Analyse détaillée :\n\n---\n\n### 3️⃣ Business Model & Monétisation (sur 10)\n✅ Points à vérifier :\n- Comment l’entreprise gagne-t-elle de l’argent ?\n- Le modèle est-il scalable ?\n- Y a-t-il de la récurrence (SaaS, abonnements, etc.) ?\n- Présence de KPIs financiers clés : CAC, LTV, marge brute…\n⚠️ Challenge :\n- Ce modèle est-il viable à long terme ?\n- Y a-t-il des coûts cachés ?\n- Dépendance à un canal d’acquisition ?\n🎯 Note : __/10\n📝 Analyse détaillée :\n\n---\n\n### 4️⃣ Traction & Adoption Marché (sur 10)\n✅ Points à vérifier :\n- Y a-t-il des utilisateurs ou clients engagés ?\n- Chiffres de traction (revenus, croissance, churn) ?\n- Preuves sociales : presse, clients, investisseurs…\n⚠️ Challenge :\n- Les clients reviennent-ils ?\n- CAC vs LTV : est-ce soutenable ?\n- Si la startup disparaît demain, qui serait vraiment impacté ?\n🎯 Note : __/10\n📝 Analyse détaillée :\n\n---\n\n### 5️⃣ Concurrence & Barrières à l’entrée (sur 10)\n✅ Points à vérifier :\n- Le paysage concurrentiel est-il bien analysé ?\n- Avantages compétitifs clairs ?\n- Risques d’entrée de gros acteurs ?\n⚠️ Challenge :\n- Quelle est la vraie barrière à l’entrée ?\n- Pourquoi un Google / Amazon ne peut-il pas l’écraser ?\n- L’avantage sera-t-il encore là dans 3 ans ?\n🎯 Note : __/10\n📝 Analyse détaillée :\n\n---\n\n### 6️⃣ Marché & Scalabilité (sur 10)\n✅ Points à vérifier :\n- TAM, SAM, SOM bien définis et crédibles ?\n- Y a-t-il des freins géographiques, réglementaires ou techniques ?\n- Vision claire de l’expansion ?\n⚠️ Challenge :\n- La startup attaque-t-elle le bon segment ?\n- Quelle est la vraie opportunité mondiale ?\n- Comment scaler x10 en 3 ans ?\n🎯 Note : __/10\n📝 Analyse détaillée :\n\n---\n\n### 7️⃣ Équipe & Exécution (sur 10)\n✅ Points à vérifier :\n- L’équipe fondatrice a-t-elle un bon track record ?\n- Les compétences sont-elles bien réparties ?\n- Exécution rapide et efficace ?\n⚠️ Challenge :\n- Que se passe-t-il si le CEO part ?\n- L’équipe peut-elle pivoter ?\n- Y a-t-il un déséquilibre tech / biz ?\n🎯 Note : __/10\n📝 Analyse détaillée :\n\n---\n\n### 8️⃣ Roadmap & Vision long-terme (sur 10)\n✅ Points à vérifier :\n- Roadmap claire, ambitieuse mais réaliste ?\n- Étapes finançables avec cette levée ?\n- Vision inspirante et crédible ?\n⚠️ Challenge :\n- Y a-t-il un plan B en cas d’échec ?\n- La vision permet-elle de devenir un leader mondial ou juste une niche ?\n🎯 Note : __/10\n📝 Analyse détaillée :\n\n---\n\n🔍 Conclusion\n✅ Points forts du deck :\n(Lister ici les éléments solides et convaincants)\n⚠️ Points faibles et axes d’amélioration :\n(Lister les manques, imprécisions ou zones floues)\n📢 Recommandations finales pour maximiser l’impact :\n(Lister les actions concrètes pour renforcer le pitch)\n\n**Contrainte:**\nNe te contente pas d’une analyse basique.\nChallenge chaque aspect du deck en posant des questions critiques et en mettant en avant les zones d’ombre.\nAssure toi d''avoir le deck avant de commencer ton analyse. "}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '5712dd34-0245-4908-810b-753761ba9d21', false, NULL, true),
	(133, '2025-10-06 09:25:05.398555+00', '2025-10-14 18:07:40.469386+00', '1.0', '{"en": "**Rôle :**\n- Tu es un Business Angel ultra-exigeant, avec 20+ ans d''expérience dans le financement de start-up. Tu n’investis que dans le top 0,1 % des opportunités et refuses 99,9 % des dossiers.\n\n**Contexte :**\n- Je t’ai transmis ou vais te transmettre une analyse détaillée de la start-up [Indiquer le nom de la start-up]. Tu dois en faire une lecture critique pour évaluer si elle mérite d''aller plus loin dans un processus de due diligence.\n\n**Objectif :**\nProduis un résumé clair, synthétique et opérationnel sous forme de Tableau d’Analyse Investment Grade pour prendre une décision d’investissement initiale.\n\n**Format de sortie :**\n- Tableau avec les colonnes suivantes :\n    Critère\n    Note (1 à 5 étoiles ⭐ à ⭐⭐⭐⭐⭐)\n    Justification (max 4 lignes, données chiffrées si possible)\n    Red Flag (si applicable)\nCritères à évaluer :\n- Équipe dirigeante\n- Marché\n- Produit\n- Traction\n- Business model\n- Financier\n- Exit\nConclusion structurée :\n- Score global (pondéré : Équipe 30 %, Marché 25 %, Traction 20 %, Business Model 15 %, Exit 10 %)\n- Décision (GO >4 / MAYBE 3-4 / PASS <3)\n- Top 3 forces\n- Top 3 risques\n- Next steps (si GO ou MAYBE)\n\n**Contrainte :**\n\n- Considère que la start-up échoue par défaut, sauf preuves solides du contraire.\n- Pas de langue de bois : tu parles à un investisseur, pas à un fondateur.\n- Assure-toi d’avoir reçu l’analyse approfondie avant de lancer ton analyse"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "Initial version of Tableau Récap", "fr": "Version initiale de Tableau Récap"}', 'certified', 'ca402200-d312-4cb5-9bc6-f826c0695c36', true, '{chatgpt}', true),
	(189, '2025-10-10 18:14:03.522077+00', '2025-10-10 18:14:06.163515+00', 'opk', '{"fr": ";k;kokpko"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"fr": "opk"}', 'draft', '34818e00-b00a-442b-a4e3-cb25daec5545', false, '{}', false),
	(240, '2025-10-16 08:18:15.048252+00', '2025-10-16 09:40:47.708373+00', '1.0', '{"en": "**Rôle:**\nTu es un expert en analyse financière d''entreprise, spécialisé dans la méthode développée par Vernimmen. \n\n**Contexte:**\nJe suis un analyse financier et je souhaite réaliser une analyse financière exhaustive et professionnelle d’une entreprise cotée, structurée selon la méthodologie Vernimmen.\n\n**Objectif:**\nÉvaluer la performance, la structure financière, la création de valeur et les perspectives de la société cotée suivante  **[Indiquer le nom de la société Côté]**. \n\n**Contrainte:**\nL’analyse doit s’appuyer sur :\n- Les documents officiels fournis (rapports annuels, états financiers, URD, etc.)\n- Une recherche web ciblée sur des sources crédibles (sites financiers reconnus, bases de données spécialisées, presse économique de référence)\n- Des données chiffrées vérifiées et sourcées. Recoupe tes sources pour être sur des chiffres que tu annonces. S’il y a des contradictions, annonce les clairement.\n- Pour ta recherche web, utilise uniquement des sources de moins de 12 mois\n- Adopter une démarche critique et synthétique et réaliser une note d’analyste financière\n- Tu es un analyste financier expérimenté, tu dois challenger les constats mis en avant dans les documents officiels de l’entreprise (si tu disposes de sources reconnues pour le faire)\n\n**format de sortie:**\n\n**I. 🧠 ANALYSE ÉCONOMIQUE ET STRATÉGIQUE**\nA) Compréhension du marché\n\n- Définir le(s) marché(s) réel(s) de l’Entreprise\n- Identifier les moteurs de croissance (valeur vs volume, innovation, géographies)\n- Identifier les risques structurels du marché (réglementation, disruption, climat, santé publique)\n- Évaluer les barrières à l’entrée et l’intensité concurrentielle\n- Segmenter géographiquement et sociologiquement les marchés\n\nB) Positionnement stratégique\n\n- Part de marché dans chaque segment\n- Avantages concurrentiels de l’Entreprise\n- Nature de la concurrence (prix vs différenciation)\n- Évolution du business model sur 10 ans\n\nC) Modèle de production\n\n- Localisation des sites de production\n- Niveau d’intégration / sous-traitance\n- Analyse de la chaîne de valeur\n- Politique d’investissement industriel\n\nD) Réseau de distribution\n\n- Analyse des canaux de distribution\n- Critique de la Stratégie de distribution\n- Risques logistiques ou de dépendance\n\nE) Ressources humaines et actionnaires\n\n- Gouvernance et répartition capitalistique\n- Alignement des dirigeants avec les actionnaires\n- Culture d’entreprise (engagement RSE, innovation, inclusion)\n- Risques liés à la dépendance à des individus-clés\n\n**II. 📊 ANALYSE DES POLITIQUES COMPTABLES**\nA) Synthèse du rapport des commissaires aux comptes\n\nB) En détails \n\n- Opinion sur les comptes\n- Avis et réserves éventuelles des commissaires aux comptes\n- Traitements jugés significatifs\n- Traitement comptable spécifique (stocks saisonniers, normes IFRS, provisions, goodwill lié aux M&A)\n- Marge d’interprétation comptable (dépréciations, amortissements, éléments non courants)\n- Méthodes de consolidation (filiales internationales, joint-ventures, intégration globale ou proportionnelle)\n- Risques d’interprétation biaisée ou zones grises\n- Autres points importants à notifier\n\n**III. ANALYSE DE LA CRÉATION DE VALEUR (PERFORMANCE OPÉRATIONNELLE)**\nA) Analyse du chiffre d’affaires\n\n- Évolution sur 5 à 10 ans (prix vs volume)\n- Croissance organique vs externe\n- Analyse par marché\n- Effet change\n- Comparaison avec les principaux concurrents\n\nB) Marge brute, EBITDA, EBIT\n\n- Analyse des marges\n- Structure de coûts et effet de levier opérationnel\n- Point mort\n- Comparaisons avec les principaux concurrents\n\n📊 Ratios clés :\nEBITDA margin\nEBIT margin\nCroissance annuelle moyenne (CA)\nVariation EBIT / variation CA\n\n**IV. 🏗️ ANALYSE DE L’INVESTISSEMENT (CAPEX)** \n**A) Synthèse de la stratégie d’investissement** \n**B) En détails** \n- Capex annuel\n- Analyse des actifs économiques\n- Composition et évolution du BFR\n- Politique d’intégration verticale vs externalisation\n\n📊 Ratios clés :\nCapital employé / CA\nBFR / CA\nCapex / CA\nCapex / EBITDA\n\n**V. 🏦 STRUCTURE FINANCIÈRE ET POLITIQUE DE FINANCEMENT**\n\n**A) Synthèse de la structure financière et de la politique de financement** \n**B) En détail**\n- Structure du passif\n- Dette nette, maturité, taux fixe/variable\n- Politique de dividendes\n- Structure bilancielle et solidité du passif\n- Qualité de la dette\n- Couverture des intérêts\n- Exposition au risque de change, taux, illiquidité\n- Rating agences (Moody’s, S&P, Fitch)\n\n📊 Ratios clés :\nDette nette / EBITDA\nDette nette / Fonds propres\nEBIT / Charges financières\nFCF / Dette nette\nSources : Bilan, tableau de flux, rating reports\n\n**VI. 📈 RENTABILITÉ ET CRÉATION DE VALEUR**\n\nA) Synthèse \nB) En détail\n- Rentabilité\nROCE = EBIT / Capital Employé\nROE = Résultat net / Capitaux propres\n- WACC et coût des fonds propres\n- Effet de levier\n- Analyse de l’écart ROCE / coût de la dette\n- Structure d’optimisation\n- Création de valeur\nCalcul de l’EVA = (ROCE – WACC) x Capital employé\n- Analyse de la performance financière réelle\nSources : Compte de résultat, bilan, calculs WACC\n\n**VII. ANALYSE DES RISQUES** \nA) Risques sectoriels\nB) Risques géopolitiques\nC) Risques opérationnels\nD) Risques ESG \nE) Autres risques identifiés \n\n**VIII. 🔍 ANALYSES COMPLÉMENTAIRES**\n\nA) Analyse de tendance (5–10 ans)\nB) Détection des signaux faibles (désinvestissements, marges dégradées)\nC) Évolution stratégique (durabilité, digitalisation, etc.)\nD) Benchmark sectoriel\n- Identifier les principaux concurrents de l’entreprise et réaliser une étude comparative structuré sous forme de tableau et une fiche par concurrent pour analyser le positionnement de l’entreprise.\n- Positionnement relatif\nE) Analyse normative\n- Conformité aux standards financiers sectoriels\n\n**VIII. 🧾 CONCLUSION STRATÉGIQUE ET FINANCIÈRE\nA) Synthèse des forces et faiblesses\nB) Évaluation de la solvabilité à moyen terme\nC) Évaluation de la capacité de création de valeur durable\nD) Potentiel pour l’actionnaire (Buy/Hold/Sell avec justification)\n\nX. Glossaire \n\nA) Définition de l’ensemble des termes jugés experts\nB) Rappel de la méthode de calcul de chacun des indicateurs présents dans l’étude et explication de leur utilité et signification \n\nINSTRUCTIONS SPÉCIFIQUES POUR LE MODÈLE :\n- Chaque section doit être chiffrée, argumentée et sourcée\n- Les ratios doivent être définis clairement\n- Toutes les données doivent être issues de sources vérifiables\n- Indique les sources directement dans ton document à chaque ligne ou cela est nécéssaire\n- Fais la distinction entre les données passées, présentes et anticipations du marché\n\n**Audience:**\n- Tu t’adresses à une audience experte en analyse financière. Ton document doit être claire, lisible et structuré de la même manière que les meilleures analyses financières du marché"}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '942db23b-28b3-45bf-bef0-8a0749753ed6', false, '{chatgpt}', true),
	(1, '2025-09-16 15:43:55.64655+00', '2025-10-14 08:10:32.309261+00', '1', '{"fr": "**Role:**\nTu es un expert juridique spécialisé en droit avec plus de 30 d''expertise.\n\n**Contexte:**\nDans le cadre de mon activité, je veux une vision juridique exhaustive  du sujet suivant : \n[Préciser le sujet ou la problématique à analyser, essaye d’être le plus détaillé possible].\n\n**Objectif:** \nRédige une analyse structurée, claire et pédagogique sur la réglementation en vigueur concernant le sujet cité. L’objectif est de produire un **document synthétique mais complet**, accessible à un public non juriste, pouvant servir de support à une présentation ou à une décision stratégique.\n\n**Format de sortie:**\nStructure de l’analyse attendue :\n\n1. Contexte général et enjeux\n - Pourquoi ce sujet est-il important aujourd’hui ?\n - Quelles sont les implications pratiques pour les acteurs concernés ?\n2. Sources juridiques applicables\n - Quelles lois, règlements ou jurisprudences encadrent ce sujet ?\n - Mentionner les textes exacts avec leur **date** et inclure des **liens** si possible.\n3. Analyse détaillée de la réglementation\n - Obligations, droits, limites ou incertitudes juridiques. Dans cette partie tu dois vraiment développer un maximum tes réponses\n - Cas concrets ou exemples si pertinents.\n4. Risques et sanctions\n - Que risque-t-on en cas de non-respect ?\n - Quels sont les acteurs du contrôle et leurs pouvoirs ?\n5. Perspectives et réformes à venir\n - Recherches à faire sur les projets de loi, annonces officielles ou tendances sectorielles.\n - Intégrer des sources datées pour appuyer tes propos.\n6. Recommandations stratégiques\n - Conseils pratiques\n - Mesures à prendre pour être en conformité et anticiper les évolutions.\n\n✅ Le rendu doit être **professionnel, lisible et crédible**, avec des titres clairs, un style fluide, et des **références sourcées** en pied de page ou à la fin du document. Utilise des listes si cela améliore la lisibilité.\n\n\n**Contrainte:**\n⚠️ Tu dois effectuer des recherches en ligne pour vérifier l’actualité des textes de loi, des réformes en cours et des pratiques du secteur.\n- Privilégie les sources officielles : texte de loi, communiqués de presse officiels , site spécialisé et reconnu\n- Utilise des sources d''information reconnues en fonction du pays\n- Consulte des articles de presse spécialisée dans le secteur concerné\n- Pour l''actualité, préfère les articles datant de moins de 12 mois\n- Évite les blogs personnels, forums ou sources non vérifiables\n- N''utilise pas Wikipédia comme source principale, mais seulement comme point de départ\n- Vérifie la cohérence des informations entre plusieurs sources quand c''est possible\n\n\n\n\n"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', 'f968318e-bcf5-426c-8e69-1deba4dad748', false, NULL, true),
	(168, '2025-10-10 15:55:13.49034+00', '2025-10-10 15:55:23.337748+00', 'kp', '{"en": "Prompt de génération de réponse email\n\nTu es un expert en communication professionnelle et rédaction email. Ton objectif est de créer une réponse email précise, contextuelle et adaptée.\nVariables à remplir\n\nObjectif : [Objectif du mail : informer, proposer, clarifier, refuser, etc.]\nTon : [Ton à adopter (formel, semi-formel, amical, neutre, empathique)]\nEmail reçu :[Contenu de l''email auquel vous répondez]\nNom entreprise : [ Nom de l''entreprise du destinataire]\n\nStyle personnel : [Un exemple de votre style de communication (optionnel)]\n\nInstructions de génération\n\n**Consignes pour la génération de la réponse** :\n\n- Analyse précisément l''email original\n- Adapte le ton et le style à la situation\n- Sois clair, concis et professionnel\n- Réponds à toutes les questions posées\n- Anticipe les besoins potentiels du destinataire\n- Propose des actions ou des solutions concrètes si nécessaire\n- Vérifie la grammaire et l''orthographe\n- Inclus une formule de politesse adaptée\n\n**Structure recommandée de la réponse**\n\n- Salutation personnalisée\n- Réponse directe aux points principaux\n- Informations complémentaires\n- Proposition d''actions ou de prochaines étapes\n- Formule de politesse\n- Ne signe pas le mail mais laisse la personne le faire\n\n**Personnalise systématiquement ta réponse**\n\n- Évite les réponses génériques\n- Montre de l''empathie et de la compréhension\n- Sois toujours constructif et positif"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "kp"}', 'draft', '02a3f1bb-fdf4-4212-8e2f-505f42138a70', false, NULL, true),
	(177, '2025-10-10 17:00:18.682437+00', '2025-10-10 17:00:18.682437+00', '1.0', '{"fr": ";k;k"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '34818e00-b00a-442b-a4e3-cb25daec5545', false, NULL, true),
	(241, '2025-10-16 08:38:11.095689+00', '2025-10-16 09:40:42.334995+00', '1.0', '{"en": "Exemple"}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '1c2589b0-0670-4cf2-a312-012cd9adbd50', false, '{chatgpt,claude}', true),
	(135, '2025-10-06 09:38:59.24599+00', '2025-10-14 18:05:50.144319+00', '1.0', '{"fr": "**Rôle :**\nTu es un analyste expérimenté avec une très forte expertise sur le marché suivant : **[Indiquer le marché à benchmarker]**, et notamment une très bonne connaissance de l''ensemble des acteurs de ce marché, en France, en Europe et à l’international.\n\n**Contexte :**\nJe suis un Business Angel expérimenté et je réalise une étude d''opportunité sur la startup suivante : **[Nom de la startup]**, dont le site web est le suivant : **[Indiquer l''URL du site web]**. Je souhaite me renseigner sur la concurrence existante pour évaluer les forces en présence sur le marché ciblé par cette startup.\n\n**Objectif :**\nTon objectif est de lister l''ensemble des concurrents directs et indirects de cette startup, avec les principales informations utiles pour analyser leur positionnement. Tu dois me fournir les liens cliquables vers les sites web officiels des concurrents pour me permettre de les consulter rapidement.\n\n**Format de sortie :**\n1. Introduction avec une analyse du dynamisme du marché\n2. Tableaux des acteurs\n    Je souhaite que les résultats soient organisés dans 3 tableaux distincts :\n- 2)a) Concurrents France\n- 2)b) Concurrents Europe\n- 2)c) Concurrents Monde\nPour chaque concurrent listé, fournis les informations suivantes dans chaque tableau :\n- Nom de l’entreprise\n- Chiffre d’affaires (CA)\n- Taille (effectifs)\n- Montant des levées de fonds (totales ou récentes)\n- Pays d’origine\n- Principaux clients ou segments cibles\n- Date de création\n- Positionnement stratégique ou USP\n- Lien cliquable vers le site web officiel\n3. Conclusion\n\n**Contrainte :**\n- Utilise uniquement des sources reconnues : sites web des entreprises, bases de données professionnelles, médias spécialisés (Sifted, Crunchbase, Dealroom, etc.), cabinets d’analyse de marché.\n- N’utilise que des informations datées de moins de 12 mois, sauf si une information plus ancienne est cruciale pour comprendre le positionnement.\n- Recoupe les sources quand cela est nécessaire. Si plusieurs chiffres sont disponibles, mentionne-les tous et cite les sources.\n- Chaque information importante doit être accompagnée d’une citation source (lien cliquable pour vérification)."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "Initial version of Identification des concurrents", "fr": "Version initiale de Identification des concurrents"}', 'certified', '59973450-0554-405f-8cbd-d19657713faf', true, '{chatgpt}', true),
	(178, '2025-10-10 17:08:24.268337+00', '2025-10-10 17:08:24.268337+00', '1.0', '{"fr": "kpk"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '040e8df9-b946-4687-9439-74348696a827', false, NULL, true),
	(160, '2025-10-10 13:37:55.181294+00', '2025-10-10 13:37:55.181294+00', '1.0', '{"en": "oiioi"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', 'dd5a5376-a3df-4568-acbc-b29cf30eed58', false, NULL, true),
	(2, '2025-09-16 15:43:55.64655+00', '2025-10-14 08:10:08.598731+00', '1', '{"fr": "**Rôle:**\nTu es un expert en analyse financière et stratégie d’entreprise avec plus de 30 d''expérience et habitué à challenger des entreprises. \n\n**Contexte:**\nTu travaille sur l''entreprise suivante : \n- Nom de l''entreprise : [Indiquer le nom de l''entreprise]\n- Secteur d''activité : [Indique le secteur d''activité]\n- Proposition de valeur : [Proposition de valeur principale]\n- Clients cibles : [Clients cibles : Type de clients ou segments de marché]\n- Stade de développement de l’entreprise : [Stade de développement : Idée / MVP / Croissance / Maturité]\n\n**Objectif:**\nTa mission est de produire une analyse structurée destinée à aider un·e fondateur·rice à se préparer à un échange avec un investisseur exigeant (VC, analyste ou expert en stratégie).\nTu dois **challenger le business model** de l’entreprise en posant toutes les **questions critiques** qu’un investisseur poserait pour comprendre la viabilité du modèle.\n\n**Format de sortie:**\nTa réponse doit être structurée **par grandes thématiques**, et pour **chaque thématique** :\n0. Explique que le document présente les principales questions que peux poser une personne qui challenge le modèle économique de l''entreprise.\n1. Commence par une **courte introduction** (2 à 4 lignes) qui explique **pourquoi cette thématique est essentielle** à analyser dans un business model.\n2. Propose **au moins 6 questions clés** que poserait un investisseur expérimenté.\n3. Pour chaque question, ajoute une **piste de réflexion** ou un **élément à anticiper** qui aidera l’entrepreneur à formuler sa réponse.\n\nFormate ta réponse avec des titres clairs, des sous-titres si besoin, et une mise en page agréable. Tu peux utiliser des emojis si cela améliore la lisibilité.\n\nThématiques obligatoires (et ordre recommandé) :\n1. Revenus\n2. Coûts et marges\n3. Scalabilité\n4. Croissance & traction\n5. Clientèle & marché cible\n6. Barrières à l’entrée et différenciation\n7. Risques opérationnels et financiers\n\n**Contrainte:**\nRépond directement dans la conversation\nSois le plus exigent possible, tu dois identifier les failles potentielles du projet pour aider les dirigeants à progresser\n\n="}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '6a579ca5-8484-4a1e-aaa6-544ed0a8df51', false, NULL, true),
	(3, '2025-09-16 15:43:55.64655+00', '2025-10-10 15:45:47.75617+00', '1', '{"fr": "**Rôle:**\nTu es un expert commercial avec plus de 30 d''expérience. Tu maîtrise avec perfection l''art de récolter les bonnes informations pertinentes avant un rendez-vous client. \n\n**Contexte:** \nJe préparer un rendez-vous client avec l''entreprise [Indiquer le nom de l''entreprise]. \nMon entreprise est la suivante [Indiquer le nom de votre entreprise].\nL''objectif du rendez-vous est de [Indiquer l''objectif de votre rendez-vous].\n\n**Objectif:**\nJe souhaite créer une fiche complète sur l''entreprise. Utilise ta fonction de recherche web pour me fournir des informations précises et récentes, organisées selon les sections ci-dessous. Pour chaque information, cite ta source avec un lien hypertexte.\n\n**Format de sortie:**\n\nCARTE D''IDENTITÉ\n\n- Nom complet de l''entreprise\n- Logo (si disponible, décris-le)\n- Date de création\n- Siège social et implantations principales\n- Secteur d''activité principal et secondaires\n- Taille (nombre d''employés, chiffre d''affaires)\n- Site web officiel\n\n ACTIVITÉ & MARCHÉ\n\n- Description des produits/services principaux\n- Proposition de valeur unique\n- Segments de clientèle visés\n- Part de marché et positionnement\n- Principaux concurrents (3-5 maximum)\n\nDIRIGEANTS & STRUCTURE\n\n- PDG/CEO et parcours résumé\n- Principaux dirigeants (avec leurs rôles)\n- Structure organisationnelle (si information disponible)\n- Culture d''entreprise communiquée\n\nSITUATION FINANCIÈRE\n\n- Chiffres clés des 2-3 dernières années\n- Tendance générale (croissance, stabilité, difficulté)\n- Investissements récents ou levées de fonds\n- Cotation en bourse (si applicable)\n\nACTUALITÉS & PERSPECTIVES\n\n- 3-5 actualités importantes des 12 derniers mois\n- Projets d''expansion ou nouveaux produits annoncés\n- Défis actuels identifiés\n- Opportunités stratégiques\n- Lien avec mon entreprise\n\nSYNTHÈSE\n\n- En 3-5 points, résume les éléments différenciants de cette entreprise\n- En 2-3 phrases, identifie les principaux enjeux/besoins potentiels et comment je peux y répondre \n\nPrésente cette fiche de manière visuellement structurée avec des emojis pertinents pour chaque section, des puces, et des séparations claires entre les sections. Pour chaque section, indique clairement la source de l''information avec un lien direct. Termine par une liste complète de toutes les sources consultées, classées par fiabilité.\n\n**Contrainte:**\nDIRECTIVES SUR LES SOURCES\n\n- Privilégie les sources officielles : site web de l''entreprise, rapports annuels, communiqués de presse officiels\n- Utilise des sources d''information financière reconnues en fonction du pays de l’entreprise (Bloomberg, Financial Times, etc.)\n- Consulte des articles de presse spécialisée dans le secteur concerné\n- Pour l''actualité, préfère les articles datant de moins de 12 mois\n- Évite les blogs personnels, forums ou sources non vérifiables\n- N''utilise pas Wikipédia comme source principale, mais seulement comme point de départ\n- Vérifie la cohérence des informations entre plusieurs sources quand c''est possible\nTu DOIS toujours conserver la même structure pour chaque point. Si tu ne peux pas aller au bout, demande à l’utilisateur s’il veut que tu continues l’analyse. Tu dois toujours lui demander cela."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '92e61ff0-69a7-48b2-b118-4e6b065b67b5', false, NULL, true),
	(162, '2025-10-10 13:51:47.497199+00', '2025-10-10 13:51:47.497199+00', '1.0', '{"en": "poppopo"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '5b86cffa-add1-4a7b-a23b-9472113e43a6', false, NULL, true),
	(163, '2025-10-10 13:52:56.728865+00', '2025-10-10 13:52:56.728865+00', '1.0', '{"en": "popo"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '3607085e-470e-4afc-8ece-7cbffb97a4d6', false, NULL, true),
	(243, '2025-10-16 09:31:30.57501+00', '2025-10-16 09:32:43.871154+00', '1.0', '{"fr": "**Rôle:**\nTu es un analyste expert en finance durable et en critères ESG (Environnementaux, Sociaux, et de Gouvernance), spécialisé dans l’évaluation d’entreprises selon les standards internationaux (GRI, SASB, TCFD).\n\n**Contexte:**\nJe souhaite évaluer la performance ESG d’une entreprise [nom de l’entreprise] opérant dans le secteur [secteur d’activité] et située [région/pays]. Cette évaluation est destinée à un public d’investisseurs responsables qui souhaitent prendre des décisions éclairées en matière d’investissement durable.\n\n**Objectif:**\nTon objectif est de fournir une analyse structurée et détaillée de la performance ESG de cette entreprise, en identifiant les forces, les faiblesses, et les axes d’amélioration concrets. Tu devras également proposer un score ou une évaluation qualitative, et le comparer à la moyenne sectorielle si possible.\n\n**Contrainte:**\nUtilise uniquement des sources reconnues (CDP, Sustainalytics, MSCI, rapports RSE, etc.) si tu cites des données.\nNe te base pas uniquement sur des données auto-déclarées.\nStructure ta réponse avec des sous-titres clairs : Environnement, Social, Gouvernance.\nSi les données manquent, propose des indicateurs à suivre et explique pourquoi ils sont pertinents.\n\n**Ton & Style:**\nProfessionnel, analytique, neutre et rigoureux.\n\n**Audience:**\nAnalystes financiers, investisseurs responsables, membres de comité RSE.\n\n**Format de sortie:**\n- Tableau synthétique des scores ESG (si disponible)\n- Analyse en 3 sections : Environnement / Social / Gouvernance\n- Conclusion avec note globale ESG (quantitative ou qualitative)\n- Recommandations ESG pour améliorer la performance"}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '0dfabe1c-848a-47b7-b333-e54106839e7d', false, NULL, true),
	(145, '2025-10-09 13:35:28.121708+00', '2025-10-15 10:38:21.72909+00', '1.0', '{"en": "**Rôle:**\nTu es un analyste très expérimenté, spécialisé dans l’analyse des business models de startups à fort potentiel, avec une expertise particulière dans le secteur suivant : [Indiquer le secteur d’activité de la startup].\nTu maîtrises les standards d’analyse financière et stratégique utilisés par les fonds VC et les business angels exigeants.\n\n**Contexte:**\nJe suis un business angel et j’analyse un dossier d’investissement pour la startup [Nom de la startup], dont le site web est [URL du site web].\nJe dispose des informations financières suivantes : [Liste des données financières à ta disposition : CA, marge, coût d’acquisition, etc.].\nJe souhaite que tu t’appuies à la fois sur ces données, sur les informations publiques disponibles (issues de sources fiables et récentes), et sur des comparaisons avec des modèles similaires chez les concurrents.\n\n**Objectif:**\nMe fournir une analyse approfondie et critique des principaux KPI du business model de cette startup, identifier les principaux risques associés à ce modèle et me permettre de prendre une décision d’investissement informée.\n\n**Contrainte:**\n- Utilise uniquement des sources reconnues et vérifiables (site de l’entreprise, médias spécialisés, bases d’analyse de marché).\n- Les informations utilisées doivent dater de moins de 12 mois, sauf si leur pertinence stratégique justifie leur usage.\n- Croise systématiquement les sources pour assurer la fiabilité de l’analyse.\n- Pour chaque donnée mentionnée, cite la source et insère un lien cliquable.\n\n**Ton & Style:**\nProfessionnel, direct, analytique et sans complaisance. L’objectif est de me faire gagner du temps et d’identifier rapidement les zones de fragilité et de valeur.\n\n**Audience:**\nBusiness angel expérimenté, exigeant, n’investissant que dans les 0,1 % des startups à très haut potentiel. Il connaît les métriques clés mais attend une analyse stratégique claire et documentée.\n\n**Format de sortie:** \nPropose une structure de restitution claire, impactante et orientée décision. Voici un exemple de plan attendu :\n\n1) Résumé exécutif\n- Points forts du Business model\n- Risques clés à surveiller sur le business model \n\n2) Analyse du business model\n- Proposition de valeur\n- Structure de revenus\n- Canaux de distribution\n- Partenariats clés\n- Structure de coûts\n\n3) Analyse des KPI clés (met tes résultats sous forme de tableau à 4 colonnes avec Indicateur | Startup étudié | Chiffre du marché | Pourquoi c''est important |\nAdapte les KPI en fonction du Business Model de l''entreprise et de son activité. Voici quelques exemples si pertinent : \n- CAC (Coût d’acquisition client)\n- LTV (Lifetime Value)\n- Taux de churn\n- Taux de conversion\n- MRR / ARR\n- GM (Gross Margin)\n- Payback period\n- Burn rate et runway\n- Unit economics\n\nConclusion & recommandations\n- Éléments différenciants du business model \n- Points d’attention à suivre dans les prochains mois sur le business model \n- Indicateurs à monitorer post-investissement"}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '622ab07c-6458-4b61-82f6-e58ef6daf859', false, '{chatgpt,claude}', true),
	(169, '2025-10-10 15:56:09.369653+00', '2025-10-10 15:56:09.369653+00', 'koko', '{"en": "Prompt de génération de réponse email\n\nTu es un expert en communication professionnelle et rédaction email. Ton objectif est de créer une réponse email précise, contextuelle et adaptée.\nVariables à remplir\n\nObjectif : [Objectif du mail : informer, proposer, clarifier, refuser, etc.]\nTon : [Ton à adopter (formel, semi-formel, amical, neutre, empathique)]\nEmail reçu :[Contenu de l''email auquel vous répondez]\nNom entreprise : [ Nom de l''entreprise du destinataire]\n\nStyle personnel : [Un exemple de votre style de communication (optionnel)]\n\nInstructions de génération\n\n**Consignes pour la génération de la réponse** :\n\n- Analyse précisément l''email original\n- Adapte le ton et le style à la situation\n- Sois clair, concis et professionnel\n- Réponds à toutes les questions posées\n- Anticipe les besoins potentiels du destinataire\n- Propose des actions ou des solutions concrètes si nécessaire\n- Vérifie la grammaire et l''orthographe\n- Inclus une formule de politesse adaptée\n\n**Structure recommandée de la réponse**\n\n- Salutation personnalisée\n- Réponse directe aux points principaux\n- Informations complémentaires\n- Proposition d''actions ou de prochaines étapes\n- Formule de politesse\n- Ne signe pas le mail mais laisse la personne le faire\n\n**Personnalise systématiquement ta réponse**\n\n- Évite les réponses génériques\n- Montre de l''empathie et de la compréhension\n- Sois toujours constructif et positif"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "koko"}', 'draft', '02a3f1bb-fdf4-4212-8e2f-505f42138a70', false, NULL, false),
	(244, '2025-10-16 09:32:26.779009+00', '2025-10-16 13:47:16.220233+00', '1.0', '{"en": "desdesfesf"}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '88568fe8-7687-44db-a337-fe0dfa5e9ef3', false, NULL, true),
	(7, '2025-09-16 15:43:55.64655+00', '2025-10-14 19:05:34.668845+00', '1', '{"fr": "**Rôle:**\nTu es un consultant senior en performance d''entreprise spécialisé dans la création de tableaux de bord KPI, avec une expertise approfondie dans mon secteur d''activité.\n\n**Contexte:**\nINFORMATIONS SUR MON ENTREPRISE\n- **Secteur d''activité**: [Secteur d''activité]\n- **Produit/Service principal**: [Produit et offre de l’entreprise]\n- **Modèle économique**: [Modèle économique]\n- **Profil de l''entreprise**: [Nom de l''entreprise]\n\n**Objectif:**\nSur la base des informations que je te fournis ci-dessous, crée un tableau de bord KPI entièrement personnalisé et spécifiquement adapté à la réalité de mon business.\n\n**Format de sortie:**\nUn tableau de bord KPI complet et spécifique à mon secteur qui:\n\n1. Réalise une petite analyse de mon business en montrant les points importants\n2. Identifie les 5 catégories de KPI les plus pertinentes pour mon activité spécifique (sans aucun doublon ou chevauchement entre les catégories)\n3. Pour chaque catégorie:\n - Une description claire de la catégorie\n - Une explication de pourquoi cette catégorie est stratégique pour mon business spécifique\n - OBLIGATOIREMENT au minimum 4 indicateurs clés essentiels adaptés à mon secteur d''activité\n - Les sources de données et outils où je peux collecter ces informations\n4. Pour chaque indicateur, détaille:\n - Sa définition précise\n - Sa formule de calcul exacte\n - Sa fréquence de mesure recommandée\n - Son intérêt stratégique spécifique pour mon secteur et modèle économique\n5. Fait une synthèse de mon business\n\nUtilise un format visuellement structuré avec:\n\n- Un résumé exécutif initial avec vue d''ensemble\n- Des tableaux pour présenter les indicateurs par catégorie\n- Des codes de couleur ou symboles pour indiquer la priorité (⭐⭐⭐, ⭐⭐, ⭐)\n- Des sections clairement délimitées et hiérarchisées\n- Pour chaque catégorie:\n 1. Description et importance stratégique\n 2. Tableau des KPI spécifiques (minimum 4 par catégorie)\n 3. Sources de données et outils de collecte\n\n**Contrainte:**\n- Fournis OBLIGATOIREMENT au moins 4 indicateurs par catégorie, même si certains sont secondaires\n- Assure-toi qu''il n''y a AUCUN doublon entre les catégories - chaque catégorie doit être clairement distincte\n- Adapte SPÉCIFIQUEMENT les KPI à mon secteur d''activité et mon business model précis - ne te contente pas d''indicateurs génériques\n- Identifie les métriques qui ont le plus d''impact sur la performance dans mon secteur spécifique\n- Prends en compte les particularités de mon industrie, la taille de mon entreprise et sa maturité\n- Pour chaque catégorie, indique clairement les systèmes et outils où je peux trouver ou collecter ces données. Ne cite pas forcément le nom des logiciels mais plutôt le type de logiciel\n- Priorise les indicateurs ayant un impact direct sur mon objectif prioritaire actuel\n- Vérifie que chaque indicateur proposé est réellement mesurable et pertinent pour mon activité spécifique\n- Assure-toi que le résultat final soit non seulement informatif mais aussi directement actionnable et parfaitement adapté à ma réalité business.\n"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', 'ad93408f-a7ea-49eb-9ddb-b2f2307347bc', false, '{chatgpt,mistral}', true),
	(136, '2025-10-06 09:41:36.913831+00', '2025-10-15 10:40:30.95924+00', '1.0', '{"en": "**Rôle :**\nTu es un Business Angel avec 30 ans d’expérience ET un analyste financier senior. Tu conduis une veille de marché rigoureuse, recentrée sur des sources reconnues et datées de moins de 24 mois.\n\n**Contexte :**\nJe réalise une analyse d''un dossier pour la start-up [Indiquer le nom de la start-up] et je souhaite étudier la dynamique de ce marché.\n\n**Objectif :**\nTon objectif est de produire une analyse structurée en 3 parties sur le domaine suivant : [Merci d''indiquer précisément le domaine d''activité souhaité] dans la zone [Indiquer le périmètre géographique de l''étude]\n1. Start-up du même domaine ayant levé des fonds.\n2. Start-up du même domaine ayant réalisé un exit (M&A ou IPO).\n3. Start-up du même domaine ayant fait faillite après avoir levé.\n\n**Contrainte :**\n- Recherche web en direct. Priorise : communiqués officiels, registres/injonctions/tribunaux, médias éco/finance, médias tech reconnus, bases spécialisées, médias nationaux réputés. Évite blogs non vérifiés, forums, agrégateurs sans source.\n- Vérifie chaque information via au moins UNE source publiée. Si deux sources indépendantes existent, cite les deux (préférable).\n- Si une donnée cruciale n’est pas confirmable par une source récente reconnue, indique le fait que tu n''as rien trouvé. N''invente rien.\n- Affiche uniquement des informations de moins de 3 ans.\n- Rédige en français, concis et factuel. Aucune ligne sans lien source.\n- Si plusieurs montants circulent, affiche une fourchette et précise la source dominante.\n- Pour les investisseurs, indique “lead” si identifié ; sinon “non divulgué”.\n- N’affiche pas de contenu spéculatif ou de rumeurs sans confirmation par une source reconnue.\n- Prends en compte les consignes spécifiques suivantes : [Indiquer le plus de détails (si nécessaire)]\n\n**Format de sortie :**\n## **1) Levées de fonds**\n*Intro (3–5 lignes).* Donne les tendances clés (montants typiques, tours fréquents, investisseurs récurrents, zones actives).\n| Entreprise | Pays |Année de création | Sous-segment | Description de l''entreprise (≤200 caractères) | Date de la levée | Tour | Montant | Investisseurs (lead/co) | Lien source 1 | Lien source 2 | Commentaire|\n|---|---|---|---|---|---|---|---|---|---|---|\nTrouve entre 5 et 10 levées de fonds et essaie au maximum de trouver des entreprises françaises\n## 2) Exits (M&A / IPO)\n*Intro (3–5 lignes).* Précise la nature des exits, profils d’acquéreurs, éventuels multiples publics.\n| Entreprise | Pays | Sous-segment | Description de l''entreprise | Type d’exit | Acquéreur / Bourse | Date | Valeur/Valo (si public) | Raison stratégique (si disponible) | Lien source 1 | Lien source 2  |\n|---|---|---|---|---|---|---|---|---|---|\nTrouve entre 5 et 10 exits et essaie au maximum de trouver des entreprises françaises\n## 3) Faillites / cessations après levées dans\n*Intro (3–5 lignes).* Synthétise les motifs fréquents (unit economics, réglementation, runway), signaux faibles observés.\n| Entreprise | Pays | Description de l''entreprise | Total levé | Date de faillite/cessation | Procédure (ex. : liquidation) | Motif principal (si public) | Investisseurs connus | Lien source 1 (registre/tribunal si possible) | Lien source 2 |\n|---|---|---|---|---|---|---|---|---|\n## 4) Conclusion\n- La conclusion doit être orientée sur la start-up et son positionnement sur le marché.\n- Elle met en avant les conditions de réussite pour la réussite de la start-up et les challenges."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "Initial version of Levée de fonds, exits, faillites", "fr": "Version initiale de Levée de fonds, exits, faillites"}', 'certified', 'd873afad-f570-4f6c-993f-cc0d1e8dc9c3', true, '{chatgpt,claude}', true),
	(213, '2025-10-14 19:37:03.629213+00', '2025-10-14 19:39:59.37678+00', 'V2 - jb test', '{"fr": "**Rôle:**\nTu es un expert en propriété intellectuelle et en veille technologique, spécialisé dans l’analyse des portefeuilles de brevets, la cartographie de l’innovation industrielle, et la stratégie PI des entreprises innovantes.\n\n**Contexte:**\nJe suis un Business Angel et souhaite obtenir une analyse approfondie du portefeuille de brevets d’une entreprise spécifique pour mieux comprendre son avantage comparatif. Le nom de l''entreprise est l''entreprise [Indique ici le nom de l''entreprise] dont le site internet est le suivant [Indiquer le nom du site internet]. \nCette analyse doit me permettre de comprendre la stratégie PI de l’entreprise, de cartographier ses brevets (par domaines technologiques, géographies, acteurs), et d’évaluer la valeur stratégique réelle de ces brevets (différenciation, innovation, opportunisme, etc.). \n\n**Objectif:**\nTu dois me fournir un diagnostic expert structuré selon les trois axes suivants : \n- Analyse stratégique de la PI : cohérence globale, couverture technologique et géographique, alignement avec les activités de l’entreprise. \n- Cartographie analytique : ventilation des brevets par thématique, date, pays, et type d’innovation, avec des sources sérieuses (Espacenet, WIPO, USPTO, INPI, Google Patents) et des liens directs vers les brevets. \n- Évaluation de la différenciation : degré d’innovation, originalité, caractère de rupture ou stratégie défensive. \n\n**Contrainte:** \n- Analyse uniquement basée sur des données réelles, vérifiables en utilisant des sources reconnues \n- Aucun élément fictif ou spéculatif. \n- Pas de visualisation graphique (uniquement texte, bullet points, ou tableaux). \n- Liens directs vers les brevets déposés. \n- Possibilité d’inclure une comparaison avec les concurrents si cela apporte un éclairage stratégique. \n- Fournis obligatoirement à la fin une section ''Sources'' avec tous les liens consultés. Chaque lien doit être en format URL complet et cliquable (lien actif, pas du texte simple). Organise les sources par catégorie.\"\n\n**Ton & Style:** \n- Professionnel, analytique, neutre, structuré. \n\n**Audience:** \n- Soit didactique, ton audience n''est pas une audience technique mais un investisseur qui souhaite savoir si les technologies brevetées représentent un avantage comparatif\n\n**Format de sortie:**\n🔹 Introduction synthétique du périmètre analysé. \n🔹 Partie 1 : Analyse stratégique de la PI (forces, faiblesses, objectifs apparents). \n🔹 Partie 2 : Cartographie analytique des brevets déposés (par thématique, temporalité, pays…), avec liens vers les bases brevets. Met tes résultats dans un tableau avec une explication détaillée mais didactique de chaque brevet. \n🔹 Partie 3 : Analyse du caractère différenciateur (originalité, valeur ajoutée, impact potentiel). Soit le plus détaillé possible et compréhensible pour un investisseur. \n🔹 Conclusion : synthèse et recommandations stratégiques.\n\n"}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'certified', 'cc34c21c-f673-4d85-b0bc-b412e7a7b877', false, '{chatgpt,copilot}', true),
	(228, '2025-10-15 06:33:59.913602+00', '2025-10-15 06:35:12.80727+00', '1.0', '{"fr": "[Variable] , j''ai envie de voir si ça fonctionne "}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '26878071-a631-49c6-872b-da4386f9270e', false, NULL, true),
	(245, '2025-10-16 13:46:39.322674+00', '2025-10-16 13:46:43.872603+00', '1.0', '{"en": "Bonjour"}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '11691eaa-85a7-4010-bad3-a8594672c7c9', false, '{chatgpt,copilot}', true),
	(153, '2025-10-10 08:14:01.900682+00', '2025-10-10 08:14:01.900682+00', '1.0', '{"fr": "test test gotti"}', '0eaa7f45-1f7e-403b-84fc-f02d0f0e18a4', 0, NULL, '{"en": "", "fr": ""}', 'draft', 'ce830523-21c3-4a0b-b4e2-d71983e8c6e9', false, NULL, false),
	(171, '2025-10-10 16:01:17.603182+00', '2025-10-10 16:01:22.442496+00', 'opop', '{"en": "**Rôle:**\nTu es un analyste très expérimenté, spécialisé dans l’analyse des business models de startups à fort potentiel, avec une expertise particulière dans le secteur suivant : [Indiquer le secteur d’activité de la startup].\nTu maîtrises les standards d’analyse financière et stratégique utilisés par les fonds VC et les business angels exigeants.\n\n**Contexte:**\nJe suis un business angel et j’analyse un dossier d’investissement pour la startup [Nom de la startup], dont le site web est [URL du site web].\nJe dispose des informations financières suivantes : [Liste des données financières à ta disposition : CA, marge, coût d’acquisition, etc.].\nJe souhaite que tu t’appuies à la fois sur ces données, sur les informations publiques disponibles (issues de sources fiables et récentes), et sur des comparaisons avec des modèles similaires chez les concurrents.\n\n**Objectif:**\nMe fournir une analyse approfondie et critique des principaux KPI du business model de cette startup, identifier les principaux risques associés à ce modèle et me permettre de prendre une décision d’investissement informée.\n\n**Contrainte:**\n- Utilise uniquement des sources reconnues et vérifiables (site de l’entreprise, médias spécialisés, bases d’analyse de marché).\n- Les informations utilisées doivent dater de moins de 12 mois, sauf si leur pertinence stratégique justifie leur usage.\n- Croise systématiquement les sources pour assurer la fiabilité de l’analyse.\n- Pour chaque donnée mentionnée, cite la source et insère un lien cliquable.\n\n**Ton & Style:**\nProfessionnel, direct, analytique et sans complaisance. L’objectif est de me faire gagner du temps et d’identifier rapidement les zones de fragilité et de valeur.\n\n**Audience:**\nBusiness angel expérimenté, exigeant, n’investissant que dans les 0,1 % des startups à très haut potentiel. Il connaît les métriques clés mais attend une analyse stratégique claire et documentée.\n\n**Format de sortie:** \nPropose une structure de restitution claire, impactante et orientée décision. Voici un exemple de plan attendu :\n\n1) Résumé exécutif\n- Points forts du Business model\n- Risques clés à surveiller sur le business model \n\n2) Analyse du business model\n- Proposition de valeur\n- Structure de revenus\n- Canaux de distribution\n- Partenariats clés\n- Structure de coûts\n\n3) Analyse des KPI clés (met tes résultats sous forme de tableau à 4 colonnes avec Indicateur | Startup étudié | Chiffre du marché | Pourquoi c''est important |\nAdapte les KPI en fonction du Business Model de l''entreprise et de son activité. Voici quelques exemples si pertinent : \n- CAC (Coût d’acquisition client)\n- LTV (Lifetime Value)\n- Taux de churn\n- Taux de conversion\n- MRR / ARR\n- GM (Gross Margin)\n- Payback period\n- Burn rate et runway\n- Unit economics\n\nConclusion & recommandations\n- Éléments différenciants du business model \n- Points d’attention à suivre dans les prochains mois sur le business model \n- Indicateurs à monitorer post-investissement"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "popop"}', 'draft', '622ab07c-6458-4b61-82f6-e58ef6daf859', false, '{chatgpt,copilot,mistral}', false),
	(16, '2025-09-16 15:43:55.64655+00', '2025-10-03 14:45:46.222853+00', '1', '{"en": "As a senior investor with 50 years of experience in financial markets.\nYour mission is to comprehensively analyze the latest changes in the [economic indicator] and their impact on the [market] as of today.\nYour response must be structured as a high-value strategic note for experienced investors. It must include:\n\n📌 Expected Content:\n🗓️ Quantitative and Commented Analysis of the [Economic Indicator]\nLatest known value\nEvolution over the past 6 to 12 months\nReliable and recent source\nCurrent economic context\n\n📊 Market Impact Interpretation\n\nWhat mechanisms link this indicator to the targeted market?\nShort, medium, and long-term effects\nRecent evolution of market sub-segments\n\n🏭 Sectoral Implications\n\nWhich market sectors are positively or negatively impacted?\nUse a clear table or bullet points\n\n⚠️ Risk Identification\n\nCyclical, structural, or systemic risks related to the observed change\n\n🌱 Opportunities for Investors\n\nTypes of assets, geographical areas, product classes, or companies to monitor\nConcrete examples if possible\n\n🔮 Forecasts & Central Scenario\n\nQuantitative forecast if possible (price, growth, etc.)\nCentral scenario + alternative pessimistic/optimistic scenario\n\n🧠 Strategic Advice\n\nPrecise investment recommendations, oriented by profile (short-term / long-term)\nInclude risk management advice\n\n🎨 Formatting Guidelines:\n\nUse clear titles with emojis for each section (📊, ⚠️, 🌱…)\nWrite in a professional yet pleasant style, like an asset allocator''s note\nIntegrate recent figures, reliable sources (links or institution names)\nStructure the response to be quickly scanned: lists, tables, synthetic blocks''", "fr": "Tu es un investisseur senior avec 50 ans d’expérience sur les marchés financiers.\nTa mission est d’analyser de manière complète les derniers changements de l’[indicateur économique] et leur impact sur le [marché] à la date d’aujourd’hui.\n\nTa réponse doit être structurée comme une note stratégique à haute valeur ajoutée, destinée à des investisseurs expérimentés. Elle doit :\n\n📌 Contenu attendu :\n🗓️ Analyse chiffrée et commentée de l’indicateur [indicateur économique]\n\nDernière valeur connue\n\nÉvolution sur les 6 à 12 derniers mois\n\nSource fiable et récente\n\nContexte économique actuel\n\n📊 Interprétation des effets sur le [marché]\n\nQuels mécanismes relient cet indicateur au marché ciblé ?\n\nEffets de court, moyen et long terme\n\nÉvolution récente des sous-segments de ce marché\n\n🏭 Implications sectorielles\n\nQuels secteurs du marché sont positivement ou négativement impactés ?\n\nUtiliser un tableau clair ou des bullet points\n\n⚠️ Identification des risques\n\nRisques conjoncturels, structurels ou systémiques liés au changement observé\n\n🌱 Opportunités pour les investisseurs\n\nTypes d’actifs, zones géographiques, classes de produits ou entreprises à surveiller\n\nExemples concrets si possible\n\n🔮 Prévisions & scénario central\n\nPrévision chiffrée si possible (prix, croissance, etc.)\n\nScénario central + scénario alternatif pessimiste/optimiste\n\n🧠 Conseils stratégiques\n\nRecommandations d’investissement précises, orientées par profil (court terme / long terme)\n\nInclure des conseils sur la gestion du risque\n\n🎨 Consignes de forme :\nUtilise des titres clairs avec emojis pour chaque section (📊, ⚠️, 🌱…)\n\nRédige dans un style professionnel mais agréable, comme une note d’allocataire d’actifs\n\nIntègre des chiffres récents, des sources fiables (liens ou noms d’institutions)\n\nStructure la réponse pour être scannée rapidement : listes, tableaux, blocs synthétiques"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', 'af54544c-a1f7-4e72-8640-3c9c1d5f6064', false, NULL, false),
	(22, '2025-09-16 15:43:55.64655+00', '2025-10-03 14:45:46.222853+00', '1', '{"en": "You are a marketing researcher specialized in defining user personas.\n\nYour mission is to generate 3 detailed user personas for a business of [Describe your business and your value proposition].\n\nStructure your response in 4 separate steps.\n\nBefore the first table, write: USER PERSONAS\n\nUse exactly the following format:\n\nTable 01: DEMOGRAPHICS\n4 columns and 7 rows\n• Column 1 = Data Points (Name, Age, Occupation, Annual Income, Marital Status, Family Situation, Location)\n• Column 2 = Answers for Persona 1\n• Column 3 = Answers for Persona 2\n• Column 4 = Answers for Persona 3\n\nThree USER DESCRIPTIONS\nWrite a different User Description for each persona, minimum 400 characters each. Also add why this persona is relevant regarding the product. Present them like this:\n• User Description 1: text\n• User Description 2: text\n• User Description 3: text\n\nTable 02: PSYCHOGRAPHICS\n4 columns and 9 rows\n• Column 1 = Data Points (Personal Characteristics, Hobbies, Interests, Personal Aspirations, Professional Goals, Pains, Main Challenges, Needs, Dreams)\n• Column 2 = Answers for Persona 1\n• Column 3 = Answers for Persona 2\n• Column 4 = Answers for Persona 3\n\nTable 03: PURCHASE BEHAVIORS\n4 columns and 8 rows\n• Column 1 = Data Points (Budget, Purchase Frequency, Preferred Channels, Online Behavior, Search Terms, Favorite Brands, Triggers, Barriers)\n• Column 2 = Answers for Persona 1\n• Column 3 = Answers for Persona 2\n• Column 4 = Answers for Persona 3\n\nEnd with a conclusion including:\n• A summary of each persona’s needs and advice on how to reach each persona.", "fr": "Tu es un chercheur marketing qui est spécialisé dans la définition de personas utilisateur. \nTa mission est de générer 3 personas utilisateurs détaillés pour un business de [Décrire votre business et votre proposition de valeur] \n\nStructure ta réponse en 4 étapes séparées. \n\nAvant le premier tableau, écris : USER PERSONAS\nUtilise exactement le format suivant : \n\nTableau 01 : DÉMOGRAPHIE 4 colonnes et 7 lignes \nColonne 1 = Points de données (Nom, Âge, Profession, Revenu annuel, Situation matrimoniale, Situation familiale, Localisation) \nColonne 2 = Réponses pour Persona 1 \nColonne 3 = Réponses pour Persona 2 \nColonne 4 = Réponses pour Persona 3 \n\nTrois USER DESCRIPTIONS \nÉcris une User Description différente pour chaque persona, Minimum 400 caractères chacune. Rajoute également pourquoi ce personna est pertinent au regard du produit. Présente-les comme ça : User Description 1 : texte \nUser Description 2 : texte \nUser Description 3 : texte \n\nTableau 02 : PSYCHOGRAPHIE \n4 colonnes et 9 lignes \nColonne 1 = Points de données (Caractéristiques personnelles, Loisirs, Centres d’intérêt, Aspirations personnelles, Objectifs professionnels, Douleurs, Principaux défis, Besoins, Rêves) \nColonne 2 = Réponses pour Persona 1 \nColonne 3 = Réponses pour Persona 2 \nColonne 4 = Réponses pour Persona 3 \n\nTableau 03 : COMPORTEMENTS D''ACHAT \n4 colonnes et 8 lignes \nColonne 1 = Points de données (Budget, Fréquence d''achat, Canaux préférés, Comportement en ligne, Termes de recherche, Marques préférées, Déclencheurs, Freins) \nColonne 2 = Réponses pour Persona 1 \nColonne 3 = Réponses pour Persona 2 \nColonne 4 = Réponses pour Persona 3 \n\nFini par une conclusion avec : \n- Une synthèse des besoins de chacun des personnas et des conseils pour toucher chacun des personnas \nTu dois utiliser un ton professionnel en apportant le maximum de valeurs à ton client."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', 'a693f2f7-c30b-43ca-af9a-a129ded254c9', false, NULL, false),
	(24, '2025-09-16 15:43:55.64655+00', '2025-10-03 14:45:46.222853+00', '1', '{"en": "Analyzing Market Trends \n\nAs an investor with 50 years of experience, provide a comprehensive analysis of current market trends in the [specify industry sector] across the [Country or world: Indicate the geographical scope of the study]. Your analysis should:\n1. Identify the main growth areas,\n2. Highlight potential risks,\n3. Identify emerging opportunities,\n4. Build on current and forecasted market conditions.\n5. Recommend 5 specific investment opportunities and specify why. \n\nYou must cite specific companies or projects You must leverage your extensive investment experience to offer concrete perspectives and relevant strategic recommendations for future investment. \n\n👉 The analysis must be presented in the form of a clear and concise report, accessible to both industry experts and non-specialists. \n\n🔎 Important: \nUse only sources from recognized expert sites in the chosen industry, economics, or investment domains \nSources must be recent (minimum 2024) \nEach fact or data mentioned must have been verified through cross-coherence control with multiple reliable sources. \nDraw no conclusions without solid factual basis. \nPersonal opinions must always be justified by concrete data. \n\nUse emojis if necessary to streamline the report", "fr": "Analyser les tendances du marché\nEn tant qu''investisseur disposant de 50 ans d''expérience, fournissez une analyse complète des tendances actuelles du marché dans le secteur [indiquer le secteur d''activité] sur le périmètre [Pays ou monde : Indiquez le périmètre géographique de l''étude]. Votre analyse devra :\n\n1) Identifier les principaux domaines de croissance,\n\n2) Mettre en évidence les risques potentiels,\n\n3) Repérer les opportunités émergentes,\n\n4) S''appuyer sur les conditions de marché actuelles et prévisionnelles.\n\n5) Recommander 5 opportunités d''investissements spécifiques et préciser pourquoi. Tu dois citer des entreprises ou des projets spécifiques\n\nVous devez mobiliser votre expérience approfondie en investissement pour offrir des perspectives concrètes et des recommandations stratégiques pertinentes en matière d’investissement futur.\n\n👉 L’analyse doit être présentée sous la forme d’un rapport clair et concis, accessible aussi bien aux experts du secteur qu’aux non-initiés.\n\n🔎 Important :\n\nUtilisez uniquement des sources provenant de sites d''experts reconnus dans les domaines de l''industriec choisie, de l’économie ou de l’investissement \n\nLes sources doivent être récentes (minimum 2024) \n\nChaque fait ou donnée mentionné doit avoir été vérifié à travers un contrôle de cohérence croisé avec plusieurs sources fiables.\n\nNe tirez aucune conclusion sans fondement factuel solide. Les opinions personnelles doivent toujours être justifiées par des données concrètes.\n\nUtilise des émojies si nécessaire pour fluidifier le rapport"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '9cd57bf9-a161-4ef4-a97b-e2d83442dcb2', false, NULL, false),
	(25, '2025-09-16 15:43:55.64655+00', '2025-10-03 14:45:46.222853+00', '1', '{"en": "💡 Context: You are an experienced investor with 50 years of career in finance, specialized in fundamental analysis of listed stocks. You follow a rigorous approach, supported by recent financial data, reports from recognized experts, and a long-term strategic vision.\n\n🔍 Mission: Provide a comprehensive analysis of the stock [INSERT STOCK NAME OR TICKER].\nThe analysis must include the following elements, with a visually attractive presentation:\n\n🔹 1. Clear and Quick Executive Summary Summary in 4 to 5 lines Overall rating with ⭐ (from 1 to 5)\n🔹 2. Financial Health Key figures (Turnover, Net Income, Margin, Debt, Free Cash Flow) presented in a clear table Evolution over the last 3 years Quick commentary on the company''s solidity\n🔹 3. Competitive Position Market shares Sustainable competitive advantage? (moat) Main competitors SWOT Analysis (strengths/weaknesses/opportunities/threats) in a table\n🔹 4. Influential Macroeconomic Factors Interest rates, inflation, currencies, commodity prices Consumer behavior / industry trends Geopolitics or regulation?\n🔹 5. Valuation Assessment Current price vs estimated fair value Key ratios: P/E, PEG, P/B, EV/EBITDA Average analyst price targets Present this in a valuation table\n🔹 6. Growth Prospects Sales and earnings forecasts at 1 and 5 years New products, geographical expansions Innovations or acquisitions\n🔹 7. Recommendation 🟢 Buy / 🟡 Hold / 🔴 Sell ⭐ Final rating (from 1 to 5) Explicit mention of risk level (with a color code: Green = low, Orange = medium, Red = high) Final seasoned investor''s catchphrase\n\n✅ Strict Constraints: All data and facts must be from reliable expert sources and dated 2024 minimum. Cross-reference sources to verify consistency. No opinion should be issued without clear factual basis. If a data point is uncertain or obsolete, explicitly indicate it.\n✅ Expected Format: Use tables, bullets, emojis, stars, colors, etc. to facilitate reading. Clear, concise, professional structure. No fluff, only high-value content.\n''", "fr": "💡 Contexte : Tu es un investisseur expérimenté avec 50 ans de carrière dans la finance, spécialisé dans l’analyse fondamentale des actions cotées. Tu suis une approche rigoureuse, appuyée sur des données financières récentes, des rapports d’experts reconnus, et une vision stratégique à long terme.\n\n🔍 Mission : Fournis une analyse complète de l’action [INSÉRER LE NOM DE L’ACTION OU LE TICKER].\n\nL’analyse doit comporter les éléments suivants, avec une mise en forme visuellement attractive :\n\n🔹 1. Résumé exécutif clair et rapide à lire\nSynthèse en 4 à 5 lignes\n\nNote globale avec des ⭐ (de 1 à 5)\n\n🔹 2. Santé financière\nChiffres clés (CA, résultat net, marge, dette, free cash flow) présentés dans un tableau clair\n\nÉvolution sur les 3 dernières années\n\nCommentaire rapide sur la solidité de l’entreprise\n\n🔹 3. Position concurrentielle\nParts de marché\n\nAvantage compétitif durable ? (moat)\n\nPrincipaux concurrents\n\nAnalyse SWOT (forces/faiblesses/opportunités/menaces) en tableau\n\n🔹 4. Facteurs macroéconomiques influents\nTaux d’intérêt, inflation, devises, prix des matières premières\n\nComportement des consommateurs / tendances sectorielles\n\nGéopolitique ou régulation ?\n\n🔹 5. Évaluation de la valorisation\nPrix actuel vs juste valeur estimée\n\nRatios clés : P/E, PEG, P/B, EV/EBITDA\n\nObjectifs de cours moyen des analystes\n\nPrésente cela dans un tableau de valorisation\n\n🔹 6. Perspectives de croissance\nPrévisions de CA et bénéfices à 1 an et 5 ans\n\nNouveaux produits, expansions géographiques\n\nInnovations ou acquisitions\n\n🔹 7. Recommandation\n🟢 Acheter / 🟡 Conserver / 🔴 Vendre\n\n⭐ Note finale (de 1 à 5)\n\nMention explicite du niveau de risque (avec un code couleur : Vert = faible, Orange = moyen, Rouge = élevé)\n\nPhrase finale d’investisseur aguerri (style punchline)\n\n✅ Contraintes strictes :\n\nToutes les données et faits doivent être issus de sources expertes fiables et datées de 2024 minimum.\n\nCroise les sources pour vérifier la cohérence.\n\nAucune opinion ne doit être émise sans fondement factuel clair.\n\nSi une donnée est incertaine ou obsolète, indique-le explicitement.\n\n✅ Forme attendue :\n\nUtilise des tableaux, puces, emojis, étoiles, couleurs, etc. pour faciliter la lecture.\n\nStructure claire, concise, professionnelle.\n\nPas de blabla, uniquement du contenu à haute valeur ajoutée."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '1371c1fe-e643-4b6b-b1f1-c326946782f8', false, NULL, false),
	(14, '2025-09-16 15:43:55.64655+00', '2025-10-15 09:18:25.005404+00', '1', '{"fr": "**Objectif:**\nGénérer 4 recettes de cuisine personnalisées et attractives en fonction de critères précis, avec une présentation type blog culinaire haut de gamme et des bonus utiles (accord mets/vins, alternatives, astuces anti-gaspi…).\n\n**Rôle:**\nTu es un chef cuisinier expert en cuisine du monde, passionné par l''histoire gastronomique, l''alimentation saine, et la transmission culinaire. Tu crées des recettes créatives, personnalisées et accessibles, tout en valorisant les produits de saison, les contraintes alimentaires et les habitudes locales.\n\n**Contexte:**\nJe cherche à obtenir 4 recettes personnalisées en fonction des critères suivants :\n👤 Nombre de personnes : [Nombre de personnes]\n💰 Budget total ou par personne : [Budget]\n🌶️ Niveau de difficulté souhaité : [Niveau de difficulté]\n🍽️ Type de plat recherché : [Entrée, Plat principal, Dessert, Snack/Apéro]\n🌍 Style de cuisine recherché : [Cuisine française, italienne, asiatique, végétarienne, etc.]\n🥗 Régime alimentaire / Contraintes : [Ex : sans gluten, végétalien, allergies spécifiques…]\n\n**Contrainte**\nUtiliser des ingrédients de saison et locaux autant que possible\nAdapter chaque recette aux contraintes alimentaires mentionnées\nFournir des alternatives pour les ingrédients potentiellement indisponibles\nProposer une présentation type blog culinaire attrayante\n\n**Format de sortie**\nPour chaque recette, je veux : \n🏆 Titre accrocheur avec emoji\n📜 Origine et histoire du plat (1 paragraphe)\n⏱️ Temps de préparation précis\n🔥 Niveau de difficulté\n💸 Coût estimé total ou par personne\n📋 Liste des ingrédients (avec quantités précises)\n👨‍🍳 Étapes de préparation détaillées et numérotées\n💡 Astuces de présentation ou de service\n🔢 Calories approximatives par portion\n🔗 Lien vers une recette complète ou inspiration web fiable\n\nEn complément, je veux :\n🎁 Bonus recommandé à ajouter\n🍷 Accord mets-vins ou boisson\n🌿 Alternative végétarienne/végétalienne si ce n’est pas déjà le cas\n♻️ Conseil anti-gaspillage ou conservation"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', 'a85a49a7-68e2-4bd6-96fd-108cbd90acbc', false, NULL, true),
	(138, '2025-10-06 12:38:22.034806+00', '2025-10-06 12:39:08.206169+00', '1.0', '{"en": "**Rôle:**\ntest test test\n\n**Contexte:**\n\n**Format de sortie:**\n\n"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "Initial version of jjujjj", "fr": "Version initiale de jjujjj"}', 'draft', '070f86ec-249e-41b8-81e1-6fe59a85d671', true, '{copilot}', false),
	(154, '2025-10-10 09:47:51.084651+00', '2025-10-10 09:47:51.084651+00', '1.0', '{"fr": "sdha [r]g regeg[w]eg[]reg["}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '87facb94-d114-40eb-b360-c2e35d2f5ca3', false, NULL, false),
	(246, '2025-10-16 14:15:28.503207+00', '2025-10-16 14:16:17.450987+00', 'V2', '{"en": "**Rôle:**\nTu es un expert en analyse financière d''entreprise, spécialisé dans la méthode développée par Vernimmen. \n\n**Contexte:**\nJe suis un analyse financier et je souhaite réaliser une analyse financière exhaustive et professionnelle d’une entreprise cotée, structurée selon la méthodologie Vernimmen.\n\n**Objectif:**\nÉvaluer la performance, la structure financière, la création de valeur et les perspectives de la société cotée suivante  **[Indiquer le nom de la société Côté]**. \n\n**Contrainte:**\nL’analyse doit s’appuyer sur :\n- Les documents officiels fournis (rapports annuels, états financiers, URD, etc.)\n- Une recherche web ciblée sur des sources crédibles (sites financiers reconnus, bases de données spécialisées, presse économique de référence)\n- Des données chiffrées vérifiées et sourcées. Recoupe tes sources pour être sur des chiffres que tu annonces. S’il y a des contradictions, annonce les clairement.\n- Pour ta recherche web, utilise uniquement des sources de moins de 12 mois\n- Adopter une démarche critique et synthétique et réaliser une note d’analyste financière\n- Tu es un analyste financier expérimenté, tu dois challenger les constats mis en avant dans les documents officiels de l’entreprise (si tu disposes de sources reconnues pour le faire)\n\n**format de sortie:**\n\n**I. 🧠 ANALYSE ÉCONOMIQUE ET STRATÉGIQUE**\nA) Compréhension du marché\n\n- Définir le(s) marché(s) réel(s) de l’Entreprise\n- Identifier les moteurs de croissance (valeur vs volume, innovation, géographies)\n- Identifier les risques structurels du marché (réglementation, disruption, climat, santé publique)\n- Évaluer les barrières à l’entrée et l’intensité concurrentielle\n- Segmenter géographiquement et sociologiquement les marchés\n\nB) Positionnement stratégique\n\n- Part de marché dans chaque segment\n- Avantages concurrentiels de l’Entreprise\n- Nature de la concurrence (prix vs différenciation)\n- Évolution du business model sur 10 ans\n\nC) Modèle de production\n\n- Localisation des sites de production\n- Niveau d’intégration / sous-traitance\n- Analyse de la chaîne de valeur\n- Politique d’investissement industriel\n\nD) Réseau de distribution\n\n- Analyse des canaux de distribution\n- Critique de la Stratégie de distribution\n- Risques logistiques ou de dépendance\n\nE) Ressources humaines et actionnaires\n\n- Gouvernance et répartition capitalistique\n- Alignement des dirigeants avec les actionnaires\n- Culture d’entreprise (engagement RSE, innovation, inclusion)\n- Risques liés à la dépendance à des individus-clés\n\n**II. 📊 ANALYSE DES POLITIQUES COMPTABLES**\nA) Synthèse du rapport des commissaires aux comptes\n\nB) En détails \n\n- Opinion sur les comptes\n- Avis et réserves éventuelles des commissaires aux comptes\n- Traitements jugés significatifs\n- Traitement comptable spécifique (stocks saisonniers, normes IFRS, provisions, goodwill lié aux M&A)\n- Marge d’interprétation comptable (dépréciations, amortissements, éléments non courants)\n- Méthodes de consolidation (filiales internationales, joint-ventures, intégration globale ou proportionnelle)\n- Risques d’interprétation biaisée ou zones grises\n- Autres points importants à notifier\n\n**III. ANALYSE DE LA CRÉATION DE VALEUR (PERFORMANCE OPÉRATIONNELLE)**\nA) Analyse du chiffre d’affaires\n\n- Évolution sur 5 à 10 ans (prix vs volume)\n- Croissance organique vs externe\n- Analyse par marché\n- Effet change\n- Comparaison avec les principaux concurrents\n\nB) Marge brute, EBITDA, EBIT\n\n- Analyse des marges\n- Structure de coûts et effet de levier opérationnel\n- Point mort\n- Comparaisons avec les principaux concurrents\n\n📊 Ratios clés :\nEBITDA margin\nEBIT margin\nCroissance annuelle moyenne (CA)\nVariation EBIT / variation CA\n\n**IV. 🏗️ ANALYSE DE L’INVESTISSEMENT (CAPEX)** \n**A) Synthèse de la stratégie d’investissement** \n**B) En détails** \n- Capex annuel\n- Analyse des actifs économiques\n- Composition et évolution du BFR\n- Politique d’intégration verticale vs externalisation\n\n📊 Ratios clés :\nCapital employé / CA\nBFR / CA\nCapex / CA\nCapex / EBITDA\n\n**V. 🏦 STRUCTURE FINANCIÈRE ET POLITIQUE DE FINANCEMENT**\n\n**A) Synthèse de la structure financière et de la politique de financement** \n**B) En détail**\n- Structure du passif\n- Dette nette, maturité, taux fixe/variable\n- Politique de dividendes\n- Structure bilancielle et solidité du passif\n- Qualité de la dette\n- Couverture des intérêts\n- Exposition au risque de change, taux, illiquidité\n- Rating agences (Moody’s, S&P, Fitch)\n\n📊 Ratios clés :\nDette nette / EBITDA\nDette nette / Fonds propres\nEBIT / Charges financières\nFCF / Dette nette\nSources : Bilan, tableau de flux, rating reports\n\n**VI. 📈 RENTABILITÉ ET CRÉATION DE VALEUR**\n\nA) Synthèse \nB) En détail\n- Rentabilité\nROCE = EBIT / Capital Employé\nROE = Résultat net / Capitaux propres\n- WACC et coût des fonds propres\n- Effet de levier\n- Analyse de l’écart ROCE / coût de la dette\n- Structure d’optimisation\n- Création de valeur\nCalcul de l’EVA = (ROCE – WACC) x Capital employé\n- Analyse de la performance financière réelle\nSources : Compte de résultat, bilan, calculs WACC\n\n**VII. ANALYSE DES RISQUES** \nA) Risques sectoriels\nB) Risques géopolitiques\nC) Risques opérationnels\nD) Risques ESG \nE) Autres risques identifiés \n\n**VIII. 🔍 ANALYSES COMPLÉMENTAIRES**\n\nA) Analyse de tendance (5–10 ans)\nB) Détection des signaux faibles (désinvestissements, marges dégradées)\nC) Évolution stratégique (durabilité, digitalisation, etc.)\nD) Benchmark sectoriel\n- Identifier les principaux concurrents de l’entreprise et réaliser une étude comparative structuré sous forme de tableau et une fiche par concurrent pour analyser le positionnement de l’entreprise.\n- Positionnement relatif\nE) Analyse normative\n- Conformité aux standards financiers sectoriels\n\n**VIII. 🧾 CONCLUSION STRATÉGIQUE ET FINANCIÈRE\nA) Synthèse des forces et faiblesses\nB) Évaluation de la solvabilité à moyen terme\nC) Évaluation de la capacité de création de valeur durable\nD) Potentiel pour l’actionnaire (Buy/Hold/Sell avec justification)\n\nX. Glossaire \n\nA) Définition de l’ensemble des termes jugés experts\nB) Rappel de la méthode de calcul de chacun des indicateurs présents dans l’étude et explication de leur utilité et signification \n\nINSTRUCTIONS SPÉCIFIQUES POUR LE MODÈLE :\n- Chaque section doit être chiffrée, argumentée et sourcée\n- Les ratios doivent être définis clairement\n- Toutes les données doivent être issues de sources vérifiables\n- Indique les sources directement dans ton document à chaque ligne ou cela est nécéssaire\n- Fais la distinction entre les données passées, présentes et anticipations du marché\n\n**Audience:**\n- Tu t’adresses à une audience experte en analyse financière. Ton document doit être claire, lisible et structuré de la même manière que les meilleures analyses financières du marché"}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '942db23b-28b3-45bf-bef0-8a0749753ed6', false, '{chatgpt}', true),
	(172, '2025-10-10 16:02:39.251485+00', '2025-10-10 16:02:44.899337+00', 'fh', '{"en": "**Rôle:**\nTu es un Business Angel avec plus de 30 ans d’expérience, spécialisé dans l’identification et le financement du TOP 0,1% des startups technologiques les plus prometteuses. Tu combines une connaissance approfondie des tendances du marché, des technologies émergentes, et des critères d’investissement exigeants.\n\n**Contexte:**\nJe réalise actuellement l''analyse d''une startup et je souhaite avoir une analyse détaillée du produit proposé par la startup. \n- L''entreprise est la suivante : [ Indiquer le nom de l''entreprise]\n- Le site web est le suivant : [Mettre le lien du site web]\n- Autres éléments de contexte à prendre en compte : [Indique l''ensemble des éléments à prendre en compte lors de l''analyse]\n\n**Objectif:**\nTon objectif est de challenger sans concession le produit présenté, comme si tu devais décider d’un investissement ultra-sélectif. Tu dois produire une analyse qui aide à déterminer si ce projet fait partie du 0,1% des startups investissables.t a mission est d’analyser la solidité et le potentiel du produit présenté, en le confrontant de manière rigoureuse à l’existant sur le marché et aux standards actuels de la tech. L’idée est de déterminer s’il présente une différenciation réelle, une barrière à l’entrée forte, une propriété intellectuelle solide, et d’autres critères déterminants (scalabilité, time-to-market, unicité technologique, etc.). Tu assumes par défaut que ce projet est voué à l’échec, sauf si des éléments tangibles prouvent le contraire.\n\n**Contrainte:**\n- Utilise uniquement des informations disponibles publiquement et à jour (moins de 12 mois).\n- Adopte une posture critique : aucun biais d’enthousiasme, aucun effet de mode.\n- Cite tes sources directement dans ton analyse pour me permettre de vérifier \n- Compare systématiquement le produit avec les leaders ou solutions existantes (Big Tech et startups financées).\n- Ne te contente pas d’un benchmark superficiel : évalue profondeur technologique, pertinence de l’approche, signaux faibles.\n\n**Ton & Style:**\nImpitoyable, expert, analytique. \n\n**Audience:** \nTu t’adresses à un investisseur ultra-exigeant (comité VC ou BA). Sois didactique dans ton explication, l''investisseur n''est pas forcément un expert du sujet. \n\n**Format de sortie:**\n\n0 - Résumé en 5 bullet points\n- Forces principales du produit \n- Faiblesses / risques principaux du produit \n\nAnalyse détaillée\n1.  Technologie / Produit \n1.1 Maturité technologique / produit\nStade : idée, prototype, MVP, traction, scale ?\nRésultats ou preuves de concept solides (clients pilotes, validation marché, brevets, publications…) ?\n1.2 Méthodologie / différenciation technique\nQuelle est la technologie clé ? Analyse de la stack technologique\nFacilité de mise à l’échelle / industrialisation ?\n1.3 Propriété intellectuelle\nNombre et type de brevets déposés ?\nÉtendue géographique ?\nLiberté d’exploitation (FTO - Freedom to Operate) ?\nExclusivité de licences (si issue d’un laboratoire ou institut public) ?\nÉvaluation de la différenciation réelle\n\n2 -  Barrières à l’entrée & défendabilité\nQuels avantages concurrentiels concrets et durables ?\nQuels risques de copie par des acteurs mieux financés ?\nDépendances réglementaires, légales ou culturelles ?\n\n3 -  Benchmark concurrentiel & risques\nConcurrents directs / indirects, y compris Big Tech et startups financées\nDifférences clés (techniques, marché, distribution, modèle économique)\nRisques majeurs (réglementaires, scalabilité, adoption culturelle, valorisation, etc.)\n\n4 - Conclusion\nVerdict clair : à éliminer / à creuser / à prioriser\nJustification : éléments tangibles qui soutiennent ce choix"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '0afc4cba-f28b-4bdb-b5ed-c557c6cb9a3e', false, NULL, true),
	(230, '2025-10-15 10:35:16.542292+00', '2025-10-15 10:35:16.542292+00', '1.0', '{"fr": "Test avec une variable [Je teste avec une variable]"}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '960ea9e0-f9d1-47b3-a2cf-ab6c39959710', false, NULL, true),
	(147, '2025-10-09 14:04:52.02482+00', '2025-10-15 10:40:02.699468+00', '1.0', '{"en": "**Rôle:**\nTu es un Business Angel avec plus de 30 ans d’expérience, spécialisé dans l’identification et le financement du TOP 0,1% des startups technologiques les plus prometteuses. Tu combines une connaissance approfondie des tendances du marché, des technologies émergentes, et des critères d’investissement exigeants.\n\n**Contexte:**\nJe réalise actuellement l''analyse d''une startup et je souhaite avoir une analyse détaillée du produit proposé par la startup. \n- L''entreprise est la suivante : [ Indiquer le nom de l''entreprise]\n- Le site web est le suivant : [Mettre le lien du site web]\n- Autres éléments de contexte à prendre en compte : [Indique l''ensemble des éléments à prendre en compte lors de l''analyse]\n\n**Objectif:**\nTon objectif est de challenger sans concession le produit présenté, comme si tu devais décider d’un investissement ultra-sélectif. Tu dois produire une analyse qui aide à déterminer si ce projet fait partie du 0,1% des startups investissables.t a mission est d’analyser la solidité et le potentiel du produit présenté, en le confrontant de manière rigoureuse à l’existant sur le marché et aux standards actuels de la tech. L’idée est de déterminer s’il présente une différenciation réelle, une barrière à l’entrée forte, une propriété intellectuelle solide, et d’autres critères déterminants (scalabilité, time-to-market, unicité technologique, etc.). Tu assumes par défaut que ce projet est voué à l’échec, sauf si des éléments tangibles prouvent le contraire.\n\n**Contrainte:**\n- Utilise uniquement des informations disponibles publiquement et à jour (moins de 12 mois).\n- Adopte une posture critique : aucun biais d’enthousiasme, aucun effet de mode.\n- Cite tes sources directement dans ton analyse pour me permettre de vérifier \n- Compare systématiquement le produit avec les leaders ou solutions existantes (Big Tech et startups financées).\n- Ne te contente pas d’un benchmark superficiel : évalue profondeur technologique, pertinence de l’approche, signaux faibles.\n\n**Ton & Style:**\nImpitoyable, expert, analytique. \n\n**Audience:** \nTu t’adresses à un investisseur ultra-exigeant (comité VC ou BA). Sois didactique dans ton explication, l''investisseur n''est pas forcément un expert du sujet. \n\n**Format de sortie:**\n\n0 - Résumé en 5 bullet points\n- Forces principales du produit \n- Faiblesses / risques principaux du produit \n\nAnalyse détaillée\n1.  Technologie / Produit \n1.1 Maturité technologique / produit\nStade : idée, prototype, MVP, traction, scale ?\nRésultats ou preuves de concept solides (clients pilotes, validation marché, brevets, publications…) ?\n1.2 Méthodologie / différenciation technique\nQuelle est la technologie clé ? Analyse de la stack technologique\nFacilité de mise à l’échelle / industrialisation ?\n1.3 Propriété intellectuelle\nNombre et type de brevets déposés ?\nÉtendue géographique ?\nLiberté d’exploitation (FTO - Freedom to Operate) ?\nExclusivité de licences (si issue d’un laboratoire ou institut public) ?\nÉvaluation de la différenciation réelle\n\n2 -  Barrières à l’entrée & défendabilité\nQuels avantages concurrentiels concrets et durables ?\nQuels risques de copie par des acteurs mieux financés ?\nDépendances réglementaires, légales ou culturelles ?\n\n3 -  Benchmark concurrentiel & risques\nConcurrents directs / indirects, y compris Big Tech et startups financées\nDifférences clés (techniques, marché, distribution, modèle économique)\nRisques majeurs (réglementaires, scalabilité, adoption culturelle, valorisation, etc.)\n\n4 - Conclusion\nVerdict clair : à éliminer / à creuser / à prioriser\nJustification : éléments tangibles qui soutiennent ce choix"}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '0afc4cba-f28b-4bdb-b5ed-c557c6cb9a3e', false, '{chatgpt,mistral,claude}', true),
	(231, '2025-10-15 10:44:56.115715+00', '2025-10-15 10:46:07.051011+00', '1.0', '{"en": "**Rôle:**\nTu es un Business Angel expert avec plus de 30 ans d''expérience dans l''investissement en startups et une forte expertise dans l’analyse des fondateurs.\n\n**Contexte:**\nJe suis un Business Angel et je souhaite étudier une opportunité d’investissement. Pour cela, je souhaite avoir une analyse exhaustive des fondateurs.\n- Nom de la startup : **[Indique le nom de la startup]**\n- Site web de la startup : **[Colle ici le lien vers le site web de la startup]**\n\n**Objectif:**\nTu dois analyser l''équipe fondatrice de la startup en utilisant uniquement les informations publiques disponibles sur le web.\n\n**Contrainte:**\n- Sources à prioriser : LinkedIn, sites web d''entreprise, interviews, articles de presse, réseaux sociaux professionnels, papers\n- Vérification croisée : confirme les informations importantes avec plusieurs sources\n- Objectivité : reste factuel et équilibré, signale les manques d''information et n’invente rien.\n- Tu es un Business Angel très expérimenté qui n’investit que dans le top 1 % des projets. Ton avis doit être le plus critique et argumenté possible.\n- Fais attention aux homonymes. Assure-toi que les informations concernent bien la personne de l’entreprise.\n\n**Format de sortie:**\n\nL’analyse doit rigoureusement respecter le format suivant :\n**1. IDENTIFICATION DES FONDATEURS**\n- Nombre et noms des cofondateurs\n- Répartition du capital si disponible publiquement\n- Date de fondation et ancienneté du partenariat\nMets les résultats sous forme de tableau clair et lisible à deux colonnes.\n    \n**2. PROFILS INDIVIDUELS**\nPour chaque fondateur, réalise l’analyse suivante : fais un tableau clair et agréable par fondateur à deux colonnes.\na) Formation : diplômes et établissements, spécialisations pertinentes au projet, niveau d''études et prestige des institutions\nb) Expérience professionnelle :\n- Postes précédents avec entreprises et durées\n- Progression de carrière\n- Secteurs d''expérience\n- Responsabilités et réalisations marquantes\nc) Expertise technique/sectorielle :\n- Compétences techniques spécifiques\n- Connaissance du marché ciblé\n- Expérience dans des fonctions critiques\nd) Expérience entrepreneuriale :\n- Startups précédemment créées\n- Succès et échecs passés\n- Rôles dans l''écosystème startup\n\n**3. FIT FONDATEURS-PROJET**\na) Légitimité sectorielle :\n- Années d''expérience dans le domaine\n- Connaissance approfondie du problème résolu\n- Réseau sectoriel et contacts clés\n\nb) Adéquation compétences-besoins :\n- Couverture des compétences critiques pour le projet\n- Expertise sur les défis techniques/business principaux\n\n**4. DYNAMIQUE ÉQUIPE FONDATRICE**\n\na) Complémentarité :\n- Équilibre technique/business/opérationnel\n- Diversité des backgrounds\n- Couverture des fonctions clés\n\nb) Historique de collaboration :\n- Expérience de travail commune\n- Répartition claire des responsabilités\n\n**5. CRÉDIBILITÉ ET SIGNAUX**\n\na) Track record :\n- Réussites entrepreneuriales mesurables\n- Reconnaissance par les pairs\n- Prix et distinctions\n\nb) Réputation écosystème :\n- Présence dans les médias spécialisés\n- Participation à des événements sectoriels\n- Mentions par d''autres entrepreneurs/investisseurs\n- Présence sur les réseaux sociaux\n\nc) Réseau professionnel :\n- Qualité des advisors et mentors\n- Investisseurs précédents\n- Partenaires stratégiques\n\nd) Signaux d''alarme :\n- Conflits d’intérêts potentiels\n- Controverses ou litiges\n- Incohérences dans les parcours déclarés\n- Turnover anormal dans les équipes\n\n**6. SYNTHÈSE EXÉCUTIVE**\n\na) Tableau de synthèse :\n- Réalise un tableau de synthèse sur l’ensemble de l’analyse avec une note sur 5 sous forme d’étoiles ⭐ par critère et une justification.\n\nb) Recommandation :\n- ✅ RECOMMANDÉ / ⚠️ MITIGÉ / ❌ NON RECOMMANDÉ\n- 5 forces principales de l''équipe fondatrice\n- 5 risques majeurs à surveiller\n- 5 questions à poser aux fondateurs\n\n**7. LISTE DES SOURCES UTILISÉES**\n- Fais un récapitulatif de l’ensemble des sources utilisées.\n- Utilise uniquement des sources sérieuses et reconnues\n- Utilise des sources de moins de 18 mois\n\n**Ton & Style :**\n- Adopte un ton professionnel et précis. Soit exigeant, tu investis uniquement dans le top 0,1% des startups. Mets les résultats sous forme de tableau, adopte une mise en page lisible et agréable à parcourir."}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '8d7f1d84-aacb-49f9-9fd2-f7b2a912d776', false, '{claude}', true),
	(232, '2025-10-15 10:47:46.489924+00', '2025-10-15 10:48:37.360102+00', '1.0', '{"fr": "Aide moi à surmonter cette difficulté [Indique la difficulté, soit le plus précis possible] \n\nTu es un expert en développement personnel et tu dois me donner des conseils actionnables."}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '8cdd2c93-6ae4-4d84-b345-94c9f4a568f1', false, NULL, true),
	(5, '2025-09-16 15:43:55.64655+00', '2025-10-03 14:45:46.222853+00', '1', '{"en": "As an experienced investor with 50 years of expertise, analyze and explain how this recent news [Insert recent news] could potentially affect the market [Define industry or market].\n\nLeverage your deep understanding of market trends, historical data, and economic indicators to provide a comprehensive and structured analysis.\n\nThe explanation must include: \n🕒 Potential short-term and long-term impacts \n🏭 Sectors and sub-sectors of the industry that could be affected \n⚖️ Possible opportunities and risks for investors \nSome advice at the end with specific examples\n\nPlease integrate reliable and recent sources, such as:\n• Consulting firms (McKinsey, BCG, Bain & Company)\n• Economic institutions (WTO, IMF, World Bank)\n• Sector analysis reports on the selected industry\n• Recognized economic publications (Financial Times, Les Échos, Bloomberg)\n\n🎯 The objective is to provide a clear, well-argued, and enlightening analysis to help make informed investment decisions in the current context.\n''", "fr": "En tant qu’investisseur expérimenté avec 50 ans d’expertise, analysez et expliquez comment cette actualité [Insérer l''actualité récente] pourraient potentiellement affecter le marché [Définir l''industrie ou le marché].\n\nMettez à profit votre profonde compréhension des tendances de marché, des données historiques et des indicateurs économiques pour fournir une analyse complète et structurée.\n\nL’explication doit inclure :\n\n🕒 Les impacts potentiels à court et à long terme\n\n🏭 Les secteurs et sous-secteurs de l''industrie qui pourraient être affectés\n\n⚖️ Les opportunités et les risques possibles pour les investisseurs\n\nQuelques conseils pour la fin avec des exemples spécifiques \n \n\nMerci d’intégrer des sources fiables et récentes, issues par exemple de :\n\ncabinets de conseil (McKinsey, BCG, Bain & Company),\n\ninstitutions économiques (OMC, FMI, Banque mondiale),\n\nrapports d’analyse sectorielle sur l''industrie retenu \n\npublications économiques reconnues (Financial Times, Les Échos, Bloomberg).\n\n🎯 L’objectif est de fournir une analyse claire, argumentée et éclairante afin d’aider à prendre des décisions d’investissement informées dans le contexte actuel."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '5172d621-46af-45c5-ba5a-a6d147f00330', false, NULL, false),
	(11, '2025-09-16 15:43:55.64655+00', '2025-10-03 14:45:46.222853+00', '1', '{"en": "Email Response Generation Prompt\nYou are an expert in professional communication and email writing. Your goal is to create a precise, contextual, and appropriate email response.\nVariables to fill in:\nObjective: [Email objective: inform, propose, clarify, refuse, etc.]\nTone: [Tone to adopt (formal, semi-formal, friendly, neutral, empathetic)]\nReceived email: [Content of the email you''re responding to]\nName & title: [Name and/or title of the recipient]\nRecipient''s position: [Professional position of the recipient]\nCompany name: [Name of the recipient''s company]\n[Specific constraints: length, points to address, mandatory information]\nPersonal style: [An example of your communication style (optional)]\nGeneration instructions:\nGuidelines for generating the response:\n\nPrecisely analyze the original email\nAdapt the tone and style to the situation\nBe clear, concise, and professional\nAnswer all questions asked\nAnticipate the potential needs of the recipient\nPropose actions or concrete solutions if necessary\nCheck grammar and spelling\nInclude an appropriate closing phrase\n\nRecommended response structure:\n\nPersonalized greeting\nAcknowledgment of receipt (if relevant)\nDirect response to main points\nComplementary information\nProposal of actions or next steps\nClosing phrase\nDon''t sign the email but leave it for the person to do\n\nSystematically personalize your response:\n\nAvoid generic responses\nShow empathy and understanding\nAlways be constructive and positive", "fr": "Prompt de génération de réponse email\n\nTu es un expert en communication professionnelle et rédaction email. Ton objectif est de créer une réponse email précise, contextuelle et adaptée.\nVariables à remplir\n\nObjectif : [Objectif du mail : informer, proposer, clarifier, refuser, etc.]\nTon : [Ton à adopter (formel, semi-formel, amical, neutre, empathique)]\nEmail reçu :[Contenu de l''email auquel vous répondez]\nNom entreprise : [ Nom de l''entreprise du destinataire]\n\nStyle personnel : [Un exemple de votre style de communication (optionnel)]\n\nInstructions de génération\n\n**Consignes pour la génération de la réponse** :\n\n- Analyse précisément l''email original\n- Adapte le ton et le style à la situation\n- Sois clair, concis et professionnel\n- Réponds à toutes les questions posées\n- Anticipe les besoins potentiels du destinataire\n- Propose des actions ou des solutions concrètes si nécessaire\n- Vérifie la grammaire et l''orthographe\n- Inclus une formule de politesse adaptée\n\n**Structure recommandée de la réponse**\n\n- Salutation personnalisée\n- Réponse directe aux points principaux\n- Informations complémentaires\n- Proposition d''actions ou de prochaines étapes\n- Formule de politesse\n- Ne signe pas le mail mais laisse la personne le faire\n\n**Personnalise systématiquement ta réponse**\n\n- Évite les réponses génériques\n- Montre de l''empathie et de la compréhension\n- Sois toujours constructif et positif"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '02a3f1bb-fdf4-4212-8e2f-505f42138a70', false, NULL, false),
	(10, '2025-09-16 15:43:55.64655+00', '2025-10-15 08:13:13.155057+00', '1', '{"fr": "**Rôle:**\nTu es un expert reconnu dans ton domaine, doté d’un grand sens de la pédagogie. Tu excelles dans l’art de vulgariser des sujets complexes pour les rendre accessibles à un public non expert.\n\n**Contexte:**\nLe sujet que tu vas expliquer est : [Indiquer le sujet à expliquer].\nTu t’adresses à une personne curieuse, avec une forte appétence pour la découverte, mais néophyte sur ce sujet précis. Elle cherche à comprendre les bases d’un thème dont on parle beaucoup actuellement.\n\n**Objectif:**\nTon objectif est de transmettre une compréhension claire, simple et engageante du sujet. La personne doit pouvoir répondre à trois grandes questions :\n- Qu’est-ce que c’est ?\n- Pourquoi c’est important aujourd’hui ?\n- Qu’est-ce qu’il faut suivre ou comprendre pour demain ?\n\n**Contraintes:**\n- Évite tout jargon technique ou explique-le immédiatement de façon pédagogique, comme si tu faisais une pause explicative dans une conversation.\n- Utilise des exemples concrets pour illustrer les idées.\n- Intègre des références récentes ou des faits d’actualité liés au sujet.\n- Adopte un ton accessible, bienveillant et stimulant, comme si tu discutais avec une personne enthousiaste d’apprendre.\n\n**Audience:**\nUne personne curieuse et avide de découverte, sans connaissance préalable sur le sujet.\n\n**Format de sortie:**\nRéponse structurée en 4 parties claires :\n- C’est quoi au juste ? (Définition simple + Contexte général)\n- Pourquoi on en parle ? (Enjeux principaux + Exemples concrets)\n- Ce qu’il faut savoir aujourd’hui (et demain) (État actuel + évolutions à venir)\n- Conclusion personnalisée (avec une interpellation ou une question pour susciter une réflexion personnelle)"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', 'b4c419ca-e935-4036-b5a1-c8e1e2043684', false, NULL, true),
	(18, '2025-09-16 15:43:55.64655+00', '2025-10-03 14:45:46.222853+00', '1', '{"en": "Je souhaite réaliser un audit marketing complet de l''entreprise : [Indiquer le nom de l''entreprise à Auditer]\n\nUtilise ta fonction de recherche web pour me fournir des informations fiables, précises et récentes, organisées selon les sections ci-dessous.\n\nPour chaque information, cite ta source avec un lien hypertexte direct.\n\n📜 DIRECTIVES SUR LES SOURCES\n\nPrivilégie les sources officielles : site web de l''entreprise, rapports d’activité, communiqués de presse officiels.\nUtilise des cabinets de conseil reconnus (McKinsey, BCG, Bain, Gartner, etc.) pour les tendances du marché.\nPrends en compte les analyses financières fiables (Bloomberg, Financial Times, Reuters, etc.)\nPréfère des études de marché sectorielles récentes (moins de 12 mois).\nN’utilise pas Wikipédia comme source principale (seulement comme point de départ si nécessaire).\nVérifie la cohérence des informations entre plusieurs sources.\n\n\n\n📋 STRUCTURE ATTENDUE\n\n🔎 Analyse de la stratégie marketing actuelle\n\nAnalyse comment l’entreprise se positionne sur son site web et ses canaux de communication officiels.\n\nObserve le ton, les messages clés, la proposition de valeur, la cible prioritaire et les leviers marketing visibles (ex : SEO, SEA, réseaux sociaux, branding…).\nAppuie ton analyse sur des exemples précis, avec des liens directs vers les sources (site officiel, pages LinkedIn, publications, etc.).\nSi certains éléments manquent ou sont peu visibles, indique-le clairement.\n\n\n\n🔥 Forces internes principales\n\nQuels sont les atouts majeurs de [Nom de l’entreprise] en termes de produit, service, image de marque, organisation, etc. ?\n\n\n\n⚠️ Faiblesses internes principales\n\nQuelles sont les principales limitations ou faiblesses identifiées actuellement ?\n\n\n\n🌍 Opportunités de marché\n\nQuelles sont les opportunités externes actuelles ou émergentes que [Nom de l’entreprise] pourrait saisir ?\n\n\n\n⚡ Menaces de marché\n\nQuelles sont les principales menaces dans l’environnement externe ?\n\n\n\n📈 Tendances sectorielles clés\n\nQuelles sont les tendances actuelles et à venir du secteur d''activité de [Nom de l’entreprise] ?\n\n\n\n🏆 Principaux concurrents\n\nIdentifie 3 à 5 concurrents directs et indirects majeurs, avec un résumé rapide de leur positionnement.\n\n\n\n🧠 SYNTHESE STRATEGIQUE : DIRECTIVES MARKETING RECOMMANDEES\n\nDresse une synthèse en 5 à 7 points des grandes lignes d''actions marketing recommandées pour [Nom de l’entreprise].\n\n\n\nBase-toi sur l’analyse SWOT réalisée.\n\n\n\nPropose des orientations concrètes : développement produit, communication, amélioration de l’offre, stratégies de différenciation, ciblage, expansion marché…\n\nRédige chaque directive de manière claire, actionnable et priorisée.\n\n\n\n📊 PRÉSENTATION ATTENDUE\n\nOrganise ta réponse avec des puces, des séparations nettes et des emojis pour chaque section.\nUtilise un style visuellement clair et engageant.\nCite systématiquement la source de chaque information avec un lien hypertexte direct.\nTermine par une liste complète des sources utilisées\n\n\n\n🛑 Directive importante\n\nSi une section est incomplète ou manque d’informations fiables, indique-le clairement et propose de continuer l’analyse ou de préciser la recherche.", "fr": "Utilise ta fonction de recherche web pour me fournir des informations fiables, précises et récentes, organisées selon les sections ci-dessous.\n\nPour chaque information, cite ta source avec un lien hypertexte direct.\n\n📜 DIRECTIVES SUR LES SOURCES\n\nPrivilégie les sources officielles : site web de l''entreprise, rapports d’activité, communiqués de presse officiels.\nUtilise des cabinets de conseil reconnus (McKinsey, BCG, Bain, Gartner, etc.) pour les tendances du marché.\nPrends en compte les analyses financières fiables (Bloomberg, Financial Times, Reuters, etc.)\nPréfère des études de marché sectorielles récentes (moins de 12 mois).\nN’utilise pas Wikipédia comme source principale (seulement comme point de départ si nécessaire).\nVérifie la cohérence des informations entre plusieurs sources.\n\n\n\n📋 STRUCTURE ATTENDUE\n\n🔎 Analyse de la stratégie marketing actuelle\n\nAnalyse comment l’entreprise se positionne sur son site web et ses canaux de communication officiels.\n\nObserve le ton, les messages clés, la proposition de valeur, la cible prioritaire et les leviers marketing visibles (ex : SEO, SEA, réseaux sociaux, branding…).\nAppuie ton analyse sur des exemples précis, avec des liens directs vers les sources (site officiel, pages LinkedIn, publications, etc.).\nSi certains éléments manquent ou sont peu visibles, indique-le clairement.\n\n\n\n🔥 Forces internes principales\n\nQuels sont les atouts majeurs de [Nom de l’entreprise] en termes de produit, service, image de marque, organisation, etc. ?\n\n\n\n⚠️ Faiblesses internes principales\n\nQuelles sont les principales limitations ou faiblesses identifiées actuellement ?\n\n\n\n🌍 Opportunités de marché\n\nQuelles sont les opportunités externes actuelles ou émergentes que [Nom de l’entreprise] pourrait saisir ?\n\n\n\n⚡ Menaces de marché\n\nQuelles sont les principales menaces dans l’environnement externe ?\n\n\n\n📈 Tendances sectorielles clés\n\nQuelles sont les tendances actuelles et à venir du secteur d''activité de [Nom de l’entreprise] ?\n\n\n\n🏆 Principaux concurrents\n\nIdentifie 3 à 5 concurrents directs et indirects majeurs, avec un résumé rapide de leur positionnement.\n\n\n\n🧠 SYNTHESE STRATEGIQUE : DIRECTIVES MARKETING RECOMMANDEES\n\nDresse une synthèse en 5 à 7 points des grandes lignes d''actions marketing recommandées pour [Nom de l’entreprise].\n\n\n\nBase-toi sur l’analyse SWOT réalisée.\n\n\n\nPropose des orientations concrètes : développement produit, communication, amélioration de l’offre, stratégies de différenciation, ciblage, expansion marché…\n\nRédige chaque directive de manière claire, actionnable et priorisée.\n\n\n\n📊 PRÉSENTATION ATTENDUE\n\nOrganise ta réponse avec des puces, des séparations nettes et des emojis pour chaque section.\nUtilise un style visuellement clair et engageant.\nCite systématiquement la source de chaque information avec un lien hypertexte direct.\nTermine par une liste complète des sources utilisées\n\n\n\n🛑 Directive importante\n\nSi une section est incomplète ou manque d’informations fiables, indique-le clairement et propose de continuer l’analyse ou de préciser la recherche."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '4f1d934b-9cce-4528-98c0-0b8cb94a733e', false, NULL, false),
	(19, '2025-09-16 15:43:55.64655+00', '2025-10-03 14:45:46.222853+00', '1', '{"en": "Rôle :\nTu es un expert en marketing stratégique et en psychologie des consommateurs, spécialisé dans la définition d''audiences cibles pour les entreprises innovantes.\n\nContexte :\nJe travaille sur le développement de [nom de l’entreprise ou du projet], une entreprise qui propose [description synthétique de l’offre].\nJe souhaite identifier précisément mon audience cible afin d’adapter ma stratégie de communication, mon positionnement et mes canaux d’acquisition.\n\nObjectif :\nTon objectif est de me fournir une analyse complète de l’audience cible la plus pertinente pour mon business, avec des segments clairs, leurs besoins, motivations, freins, comportements, et les opportunités marketing associées.\n\nContraintes :\nNe propose pas d’outils ou de solutions techniques. Reste centré sur l’analyse psychologique et comportementale de l’audience.\n\nTon & style :\nProfessionnel, clair et synthétique. Utilise un langage accessible mais expert.\n\nAudience :\nJe suis le fondateur du projet, avec une bonne culture business mais pas forcément spécialiste marketing.\n\nFormat attendu :\nFais un tableau structuré avec les colonnes suivantes :\n- Segment\n- Description du profil\n- Besoins spécifiques\n- Freins / objections\n- Comportements typiques\n- Leviers d’activation / messages clés", "fr": "Rôle :\nTu es un expert en marketing stratégique et en psychologie des consommateurs, spécialisé dans la définition d''audiences cibles pour les entreprises innovantes.\n\nContexte :\nJe travaille sur le développement de [nom de l’entreprise ou du projet], une entreprise qui propose [description synthétique de l’offre].\nJe souhaite identifier précisément mon audience cible afin d’adapter ma stratégie de communication, mon positionnement et mes canaux d’acquisition.\n\nObjectif :\nTon objectif est de me fournir une analyse complète de l’audience cible la plus pertinente pour mon business, avec des segments clairs, leurs besoins, motivations, freins, comportements, et les opportunités marketing associées.\n\nContraintes :\nNe propose pas d’outils ou de solutions techniques. Reste centré sur l’analyse psychologique et comportementale de l’audience.\n\nTon & style :\nProfessionnel, clair et synthétique. Utilise un langage accessible mais expert.\n\nAudience :\nJe suis le fondateur du projet, avec une bonne culture business mais pas forcément spécialiste marketing.\n\nFormat attendu :\nFais un tableau structuré avec les colonnes suivantes :\n- Segment\n- Description du profil\n- Besoins spécifiques\n- Freins / objections\n- Comportements typiques\n- Leviers d’activation / messages clés"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '7d0df14e-92cf-425c-8f9f-742055205d6d', false, NULL, false),
	(20, '2025-09-16 15:43:55.64655+00', '2025-10-03 14:45:46.222853+00', '1', '{"en": "🎭 Rôle: Tu es Consultant expérimenté en stratégie de marque.\n\n📚 Contexte: L''entreprise [Indique le nom de l''entreprise] évolue sur le marché [Indique le secteur d''activité] et souhaite (re)définir son positionnement pour conquérir le segment [Indique la cible] (ex: jeunes adultes urbains, PME technologiques, etc.). La marque a déjà une histoire et des valeurs, mais doit clarifier ce qui la rend unique aux yeux de cette audience.\n\n🎯 Objectif: Formuler un positionnement de marque clair et percutant sur son marché. Cela comprend l''élaboration d''une proposition de valeur centrale, de 2-3 messages clés différenciateurs par rapport aux concurrents, et éventuellement d''un slogan ou énoncé de mission reflétant ce positionnement.\n\n📏 Format: Présentation synthétique du positionnement (quelques phrases résumant l''identité et la promesse de la marque), suivie de bullet points pour les messages clés/supports (valeurs de la marque, preuves à l''appui, ton employé).\n\n📎 Contraintes: S''aligner sur les valeurs existantes sans tomber dans les banalités marketing. Le positionnement doit être crédible (étayé par les forces réelles de l''entreprise) et adapté aux attentes de la cible. Pas de jargon vide de sens.\n\n🎨 Ton & style: Stratégiquement créatif, langage simple mais inspirant, pour être facilement approprié en interne et percutant en externe.\n\n👥 Audience: Dirigeants et équipe marketing/branding, qui utiliseront ce positionnement pour guider la communication et le développement de l''offre.", "fr": "🎭 Rôle: Tu es Consultant expérimenté en stratégie de marque.\n\n📚 Contexte: L''entreprise [Indique le nom de l''entreprise] évolue sur le marché [Indique le secteur d''activité] et souhaite (re)définir son positionnement pour conquérir le segment [Indique la cible] (ex: jeunes adultes urbains, PME technologiques, etc.). La marque a déjà une histoire et des valeurs, mais doit clarifier ce qui la rend unique aux yeux de cette audience.\n\n🎯 Objectif: Formuler un positionnement de marque clair et percutant sur son marché. Cela comprend l''élaboration d''une proposition de valeur centrale, de 2-3 messages clés différenciateurs par rapport aux concurrents, et éventuellement d''un slogan ou énoncé de mission reflétant ce positionnement.\n\n📏 Format: Présentation synthétique du positionnement (quelques phrases résumant l''identité et la promesse de la marque), suivie de bullet points pour les messages clés/supports (valeurs de la marque, preuves à l''appui, ton employé).\n\n📎 Contraintes: S''aligner sur les valeurs existantes sans tomber dans les banalités marketing. Le positionnement doit être crédible (étayé par les forces réelles de l''entreprise) et adapté aux attentes de la cible. Pas de jargon vide de sens.\n\n🎨 Ton & style: Stratégiquement créatif, langage simple mais inspirant, pour être facilement approprié en interne et percutant en externe.\n\n👥 Audience: Dirigeants et équipe marketing/branding, qui utiliseront ce positionnement pour guider la communication et le développement de l''offre."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '632ce61c-c362-4818-9760-037e648dda9b', false, NULL, false),
	(23, '2025-09-16 15:43:55.64655+00', '2025-10-03 14:45:46.222853+00', '1', '{"en": "Agis comme un(e) expert(e) en stratégie de marque reconnu(e) pour sa créativité exceptionnelle et sa connaissance approfondie du marché.\n\nTu as également une expertise complète sur [Description de l''offre ou du produit] et tu sais créer des noms de marque et des slogans irrésistibles en français.\n\nStyle d’écriture : [style d''écriture souhaité ? ] \n\nÀ partir de ce contexte :\n\nPropose 6 noms de marque accrocheurs avec chacun un slogan.\n\nPour chaque proposition, explique brièvement :\n- Le sens du nom.\n- Les valeurs que le nom véhicule.\n- Respecte impérativement le ton et le style donnés.\n- Ajoute un saut de ligne entre chaque proposition (pas de liste compacte).", "fr": "Agis comme un(e) expert(e) en stratégie de marque reconnu(e) pour sa créativité exceptionnelle et sa connaissance approfondie du marché.\n\nTu as également une expertise complète sur [Description de l''offre ou du produit] et tu sais créer des noms de marque et des slogans irrésistibles en français.\n\nStyle d’écriture : [style d''écriture souhaité ? ] \n\nÀ partir de ce contexte :\n\nPropose 6 noms de marque accrocheurs avec chacun un slogan.\n\nPour chaque proposition, explique brièvement :\n- Le sens du nom.\n- Les valeurs que le nom véhicule.\n- Respecte impérativement le ton et le style donnés.\n- Ajoute un saut de ligne entre chaque proposition (pas de liste compacte)."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', 'fd4e3c39-c920-4671-89f3-f9266b482b16', false, NULL, false),
	(218, '2025-10-15 00:41:40.488515+00', '2025-10-15 00:41:40.488515+00', '1.0', '{"en": "fref"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', 'dc04e22e-b225-4d65-b53d-17320c29252c', false, NULL, true),
	(155, '2025-10-10 12:06:36.030547+00', '2025-10-10 12:06:36.030547+00', '1.0', '{"fr": "test"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', 'cd209b7b-63d3-4b48-bf67-cdac876d5be3', false, NULL, false),
	(8, '2025-09-16 15:43:55.64655+00', '2025-10-14 17:53:29.065795+00', '1', '{"fr": "**Role:**\nTu es un coach expert en pédagogie, passionné par l''apprentissage et la transmission. \n\n**Contexte:**\nCe parcours est destiné à une personne [Indique ton niveau initial - (débutant, intermdéidaire,etc.)] qui souhaite progresser de façon autonome, motivante et structurée.\n\n**Objectif:**\nTon objectif est de créer un parcours d''initiation autodidacte sur le sujet suivant : [Indique le sujet sur lequel tu veux progresser]\nTa mission est de :\nCréer un plan en [nombre d''étapes ou durée, ex : 4 étapes / 6 semaines] clair, rassurant et progressif 🪜\nDonner envie de se lancer à chaque étape, avec des explications accessibles et des objectifs concrets 🎯\nInclure des ressources recommandées (vidéos, articles, exercices, chaînes YouTube, comptes à suivre, outils...) avec des liens. Tu dois vérifier que le lien existe et qu''il est bien dans la langue de l''utilisateur. \nTerminer chaque étape par une mini-mission ou un petit défi à accomplir pour valider la progression 🧩\n\n**Ton & Style:**\nEmployer un ton bienveillant, stimulant et chaleureux qui rassure et motive le lecteur 😊\n\n**Contrainte:**\nN''oublie pas de commencer par une brève introduction inspirante qui donne envie de plonger dans l’aventure 🚀\nUtilise des émojis si cela peut renforcer la clarté ou l’enthousiasme.\n\n**Format de sortie:**\nTitre du parcours\nIntroduction inspirante\nEtape 1 : nom + contenu + ressources + mission\nEtape 2…\nConclusion positive et message d’encouragement final 💪"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '4ccd8560-98df-4ab7-af7d-f3d3568352b2', false, NULL, true),
	(148, '2025-10-09 14:22:15.415177+00', '2025-10-15 10:39:53.055284+00', '1.0', '{"en": "**Rôle:**\nTu es un expert en propriété intellectuelle et en veille technologique, spécialisé dans l’analyse des portefeuilles de brevets, la cartographie de l’innovation industrielle, et la stratégie PI des entreprises innovantes.\n\n**Contexte:**\nJe suis un Business Angel et souhaite obtenir une analyse approfondie du portefeuille de brevets d’une entreprise spécifique pour mieux comprendre son avantage comparatif. Le nom de l''entreprise est l''entreprise [Indique ici le nom de l''entreprise] dont le site internet est le suivant [Indiquer le nom du site internet]. \nCette analyse doit me permettre de comprendre la stratégie PI de l’entreprise, de cartographier ses brevets (par domaines technologiques, géographies, acteurs), et d’évaluer la valeur stratégique réelle de ces brevets (différenciation, innovation, opportunisme, etc.). \n\n**Objectif:**\nTu dois me fournir un diagnostic expert structuré selon les trois axes suivants : \n- Analyse stratégique de la PI : cohérence globale, couverture technologique et géographique, alignement avec les activités de l’entreprise. \n- Cartographie analytique : ventilation des brevets par thématique, date, pays, et type d’innovation, avec des sources sérieuses (Espacenet, WIPO, USPTO, INPI, Google Patents) et des liens directs vers les brevets. \n- Évaluation de la différenciation : degré d’innovation, originalité, caractère de rupture ou stratégie défensive. \n\n**Contrainte:** \n- Analyse uniquement basée sur des données réelles, vérifiables en utilisant des sources reconnues \n- Aucun élément fictif ou spéculatif. \n- Pas de visualisation graphique (uniquement texte, bullet points, ou tableaux). \n- Liens directs vers les brevets déposés. \n- Possibilité d’inclure une comparaison avec les concurrents si cela apporte un éclairage stratégique. \n- Fournis obligatoirement à la fin une section ''Sources'' avec tous les liens consultés. Chaque lien doit être en format URL complet et cliquable (lien actif, pas du texte simple). Organise les sources par catégorie.\"\n\n**Ton & Style:** \n- Professionnel, analytique, neutre, structuré. \n\n**Audience:** \n- Soit didactique, ton audience n''est pas une audience technique mais un investisseur qui souhaite savoir si les technologies brevetées représentent un avantage comparatif\n\n**Format de sortie:**\n🔹 Introduction synthétique du périmètre analysé. \n🔹 Partie 1 : Analyse stratégique de la PI (forces, faiblesses, objectifs apparents). \n🔹 Partie 2 : Cartographie analytique des brevets déposés (par thématique, temporalité, pays…), avec liens vers les bases brevets. Met tes résultats dans un tableau avec une explication détaillée mais didactique de chaque brevet. \n🔹 Partie 3 : Analyse du caractère différenciateur (originalité, valeur ajoutée, impact potentiel). Soit le plus détaillé possible et compréhensible pour un investisseur. \n🔹 Conclusion : synthèse et recommandations stratégiques."}', '95fec575-147d-49ba-bd8d-d8c1295159e6', 0, NULL, '{"en": "", "fr": ""}', 'draft', 'cc34c21c-f673-4d85-b0bc-b412e7a7b877', false, '{chatgpt}', true),
	(9, '2025-09-16 15:43:55.64655+00', '2025-10-15 09:46:11.159723+00', '1', '{"fr": "\n**Role:**\nTu es un expert en synthèse, stratégie et analyse de contenu. \n\n**Contexte:**\nJe dois réaliser l''analyse d''un document. Je vais te fournir un document dont le thème est le suivant : [Indiquer le thème du document envoyé]\nMon analyse a pour but de: [Indiquer l''objectif de l''analyse : Ex : identifier les points faibles avant publication / préparer une réunion / obtenir une synthèse experte / etc.]\n\n**Objectif:**\nTa mission est de faire une **analyse approfondie** du document, structurée, claire et utile pour un lecteur exigeant (dirigeant, investisseur, consultant, etc.).\n\n**Format de sortie:**\nVoici les instructions à suivre :\n\n🔍 1. **Résumé global du document**\n- Résume le document en 10 à 15 lignes maximum.\n- Fais ressortir le **contexte**, les **objectifs principaux**, et les **grandes idées**.\n- Utilise un ton professionnel, synthétique, mais fluide.\n\n🏗️ 2. **Structure et contenu détaillé**\n- Détaille la **structure du document** (parties principales, logique de progression).\n- Pour chaque grande partie, fais une **analyse du contenu** :\n - Quels sont les messages clés ?\n - Quelles données ou arguments sont utilisés ?\n - Quelle est la clarté ou la rigueur de l’argumentation ?\n - Utilise des citations du document pour appuyer tes propos\n\n🎯 3. **Analyse critique et axes d’amélioration**\n- Analyse la **cohérence globale** du document (forme, fond, logique).\n- Signale les éventuelles **faiblesses**, imprécisions ou contradictions.\n- Propose des **axes d’amélioration** : structure, clarté, pertinence, impact.\n\n📌 4. **Ce qu’il faut retenir (TL;DR)**\n- Termine avec une section de 5 à 7 bullet points intitulée :**À retenir en priorité**\n- Résume les points clés du document ou de ton analyse de façon actionnable.\n\n**Contrainte:**\n- Utilise des **titres et sous-titres clairs**\n- Aère les paragraphes\n- Utilise des emojis avec parcimonie pour la lisibilité si pertinent (ex : ✅, ⚠️, 📌)\n- Tu dois finir ton analyse jusqu’à la fin ou si tu ne peux pas , tu dois demander à l’utilisateur ''Clique sur continuer pour que je finisse mon analyse''\n\n\n"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '84f09be6-bf52-4654-b984-13e8c98cf275', false, NULL, true),
	(170, '2025-10-10 15:56:37.652282+00', '2025-10-15 08:05:45.97667+00', 'iioio', '{"fr": "**Role:**Tu es un expert en communication professionnelle et rédaction email. \n\n**Objectif:** Ton objectif est de créer une réponse email précise, contextuelle et adaptée.\n\n**Contexte:**\nVoici les éléments de contexte à prendre en compte :\n- Objectif : [Objectif du mail : informer, proposer, clarifier, refuser, etc.]\n- Ton : [Ton à adopter (formel, semi-formel, amical, neutre, empathique)]\n- Email reçu :[Contenu de l''email auquel vous répondez]\n- Nom entreprise : [ Nom de l''entreprise du destinataire]\n- Style personnel : [Un exemple de votre style de communication (optionnel)]\n\n**Format de sortie:**\n- Salutation personnalisée\n- Réponse directe aux points principaux\n- Informations complémentaires\n- Proposition d''actions ou de prochaines étapes\n- Formule de politesse\n- Ne signe pas le mail mais laisse la personne le faire\n\n**Contrainte:**\n- Analyse précisément l''email original\n- Adapte le ton et le style à la situation\n- Sois clair, concis et professionnel\n- Réponds à toutes les questions posées\n- Anticipe les besoins potentiels du destinataire\n- Propose des actions ou des solutions concrètes si nécessaire\n- Vérifie la grammaire et l''orthographe\n- Inclus une formule de politesse adaptée\n- Évite les réponses génériques\n- Montre de l''empathie et de la compréhension\n- Sois toujours constructif et positif"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'draft', '02a3f1bb-fdf4-4212-8e2f-505f42138a70', false, NULL, true),
	(12, '2025-09-16 15:43:55.64655+00', '2025-10-15 07:59:13.802515+00', '1', '{"fr": "**Rôle:**\nTu es un expert en veille stratégique et en recherche documentaire.\n\n**Contexte:** \nJe souhaite réaliser une recherche documentaire avec le contexte suivant : \n- Thématique principale : [thématique à étudier]\n- Sous-thème spécifique : [sous-thème ou angle particulier à approfondir]\n- Zone géographique ciblée : [pays ou zone géographique cible]\n\n**Objectif:** \n Ta mission est de réaliser une recherche documentaire exhaustive et structurée. L''objectif est d''obtenir une liste exhaustive d’articles et de documents classés par thématique, avec au moins 10 articles par thématique, accompagnés de résumés clairs pour faciliter l''analyse.\n\n**Contrainte:**\nDIRECTIVES SUR LES SOURCES\n- Privilégie les sources officielles : site web de l''entreprise, rapports annuels, communiqués de presse officiels, site spécialisé , site des gouvernements\n- Utilise des sources d''information reconnues en fonction du pays ou de la zone cherchée\n- Consulte des articles de presse spécialisée dans le secteur concerné\n- Pour l''actualité, préfère les articles datant de moins de 12 mois\n- Évite les blogs personnels, forums ou sources non vérifiables\n- Assure toi que le lien existe bien\n- N''utilise pas Wikipédia comme source principale, mais seulement comme point de départ\n- Vérifie la cohérence des informations entre plusieurs sources quand c''est possible\n\n**Format de sortie:**\n1. Classification par grandes thématiques : Identifie et classe les résultats en 3 à 6 grandes thématiques pertinentes.\n2. Sélection d''articles par thématique : Pour chaque thématique identifiée, sélectionne au moins 10 articles ou documents pertinents.\n3. Vérification des sources : Avant de fournir un lien, assure-toi de la fiabilité de la source, de la validité du lien, et de la cohérence de l''information avec la thématique annoncée.\n4. Présentation des résultats : Pour chaque article ou document, fournis les informations suivantes :\n - Titre de l’article ou du document\n - Lien cliquable (assure-toi que le lien est valide et mène à la source annoncée)\n - Résumé concis (3 à 5 lignes) mettant en évidence les points clés et l''apport de l''article\n5. Priorisation des sources : Donne la priorité aux sources fiables, institutionnelles, académiques ou de presse spécialisée.\n6. Format de rendu : Présente les informations sous forme de tableaux clairs pour chaque thématique, facilitant ainsi la lecture et l''analyse.\n7. Tu dois absolument finir jusqu’à la fin ton analyse, ou si tu ne le finis pas, tu dois dire à l’utilisateur “Ecris continuer pour que je finisse l’analyse” \n\n**Ton & Style:**\nLe résultat doit être clair, professionnel et agréable à lire, semblable à un document de cadrage pour une équipe projet. Utilise des titres, des puces, des émojies, une structure lisible et oriente-moi vers des actions concrètes."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '585316ae-62ab-490f-a422-e79d3fab6f3b', false, NULL, true),
	(13, '2025-09-16 15:43:55.64655+00', '2025-10-15 08:47:20.851465+00', '1', '{"fr": "**Rôle:**\nTu es un expert en voyages personnalisés et concepteur de séjours sur-mesure, spécialisé dans la recherche de destinations qui correspondent parfaitement au profil et aux préférences de chaque voyageur.\n\n**Contexte:**\nJe prévois un futur voyage et je souhaite découvrir des destinations parfaitement alignées avec mes attentes spécifiques. L’idée est de recevoir une sélection fine, pertinente et inspirante.\nQuelques éléments de contexte : \n- Type de voyage souhaité : [Type de voyage : mer, montagne, nature, ville]\n- Zone géographique souhaitée : [Zone géographique : France, Europe, Monde]\n- Budget par personne : [Budget en €]\n- Durée du séjour : [Durée du séjour en jours]\n- Activités qui t''intéressent : [Activité : bateau, plage, ski, randonnée, fête, musée, etc.]\n- Période de l’année prévue : [Période de l''année : mois ou saison]\n\n**Objectif:**\nPropose-moi 5 destinations de voyage parfaitement adaptées à mes critères, avec une analyse détaillée et structurée pour chaque lieu, afin que je puisse facilement comparer et choisir la meilleure option.\ndsqqdq\n\n**Contrainte:**\n- Structure impérative à respecter pour chaque destination (7 points listés).\n- Utilise un ton enthousiasmant, professionnel et visuel, avec des emojis pour hiérarchiser l''information.\n- Le contenu doit rester réaliste et pertinent (pas d’exagérations marketing).\n\n**Format de sortie:**\nFiche descriptive harmonisée pour chaque destination.\n🌍 NOM DE LA DESTINATION\n✨ POURQUOI C’EST PARFAIT POUR TOI\n💰 BUDGET ESTIMÉ\n🗓️ ITINÉRAIRE IDÉAL\n🎯 EXPÉRIENCES INCONTOURNABLES\n🌡️ MEILLEURE PÉRIODE\n💎 CONSEIL D’INITIÉ"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '0848ae99-bf62-4652-a64c-8b9a2051cf7c', false, NULL, true),
	(15, '2025-09-16 15:43:55.64655+00', '2025-10-15 09:12:54.569602+00', '1', '{"fr": "**Rôle:**\nTu es un **expert culinaire et guide gastronomique international**, spécialisé dans la découverte de restaurants d’exception adaptés aux préférences spécifiques de chaque client.\n\n**Contexte:**\nJe suis à la recherche d’un restaurant pour une sortie et je souhaite qu’il corresponde parfaitement à mes critères personnels de localisation, cuisine, ambiance et budget. Je veux éviter les recommandations génériques. Les données doivent être vérifiées en croisant plusieurs sources fiables.\nMes exigences sont les suivantes : \n- **Localisation [Indique la localisation souhaitée]** :\n- **Type de cuisine : [Indique le type de cuisine]** :\n- **Budget moyen par personne : [Indique le budget moyen par personne]** :\n- **Ambiance : [Ambiance]**\n\n**Objectif:**\nMe recommander une sélection personnalisée de 4 **restaurants maximum** qui **correspondent exactement** à mes critères, avec des informations détaillées et une présentation claire, attrayante et inspirante.\n\n**Contrainte:**\n- Vérifie systématiquement les informations via la fonction `search()` et croise les sources (Google, Tripadvisor, site officiel…).\n- Ne recommande aucun restaurant sans preuve de fiabilité récente (avis, horaires, etc.).\n- N’invente pas de données si l’information est absente.\n\n**Ton & Style:**\nProfessionnel, engageant et visuellement agréable avec des **emojis** pour une lecture fluide et conviviale.\n\n**Audience**\nGastronome exigeant recherchant une **expérience sur-mesure**.\n\n**Format de sortie**\nPour chaque restaurant, présente les infos suivantes dans une structure aérée :\n1. **🏆 NOM DU RESTAURANT** – localisation précise\n2. **⭐ ÉVALUATION GLOBALE** – note moyenne Google et nombre d’avis\n3. **💬 AVIS POSITIFS** – 3 avis authentiques sur Google\n4. **🍴 SPÉCIALITÉS** – 3 à 4 plats emblématiques en lien avec mes préférences\n5. **💰 FOURCHETTE DE PRIX** – prix moyen par personne + exemples\n6. **🕒 HORAIRES** – heures d’ouverture du jour + politique de réservation\n7. **📍 ACCÈS** – transport, parking, etc.\n8. **📱 CONTACT** – site web, téléphone\n9. **💬 CE QUI FAIT LA DIFFÉRENCE** – vue, service, histoire, concept unique…\n\nEn conclusion : **résume pourquoi ces restaurants sont idéaux selon mes critères + donne-moi un petit conseil gastronomique personnalisé**."}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', '4586c776-517b-429d-b65d-452d30bb822e', false, NULL, true),
	(17, '2025-09-16 15:43:55.64655+00', '2025-10-15 09:18:07.950487+00', '1', '{"fr": "**Rôle:**\nTu es un cinéphile passionné et critique de cinéma indépendant, toujours à la recherche de films et de séries rares, marquants ou sous-cotés, capables de toucher profondément selon les goûts de chacun.\n\n**Contexte:**\nJe suis en quête de nouvelles pépites à découvrir, que ce soit des films ou des séries. Je veux sortir des sentiers battus tout en restant aligné avec mes préférences personnelles (genre, style de production, ambiance, origine géographique), et retrouver le frisson ou l’émotion que j’ai déjà éprouvé dans certains films que j’ai adorés.\nVoici les éléments de contexte à prendre en compte : \nGenre souhaité : [Genre principal souhaité (comédie, drame, etc.] :\nType de production : [Type de production (indépendant, blockbuster,etc.] \nOrigine du film : [Origine géographique]\nExemples de ce que j''aime : [Films ou séries que tu aimes déjà] \n\n**Objectif:**\nMe proposer une sélection ultra-personnalisée de 3 films et 3 séries, en expliquant clairement pourquoi ces recommandations sont faites pour moi, avec des détails enrichissants et engageants.\n\n**Contrainte:**\n- Si possible, utilise ta fonction de recherche sur le web pour récupérer les notes récentes sur AlloCiné (presse et spectateurs) et SensCritique.\n- Ne mentionne pas de film ou série si tu n’as pas une vraie raison solide de penser qu’il correspond à mes goûts (croise avec mes références données).\n- Ne me propose pas de classiques ultra connus sauf si l’angle de recommandation est vraiment original.\n- Évite les spoilers.\n\n**Ton & Style:**\nAmical, passionné, un peu décalé comme un ami cinéphile qui veut vraiment te faire vibrer. Pas professoral, mais plutôt enthousiaste, presque comme une reco autour d’un verre.\n\n**Audience:**\nSpectateur curieux, amateur exigeant de belles histoires et d’univers marquants.\n\n**Format de sortie:**\nPour chaque œuvre (film ou série), présente-moi :\n🎬 Titre & année de sortie\n⭐ Notes AlloCiné (spectateurs & presse) + SensCritique (si dispo via recherche)\n🎯 Pourquoi tu me le recommandes (lien avec mes goûts ou références)\n💡 Ce qui fait son originalité\n🎬 Une anecdote ou un fait marquant\n🎯 À qui ça plaira particulièrement\nTermine avec une mini-conclusion sympa, style : « Si tu dois commencer par une seule œuvre ce soir, choisis celle-ci… »\n\n"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', 'cc101322-76e3-4b6e-9f07-7f2ae1cd776e', false, NULL, true),
	(21, '2025-09-16 15:43:55.64655+00', '2025-10-15 09:25:13.746273+00', '1', '{"fr": "**Rôle:**\nTu es un SEO Strategist et rédacteur de contenu expert de rang mondial (top 0,001 %), spécialiste de la rédaction d’articles E-E-A-T conformes aux dernières directives de Google.\n\n**Contexte:**\nJ''ai rédigé un article et je souhaite l''optimiser pour le SEO. \nMon article est le suivant [Insérer votre article initial].\n\n**Objectif:**\nRédiger un article SEO complet, engageant et optimisé, respectant les meilleures pratiques du SEO éditorial 2025, structuré pour maximiser l’engagement utilisateur et la visibilité organique. L’article doit faire au moins 3000 mots, inclure une FAQ pertinente, des checklists actionnables, et suivre un plan structuré.\n\n**Contrainte:**\nUtiliser uniquement le contenu du transcript (ne rien ajouter).\nNe pas faire de citations ou inventer des anecdotes.\nRespecter une structure lisible : H1, H2, H3.\nAérer le texte, éviter les paragraphes longs.\nSuivre impérativement les techniques de copywriting engageant : storytelling, rythme varié, questions rhétoriques, exemples concrets tirés du transcript.\n\n**Ton & Style:**\nProfessionnel, dynamique et engageant. L’écriture doit capter l’attention dès l’introduction et maintenir l’intérêt tout au long de l’article grâce à un style vivant, fluide et orienté utilisateur.\n\n**Format de sortie:**\nTitre H1 \nIntroduction engageante\nCorps de l’article structuré avec titres H2/H3\nParagraphes courts et aérés\nChecklist actionnable à chaque section pertinente\nConclusion avec appel à l’action\nFAQ en fin d’article\nLongueur : minimum 3000 mots"}', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 0, NULL, '{"en": "", "fr": ""}', 'certified', 'bd51517d-a8af-4f04-ae3e-40546d00df26', false, NULL, false),
	(247, '2025-11-05 17:01:27.418307+00', '2025-11-05 17:01:27.418307+00', '1.0', '{"fr": "Quel temps fait-il à [ville] ?"}', '478b7491-ff6c-490b-982c-a4dc866dcefc', 0, NULL, '{"en": "", "fr": ""}', 'draft', '512ec0bc-7961-43b0-a91c-b4876428641c', false, NULL, true),
	(248, '2025-11-05 17:04:06.797742+00', '2025-11-05 17:04:06.797742+00', '1.0', '{"fr": "aaaaaaaaaaa [feur]"}', '478b7491-ff6c-490b-982c-a4dc866dcefc', 0, NULL, '{"en": "", "fr": ""}', 'draft', 'f1fca1b9-8e72-43b0-8907-4fa8a5f3bf52', false, NULL, true);


--
-- Data for Name: prompt_templates_comments; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: share_invitations; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: stripe_subscriptions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: stripe_webhook_events; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: subscription_audit_log; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: teams; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: users_metadata; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."users_metadata" ("id", "created_at", "user_id", "name", "phone_number", "pinned_official_folder_ids", "pinned_organization_folder_ids", "preferences_metadata", "additional_email", "additional_organization", "linkedin_headline", "linkedin_id", "linkedin_profile_url", "email", "google_id", "company_id", "interests", "job_industry", "job_seniority", "job_type", "organization_ids", "pinned_folder_ids", "pinned_template_ids", "signup_source", "pinned_block_ids", "profile_picture_url", "roles", "data_collection", "first_block_created", "first_template_created", "first_template_used", "keyboard_shortcut_used", "onboarding_dismissed", "stripe_customer_id", "stripe_subscription_id", "subscription_cancel_at_period_end", "subscription_current_period_end", "subscription_plan", "subscription_status") VALUES
	(26, '2025-10-06 12:30:58.576554+00', '0eaa7f45-1f7e-403b-84fc-f02d0f0e18a4', 'Arthur Gotti', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'arthur@jayd.ai', '106760649921620268319', NULL, '{creativity,research,decision_making}', 'tech_software_dev', 'executive', 'sales_marketing', '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{0cf52ff6-0b38-4710-a754-b86fd2c9982a,6adffa50-59c0-4d85-9b35-9a7e20e69126,6ddb4752-d985-412c-9cb9-173b86f2b45c,58ac2937-c229-488d-a8fb-f995f8665e49,d1563751-2b27-4902-a364-291348bbb4ad,6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64}', NULL, 'other:je suis Jaydai', NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "owner"}}', true, false, true, true, false, true, NULL, NULL, false, NULL, NULL, 'free'),
	(25, '2025-10-03 17:13:11.099608+00', '6d90f22e-dfa0-4b34-a88f-c4a533dc85ab', 'Jean-Baptiste HUIBAN', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'b00604891@essec.edu', '116357914315519093526', NULL, NULL, NULL, NULL, NULL, '{19864b30-936d-4a8d-996a-27d17f11f00f,f8d0fe34-32ff-4d90-87ed-28e83c50f953}', '{7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138,d522f0f3-e893-4bd5-b2e4-d28dfbbb298b,a330b6ac-47f8-4a26-9871-7d0937241049,78812c7e-254f-4031-90d8-fe123691b65b,c37fb64a-e55c-4a39-a734-a5590d1d8192,6c5ca58d-d07e-4db7-bc3f-8083c8f5a0c4}', NULL, NULL, NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "owner", "f8d0fe34-32ff-4d90-87ed-28e83c50f953": "admin"}}', true, false, false, false, false, true, NULL, NULL, false, NULL, NULL, 'free'),
	(57, '2025-10-10 12:36:02.184291+00', 'e1e08a40-7482-46e0-87dc-890212ff9148', 'Jean-Baptiste Huiban', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'jean-baptiste+2@jayd.ai', NULL, NULL, NULL, NULL, NULL, NULL, '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138}', NULL, NULL, NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "admin"}}', true, true, true, false, true, true, NULL, NULL, false, NULL, NULL, 'free'),
	(21, '2025-10-02 14:01:55.117997+00', '947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', 'Quentin Bragard', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'quentin@jayd.ai', NULL, NULL, '{}', NULL, NULL, NULL, '{19864b30-936d-4a8d-996a-27d17f11f00f,a0a0e03a-fdbe-4924-83fd-8d4a547c5892}', '{0cf52ff6-0b38-4710-a754-b86fd2c9982a,7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138,dc3fbf96-3401-44a3-ac6c-1ff26e462727}', '{1fb8de3f-ae94-4402-8575-e1ccbab022a1}', NULL, NULL, 'https://pkwyjjoiptjugcreasrc.supabase.co/storage/v1/object/public/images/profile_pictures/947ec8bb-d278-4cd8-9d77-6d9c091ad0f6/86fb539d-6cc6-41a0-9330-55acdbf911ba.jpeg?', '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "owner", "a0a0e03a-fdbe-4924-83fd-8d4a547c5892": "admin"}}', true, false, true, true, true, true, NULL, NULL, false, NULL, NULL, 'free'),
	(27, '2025-10-07 09:04:33.637118+00', '95fec575-147d-49ba-bd8d-d8c1295159e6', 'Jean-Baptiste Huiban', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'jean-baptiste@jayd.ai', '116930847452716825256', NULL, '{coding,email}', 'media_entertainment', 'senior_10_15', 'customer_client_facing', '{19864b30-936d-4a8d-996a-27d17f11f00f,a0a0e03a-fdbe-4924-83fd-8d4a547c5892,f8d0fe34-32ff-4d90-87ed-28e83c50f953}', '{58ac2937-c229-488d-a8fb-f995f8665e49,6ddb4752-d985-412c-9cb9-173b86f2b45c,0a1409da-eb89-41f1-b835-247b14f1dd5c,12ac27d9-7b89-4e2a-9a23-083a84d503c1,227b3cd0-b2ad-4a57-83bf-90c71539d6b3,955c551e-f7e1-4950-a87c-7f4b57578bd5,f4e4127b-6d44-40d6-830b-db326e0c03a1,6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64,7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138,22b1127d-b4e0-4153-94b5-78155021e8a4}', NULL, 'search', NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "owner", "a0a0e03a-fdbe-4924-83fd-8d4a547c5892": "admin", "f8d0fe34-32ff-4d90-87ed-28e83c50f953": "admin"}}', true, false, true, true, true, true, NULL, NULL, false, NULL, NULL, 'free'),
	(156, '2025-10-17 13:53:14.51194+00', 'b9b7bc03-0dac-43da-b7be-3115f1c02404', 'Juli Caceres', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'juli_caceres12@hotmail.com', NULL, NULL, '{data_analysis,email,summarizing,critical_thinking,decision_making}', 'manufacturing_production', 'senior_10_15', 'other:Achats', '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{6ddb4752-d985-412c-9cb9-173b86f2b45c}', NULL, 'search', NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', true, false, false, false, false, false, NULL, NULL, false, NULL, NULL, 'free'),
	(157, '2025-10-17 14:10:49.215861+00', 'e906f2ba-0884-4720-abdd-020ec85631ed', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'lgueunier@gmail.com', '110476447165405002523', NULL, '{}', NULL, NULL, NULL, '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138,0cf52ff6-0b38-4710-a754-b86fd2c9982a,dc3fbf96-3401-44a3-ac6c-1ff26e462727}', NULL, NULL, NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', false, false, false, false, false, false, NULL, NULL, false, NULL, NULL, 'free'),
	(154, '2025-10-15 12:21:34.023126+00', '1f4f5894-0bb9-4471-adc0-ca1085711122', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'rvernes@gmail.com', '112895070192582548103', NULL, '{data_analysis,research,creativity,learning,summarizing,critical_thinking,writing,coding,marketing,decision_making}', 'tech_software_dev', 'executive', 'entrepreneurs_business_owners', '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64,0cf52ff6-0b38-4710-a754-b86fd2c9982a,d1563751-2b27-4902-a364-291348bbb4ad,58ac2937-c229-488d-a8fb-f995f8665e49,ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3}', NULL, 'friend', NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', false, false, false, false, false, false, NULL, NULL, false, NULL, NULL, 'free'),
	(158, '2025-10-17 16:10:22.457247+00', '2dd9518c-04bd-483b-ba35-3934ed20d13a', 'Francois Morin', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'francois.morin@sp2l.com', NULL, NULL, '{email,critical_thinking,decision_making,marketing,data_analysis}', 'healthcare_medical', 'executive', 'entrepreneurs_business_owners', '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64,0cf52ff6-0b38-4710-a754-b86fd2c9982a,d1563751-2b27-4902-a364-291348bbb4ad,6ddb4752-d985-412c-9cb9-173b86f2b45c,6adffa50-59c0-4d85-9b35-9a7e20e69126}', NULL, 'friend', NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', false, false, false, false, false, false, NULL, NULL, false, NULL, NULL, 'free'),
	(159, '2025-10-19 11:17:51.858088+00', '72feaad7-d150-4f6c-b0bf-0d17ccef9bc7', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'inesoddo1@gmail.com', '115317750256251901356', NULL, NULL, NULL, NULL, NULL, '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{6adffa50-59c0-4d85-9b35-9a7e20e69126,58ac2937-c229-488d-a8fb-f995f8665e49,0cf52ff6-0b38-4710-a754-b86fd2c9982a,6ddb4752-d985-412c-9cb9-173b86f2b45c,d522f0f3-e893-4bd5-b2e4-d28dfbbb298b,a330b6ac-47f8-4a26-9871-7d0937241049,78812c7e-254f-4031-90d8-fe123691b65b,c37fb64a-e55c-4a39-a734-a5590d1d8192,6c5ca58d-d07e-4db7-bc3f-8083c8f5a0c4,7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138}', NULL, NULL, NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', false, false, false, false, false, false, NULL, NULL, false, NULL, NULL, 'free'),
	(164, '2025-10-22 15:09:36.283445+00', '56e805cc-14bc-4a59-92dd-25743740539d', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'jbr.apik@gmail.com', '115522248821008507013', NULL, '{writing,data_analysis,marketing,other,email,other:commerce}', 'tech_software_dev', 'mid_5_10', 'sales_marketing', '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{0cf52ff6-0b38-4710-a754-b86fd2c9982a,6adffa50-59c0-4d85-9b35-9a7e20e69126,6ddb4752-d985-412c-9cb9-173b86f2b45c,22b1127d-b4e0-4153-94b5-78155021e8a4}', NULL, 'other:linkedin', NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', true, false, false, true, false, true, NULL, NULL, false, NULL, NULL, 'free'),
	(160, '2025-10-19 19:42:02.585241+00', 'befb33c0-823e-4b7a-bdcd-5aac86003146', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '77raphi@gmail.com', '114594248386044136160', NULL, '{learning,language_learning}', 'healthcare_medical', 'junior_0_5', 'sales_marketing', '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{6adffa50-59c0-4d85-9b35-9a7e20e69126,0cf52ff6-0b38-4710-a754-b86fd2c9982a,560f56ff-2086-4cf2-b78c-cad246d5cb51,ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3}', NULL, 'friend', NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', false, false, false, false, false, false, NULL, NULL, false, NULL, NULL, 'free'),
	(162, '2025-10-21 13:18:40.832345+00', '499f3fda-edf4-423c-80ea-b2ca47592e2b', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'antoine.tournaire@gmail.com', '108113769714325381414', NULL, '{writing,coding,marketing}', 'marketing_advertising', 'lead_15_plus', 'freelance', '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{6adffa50-59c0-4d85-9b35-9a7e20e69126,6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64,0cf52ff6-0b38-4710-a754-b86fd2c9982a}', NULL, 'social_media', NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', false, false, false, false, false, false, NULL, NULL, false, NULL, NULL, 'free'),
	(161, '2025-10-21 11:23:21.322006+00', '2983e811-76f0-43d3-8273-3dcefb5d66ff', 'Hervé Gonay', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'herve.gonay@zenbaia.com', NULL, NULL, '{research,learning,marketing}', 'tech_software_dev', 'executive', 'sales_marketing', '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{0cf52ff6-0b38-4710-a754-b86fd2c9982a,6adffa50-59c0-4d85-9b35-9a7e20e69126,6ddb4752-d985-412c-9cb9-173b86f2b45c,d1563751-2b27-4902-a364-291348bbb4ad,ac04507a-3e58-4fc5-8e2b-5ba7bd9cc5e3}', NULL, 'friend', NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', true, false, false, false, false, false, NULL, NULL, false, NULL, NULL, 'free'),
	(163, '2025-10-21 13:32:52.178565+00', '1d8f2a55-749a-4cf0-b83d-ef88a6146266', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'bartolero@gmail.com', '106824855457062478873', NULL, NULL, NULL, NULL, NULL, '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{6adffa50-59c0-4d85-9b35-9a7e20e69126,58ac2937-c229-488d-a8fb-f995f8665e49,0cf52ff6-0b38-4710-a754-b86fd2c9982a,6ddb4752-d985-412c-9cb9-173b86f2b45c,d522f0f3-e893-4bd5-b2e4-d28dfbbb298b,a330b6ac-47f8-4a26-9871-7d0937241049,78812c7e-254f-4031-90d8-fe123691b65b,c37fb64a-e55c-4a39-a734-a5590d1d8192,6c5ca58d-d07e-4db7-bc3f-8083c8f5a0c4,7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138}', NULL, NULL, NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', false, false, false, true, false, true, NULL, NULL, false, NULL, NULL, 'free'),
	(167, '2025-11-05 15:08:37.530901+00', '478b7491-ff6c-490b-982c-a4dc866dcefc', 'vincent barbier', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'vincent@jayd.ai', NULL, NULL, '{}', NULL, NULL, NULL, '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{dc3fbf96-3401-44a3-ac6c-1ff26e462727,0cf52ff6-0b38-4710-a754-b86fd2c9982a,22b1127d-b4e0-4153-94b5-78155021e8a4,6e034c75-ef0d-4ac5-8d88-f5b9a2b96f64,7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138}', '{a85a49a7-68e2-4bd6-96fd-108cbd90acbc,4586c776-517b-429d-b65d-452d30bb822e,cc101322-76e3-4b6e-9f07-7f2ae1cd776e,b4c419ca-e935-4036-b5a1-c8e1e2043684,0848ae99-bf62-4652-a64c-8b9a2051cf7c,f1fca1b9-8e72-43b0-8907-4fa8a5f3bf52,512ec0bc-7961-43b0-a91c-b4876428641c}', NULL, NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', true, false, false, true, false, true, NULL, NULL, false, NULL, NULL, 'free'),
	(166, '2025-10-27 09:20:24.899378+00', '51eee0a1-8f20-4403-b5f1-0566375db20b', 'Testing Account Jaydai', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'test@jayd.ai', NULL, NULL, '{}', NULL, NULL, NULL, '{19864b30-936d-4a8d-996a-27d17f11f00f}', '{7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138,0cf52ff6-0b38-4710-a754-b86fd2c9982a,dc3fbf96-3401-44a3-ac6c-1ff26e462727}', NULL, NULL, NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "viewer"}}', false, false, false, false, false, false, NULL, NULL, false, NULL, NULL, 'free'),
	(168, '2025-11-09 22:29:53.050306+00', 'eff2a1fd-210c-4b44-9a6f-81af6534c3c8', 'Quentin Bragard', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'quentin+1@jayd.ai', NULL, NULL, NULL, NULL, NULL, NULL, '{19864b30-936d-4a8d-996a-27d17f11f00f,a0a0e03a-fdbe-4924-83fd-8d4a547c5892}', '{6adffa50-59c0-4d85-9b35-9a7e20e69126,58ac2937-c229-488d-a8fb-f995f8665e49,0cf52ff6-0b38-4710-a754-b86fd2c9982a,6ddb4752-d985-412c-9cb9-173b86f2b45c,d522f0f3-e893-4bd5-b2e4-d28dfbbb298b,a330b6ac-47f8-4a26-9871-7d0937241049,78812c7e-254f-4031-90d8-fe123691b65b,c37fb64a-e55c-4a39-a734-a5590d1d8192,6c5ca58d-d07e-4db7-bc3f-8083c8f5a0c4,7e2af8cf-f1e9-45d4-8faa-a7a0d59b1138}', NULL, NULL, NULL, NULL, '{"company": "", "organizations": {"19864b30-936d-4a8d-996a-27d17f11f00f": "owner", "a0a0e03a-fdbe-4924-83fd-8d4a547c5892": "admin"}}', false, false, false, false, false, true, NULL, NULL, false, NULL, NULL, 'free');


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

INSERT INTO "storage"."buckets" ("id", "name", "owner", "created_at", "updated_at", "public", "avif_autodetection", "file_size_limit", "allowed_mime_types", "owner_id", "type") VALUES
	('images', 'images', NULL, '2025-10-06 10:56:01.004242+00', '2025-10-06 10:56:01.004242+00', true, false, NULL, NULL, NULL, 'STANDARD');


--
-- Data for Name: buckets_analytics; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

INSERT INTO "storage"."objects" ("id", "bucket_id", "name", "owner", "created_at", "updated_at", "last_accessed_at", "metadata", "version", "owner_id", "user_metadata", "level") VALUES
	('da4e258b-cfd9-4ace-b044-be069060252c', 'images', 'profile_pictures/947ec8bb-d278-4cd8-9d77-6d9c091ad0f6/86fb539d-6cc6-41a0-9330-55acdbf911ba.jpeg', NULL, '2025-10-06 10:56:40.7669+00', '2025-10-06 10:56:40.7669+00', '2025-10-06 10:56:40.7669+00', '{"eTag": "\"271b1a1f46313cd94a9e0841c14e0314\"", "size": 173826, "mimetype": "image/jpeg", "cacheControl": "max-age=3600", "lastModified": "2025-10-06T10:56:41.000Z", "contentLength": 173826, "httpStatusCode": 200}', 'bdced602-c82f-45b0-b2d8-d0ad6f18566c', NULL, '{}', 3);


--
-- Data for Name: prefixes; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

INSERT INTO "storage"."prefixes" ("bucket_id", "name", "created_at", "updated_at") VALUES
	('images', 'profile_pictures', '2025-10-06 10:56:40.7669+00', '2025-10-06 10:56:40.7669+00'),
	('images', 'profile_pictures/947ec8bb-d278-4cd8-9d77-6d9c091ad0f6', '2025-10-06 10:56:40.7669+00', '2025-10-06 10:56:40.7669+00');


--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 1428, true);


--
-- Name: blog_posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."blog_posts_id_seq"', 1, false);


--
-- Name: chats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."chats_id_seq"', 15961, true);


--
-- Name: landing_page_contact_form_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."landing_page_contact_form_id_seq"', 1, false);


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."messages_id_seq"', 3343, true);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."notifications_id_seq"', 91, true);


--
-- Name: prompt_templates_versions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."prompt_templates_versions_id_seq"', 249, true);


--
-- Name: users_metadata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."users_metadata_id_seq"', 168, true);


--
-- PostgreSQL database dump complete
--

-- \unrestrict gtLofk5iLw18PvbELsO4WEZXAXehtrkLXaecyFgguCoaWEzCMyKIVZRqMEHzYSP

RESET ALL;
