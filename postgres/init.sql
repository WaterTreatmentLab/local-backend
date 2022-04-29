CREATE TABLE public.users(
    user_id int generated by default as identity primary key,
    email varchar unique not null,
    passwd varchar not null
);

CREATE TABLE public.workstation(
    workstation_id int generated by default as identity primary key,
    name varchar not null unique,
    description varchar
);

CREATE TABLE public.operations(
    operation_id int generated by default as identity primary key,
    operation_name varchar not null unique
);

CREATE TABLE public.roles(
    role_id int generated by default as identity primary key,
    role_name varchar not null unique
);

CREATE TABLE public.resources(
    resource_id int generated by default as identity primary key,
    source varchar not null,
    source_id int not null,
    constraint ck_source check ( source in ('user', 'workstation') )
);

CREATE TABLE public.permission(
    role_id int not null,
    operation_id int not null,
    resource_id int not null,
    primary key (role_id, operation_id, resource_id),
    foreign key (role_id) references roles (role_id),
    foreign key (operation_id) references operations (operation_id),
    foreign key (resource_id) references resources (resource_id)
);

CREATE TABLE public.user_roles(
    user_id int,
    role_id int not null,
    constraint pk_permissions primary key (user_id),
    foreign key (user_id) references users (user_id),
    foreign key (role_id) references roles (role_id)
);

CREATE TABLE public.parameters(
    parameter_id int generated by default as identity primary key,
    parameter_name varchar
);

CREATE TABLE public.components(
    component_id int generated by default as identity primary key,
    component_name varchar
);

CREATE TABLE public.metric(
    workstation_id int not null,
    parameter_id int not null,
    component_id int not null,
    primary key (workstation_id, parameter_id, component_id),
    foreign key (workstation_id) references workstation (workstation_id),
    foreign key (parameter_id) references parameters (parameter_id),
    foreign key (component_id) references components (component_id)
);

INSERT INTO public.users (email, passwd)
	VALUES ('user@email.com','$2b$12$yOaeOCNaJybzzO7s13W06ur7bY4E82L.JdKJOkxfqHdY1EXT3Brh.');

INSERT INTO public.workstations (name, description)
	VALUES ('testworstation', 'test description');