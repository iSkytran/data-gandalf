CREATE TABLE dataset(
   id INTEGER NOT NULL PRIMARY KEY,
   topic TEXT NOT NULL,
   name TEXT NOT NULL,
   description TEXT NOT NULL,
   source TEXT NOT NULL,
   tags TEXT[],
   license TEXT,
   percent_null REAL,
   column_count INTEGER
);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (1,'example','Dataset 1','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (2,'example','Dataset 2','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (3,'example','Dataset 3','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (4,'example','Dataset 4','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (5,'example','Dataset 5','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (6,'example','Dataset 6','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (7,'example','Dataset 7','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (8,'example','Dataset 8','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (9,'example','Dataset 9','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (10,'example','Dataset 10','Some dataset.','https://example.com',NULL,'MIT',0,10);
