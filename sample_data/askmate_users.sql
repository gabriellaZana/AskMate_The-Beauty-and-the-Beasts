ALTER TABLE IF EXISTS ONLY public.user DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;

DROP TABLE IF EXISTS public.user;
DROP SEQUENCE IF EXISTS public.user_id_seq;
CREATE TABLE users (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    user_name text,
    reputation integer
);

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_users_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD users_id integer;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_users_id FOREIGN KEY (users_id) REFERENCES users(id);

ALTER TABLE ONLY answer
    ADD users_id integer;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_users_id FOREIGN KEY (users_id) REFERENCES users(id);

ALTER TABLE ONLY question
    ADD users_id integer;

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_users_id FOREIGN KEY (users_id) REFERENCES users(id);


INSERT INTO users VALUES (1, '2017-05-02 16:55:00', 'DinnyeBeöthy', 0);
INSERT INTO users VALUES (2, '2017-05-02 16:55:00', 'Dankó', 0);
SELECT pg_catalog.setval('users_id_seq', 2, true);
