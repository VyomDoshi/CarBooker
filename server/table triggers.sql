-- to avoid making the triggers circular in nature we add an if statement so that the loop doesnt keep going on.
use db4;
delimiter /
CREATE TRIGGER PID_AI AFTER INSERT
ON db4.pid for each row
begin
if (select count(*) from db1.pid where pid = new.pid AND port_no = new.port_no AND stat = new.stat)=0 then
INSERT INTO db1.pid values(new.pid, new.port_no, new.stat);
end if;
if (select count(*) from db2.pid where pid = new.pid AND port_no = new.port_no AND stat = new.stat)=0 then
INSERT INTO db2.pid values(new.pid, new.port_no, new.stat);
end if;
if (select count(*) from db3.pid where pid = new.pid AND port_no = new.port_no AND stat = new.stat)=0 then
INSERT INTO db3.pid values(new.pid, new.port_no, new.stat);
end if;
end/

CREATE TRIGGER PID_AU AFTER UPDATE
ON db4.pid for each row
begin
if (select count(*) from db1.pid where pid = new.pid AND port_no = new.port_no AND stat = new.stat)=0 then
UPDATE db1.pid SET stat = new.stat WHERE pid = new.pid;
end if;
if (select count(*) from db2.pid where pid = new.pid AND port_no = new.port_no AND stat = new.stat)=0 then
UPDATE db2.pid SET stat = new.stat WHERE pid = new.pid;
end if;
if (select count(*) from db3.pid where pid = new.pid AND port_no = new.port_no AND stat = new.stat)=0 then
UPDATE db3.pid SET stat = new.stat WHERE pid = new.pid;
end if;
end/

CREATE TRIGGER CAR_AU AFTER UPDATE
ON db4.car_details for each row
begin
if (select count(*) from db1.car_details where id = new.id AND name_car = new.name_car AND quantity = new.quantity AND price_per_km = new.price_per_km)=0 then
UPDATE db1.car_details SET quantity = new.quantity WHERE id = new.id;
end if;
if (select count(*) from db2.car_details where id = new.id AND name_car = new.name_car AND quantity = new.quantity AND price_per_km = new.price_per_km)=0 then
UPDATE db2.car_details SET quantity = new.quantity WHERE id = new.id;
end if;
if (select count(*) from db3.car_details where id = new.id AND name_car = new.name_car AND quantity = new.quantity AND price_per_km = new.price_per_km)=0 then
UPDATE db3.car_details SET quantity = new.quantity WHERE id = new.id;
end if;
end/

CREATE TRIGGER CAR_AI AFTER INSERT
ON db4.car_details for each row
begin
if (select count(*) from db1.car_details where id = new.id AND name_car = new.name_car AND quantity = new.quantity AND price_per_km = new.price_per_km)=0 then
INSERT INTO db1.car_details values(new.id, new.name_car, new.quantity, new.price_per_km);
end if;
if (select count(*) from db2.car_details where id = new.id AND name_car = new.name_car AND quantity = new.quantity AND price_per_km = new.price_per_km)=0 then
INSERT INTO db2.car_details values(new.id, new.name_car, new.quantity, new.price_per_km);
end if;
if (select count(*) from db3.car_details where id = new.id AND name_car = new.name_car AND quantity = new.quantity AND price_per_km = new.price_per_km)=0 then
INSERT INTO db3.car_details values(new.id, new.name_car, new.quantity, new.price_per_km);
end if;
end/

delimiter ;