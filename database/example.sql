CREATE TABLE dataset(
   id INTEGER NOT NULL PRIMARY KEY,
   topic TEXT NOT NULL,
   title TEXT NOT NULL,
   description TEXT NOT NULL,
   source TEXT NOT NULL,
   tags TEXT[] NOT NULL,
   licenses TEXT[] NOT NULL,
   col_names TEXT[] NOT NULL,
   col_count INTEGER,
   row_count INTEGER,
   entry_count INTEGER,
   null_count INTEGER,
   usability FLOAT
);

CREATE TABLE rating(
   id INTEGER NOT NULL PRIMARY KEY,
   user_session TEXT NOT NULL,
   recommend BOOLEAN NOT NULL,
   source_dataset INTEGER REFERENCES dataset(id),
   destination_dataset INTEGER REFERENCES dataset(id)
);

INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (1,'examplecom','Dataset 1','Some dataset.','https://example.com','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (2,'examplecom','Dataset 2','Some dataset.','https://example.com','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (3,'examplecom','Dataset 3','Some dataset.','https://example.com','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (4,'examplecom','Dataset 4','Some dataset.','https://example.com','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (5,'examplecom','Dataset 5','Some dataset.','https://example.com','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (6,'examplecom','Dataset 6','Some dataset.','https://example.com','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (7,'examplecom','Dataset 7','Some dataset.','https://example.com','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (8,'examplecom','Dataset 8','Some dataset.','https://example.com','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (9,'examplecom','Dataset 9','Some dataset.','https://example.com','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (10,'examplecom','Dataset 10','Some dataset.','https://example.com','{}','{"MIT"}','{}',10,10,10,10,1.0);

INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (11,'examplenet','Dataset 11','Some dataset.','https://example.net','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (12,'examplenet','Dataset 12','Some dataset.','https://example.net','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (13,'examplenet','Dataset 13','Some dataset.','https://example.net','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (14,'examplenet','Dataset 14','Some dataset.','https://example.net','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (15,'examplenet','Dataset 15','Some dataset.','https://example.net','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (16,'examplenet','Dataset 16','Some dataset.','https://example.net','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (17,'examplenet','Dataset 17','Some dataset.','https://example.net','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (18,'examplenet','Dataset 18','Some dataset.','https://example.net','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (19,'examplenet','Dataset 19','Some dataset.','https://example.net','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (20,'examplenet','Dataset 20','Some dataset.','https://example.net','{}','{"MIT"}','{}',10,10,10,10,1.0);

INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (21,'exampleorg','Dataset 21','Some dataset.','https://example.org','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (22,'exampleorg','Dataset 22','Some dataset.','https://example.org','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (23,'exampleorg','Dataset 23','Some dataset.','https://example.org','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (24,'exampleorg','Dataset 24','Some dataset.','https://example.org','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (25,'exampleorg','Dataset 25','Some dataset.','https://example.org','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (26,'exampleorg','Dataset 26','Some dataset.','https://example.org','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (27,'exampleorg','Dataset 27','Some dataset.','https://example.org','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (28,'exampleorg','Dataset 28','Some dataset.','https://example.org','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (29,'exampleorg','Dataset 29','Some dataset.','https://example.org','{}','{"MIT"}','{}',10,10,10,10,1.0);
INSERT INTO dataset(id,topic,title,description,source,tags,licenses,col_names,col_count,row_count,entry_count,null_count,usability) VALUES (30,'exampleorg','Dataset 30','Some dataset.','https://example.org','{}','{"MIT"}','{}',10,10,10,10,1.0);

INSERT INTO rating(id,user_session,recommend,source_dataset,destination_dataset) VALUES (1,'79208474-49c5-46d9-97b8-824c52a25d82',true,1,2);
INSERT INTO rating(id,user_session,recommend,source_dataset,destination_dataset) VALUES (2,'79208474-49c5-46d9-97b8-824c52a25d82',true,1,3);
INSERT INTO rating(id,user_session,recommend,source_dataset,destination_dataset) VALUES (3,'79208474-49c5-46d9-97b8-824c52a25d82',false,1,4);
INSERT INTO rating(id,user_session,recommend,source_dataset,destination_dataset) VALUES (4,'079208474-49c5-46d9-97b8-824c52a25d82',false,1,5);

