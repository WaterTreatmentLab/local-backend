CREATE TABLE public.users (
	email varchar NULL,
	"password" varchar NULL
);

CREATE TABLE public.workstations (
	name varchar NULL,
	test varchar NULL
);

INSERT INTO public.users (email,"password")
	VALUES ('user@email.com','$2b$12$yOaeOCNaJybzzO7s13W06ur7bY4E82L.JdKJOkxfqHdY1EXT3Brh.');

INSERT INTO public.workstations (name,test)
	VALUES ('testworkstation','test');