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

INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (1,'examplecom','Dataset 1','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (2,'examplecom','Dataset 2','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (3,'examplecom','Dataset 3','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (4,'examplecom','Dataset 4','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (5,'examplecom','Dataset 5','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (6,'examplecom','Dataset 6','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (7,'examplecom','Dataset 7','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (8,'examplecom','Dataset 8','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (9,'examplecom','Dataset 9','Some dataset.','https://example.com',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (10,'examplecom','Dataset 10','Some dataset.','https://example.com',NULL,'MIT',0,10);

INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (11,'examplenet','Dataset 11','Some dataset.','https://example.net',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (12,'examplenet','Dataset 12','Some dataset.','https://example.net',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (13,'examplenet','Dataset 13','Some dataset.','https://example.net',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (14,'examplenet','Dataset 14','Some dataset.','https://example.net',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (15,'examplenet','Dataset 15','Some dataset.','https://example.net',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (16,'examplenet','Dataset 16','Some dataset.','https://example.net',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (17,'examplenet','Dataset 17','Some dataset.','https://example.net',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (18,'examplenet','Dataset 18','Some dataset.','https://example.net',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (19,'examplenet','Dataset 19','Some dataset.','https://example.net',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (20,'examplenet','Dataset 20','Some dataset.','https://example.net',NULL,'MIT',0,10);

INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (21,'exampleorg','Dataset 21','Some dataset.','https://example.org',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (22,'exampleorg','Dataset 22','Some dataset.','https://example.org',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (23,'exampleorg','Dataset 23','Some dataset.','https://example.org',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (24,'exampleorg','Dataset 24','Some dataset.','https://example.org',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (25,'exampleorg','Dataset 25','Some dataset.','https://example.org',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (26,'exampleorg','Dataset 26','Some dataset.','https://example.org',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (27,'exampleorg','Dataset 27','Some dataset.','https://example.org',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (28,'exampleorg','Dataset 28','Some dataset.','https://example.org',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (29,'exampleorg','Dataset 29','Some dataset.','https://example.org',NULL,'MIT',0,10);
INSERT INTO dataset(id,topic,name,description,source,tags,license,percent_null,column_count) VALUES (30,'exampleorg','Dataset 30','Some dataset.','https://example.org',NULL,'MIT',0,10);
