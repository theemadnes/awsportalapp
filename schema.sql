drop table if exists entries;
create table instance_tracker (
  id integer primary key autoincrement,
  instance_id text not null,
  instance_type text not null,
  availability_zone text not null
);
