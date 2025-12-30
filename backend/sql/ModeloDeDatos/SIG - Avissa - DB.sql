CREATE TABLE avs_streets (
  str_id integer PRIMARY KEY,
  str_name varchar(100),
  geom geometry(MultiLineString,32616)
);

CREATE TABLE avs_routes (
  rot_id integer PRIMARY KEY,
  rot_name varchar(100),
  rot_code varchar(10),
  rty_id integer,
  cls_id integer
);

CREATE TABLE avs_route_paths (
  rtp_id integer PRIMARY KEY,
  geom geometry(MultiLineString,32616),
  rot_id integer,
  dir_id integer
);

CREATE TABLE avs_route_stops (
  rts_id integer PRIMARY KEY,
  rtp_id integer,
  rts_sequence numeric(4),
  rts_name varchar(100),
  geom geometry(Point,32616),
  rts_type varchar(3)
);

CREATE TABLE avs_route_types (
  rty_id integer PRIMARY KEY,
  rty_description varchar(30)
);

CREATE TABLE avs_municipalities (
  mun_id integer PRIMARY KEY,
  mun_name varchar(100),
  geom geometry(MultiPolygon,32616)
);

CREATE TABLE avs_directions (
  dir_id integer PRIMARY KEY,
  dir_name varchar(10)
);

CREATE TABLE avs_route_classes (
  cls_id integer PRIMARY KEY,
  cls_name varchar(50)
);

ALTER TABLE avs_routes ADD FOREIGN KEY (rty_id) REFERENCES avs_route_types (rty_id);

ALTER TABLE avs_routes ADD FOREIGN KEY (cls_id) REFERENCES avs_route_classes (cls_id);

ALTER TABLE avs_route_paths ADD FOREIGN KEY (rot_id) REFERENCES avs_routes (rot_id);

ALTER TABLE avs_route_paths ADD FOREIGN KEY (dir_id) REFERENCES avs_directions (dir_id);

ALTER TABLE avs_route_stops ADD FOREIGN KEY (rtp_id) REFERENCES avs_route_paths (rtp_id);


create sequence avs_str_seq start with 1 increment by 1 ;
create sequence avs_dir_seq start with 1 increment by 1 ;
create sequence avs_mun_seq start with 1 increment by 1 ;
create sequence avs_rtp_seq start with 1 increment by 1 ;
create sequence avs_rot_seq start with 1 increment by 1 ;
create sequence avs_cls_seq start with 1 increment by 1 ;
create sequence avs_rts_seq start with 1 increment by 1 ;
create sequence avs_rty_seq start with 1 increment by 1 ;


select updategeometrysrid('avs_streets', 'geom', 4326); 
select updategeometrysrid('avs_route_stops', 'geom', 4326); 
select updategeometrysrid('avs_municipalities', 'geom', 4326); 
select updategeometrysrid('avs_route_paths', 'geom', 4326);

