DROP DATABASE IF EXISTS optraj_bdd;
CREATE DATABASE optraj_bdd;
GRANT ALL PRIVILEGES ON *.* TO 'Client'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'Client'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION;
USE optraj_bdd;

DROP TABLE IF EXISTS CONSUMER;
CREATE TABLE CONSUMER (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  LOGIN VARCHAR(30) NOT NULL,
  PWD VARCHAR(100) NOT NULL,
  LVL INT(10) UNSIGNED NOT NULL,
  FIRSTNAME VARCHAR(30) NOT NULL,
  NAME VARCHAR(30) NOT NULL,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8; 
ALTER TABLE CONSUMER ADD
CONSTRAINT login_unicity UNIQUE
(
login
);

DROP TABLE IF EXISTS QUALIFICATION;
CREATE TABLE QUALIFICATION (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  NAME VARCHAR(30) NOT NULL,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS CRAFT;
CREATE TABLE CRAFT (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  NAME VARCHAR(30) NOT NULL,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS POSITION;
CREATE TABLE POSITION (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  LATITUDE FLOAT NOT NULL,
  LONGITUDE FLOAT NOT NULL,
  ADDRESS VARCHAR(150) NOT NULL,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS SITE;
CREATE TABLE SITE (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  NUM_SITE VARCHAR(30) NOT NULL,
  NAME VARCHAR(30) NOT NULL,
  SITE_MASTER VARCHAR(30) NOT NULL,
  SITE_MANAGER  VARCHAR(30) NOT NULL,
  DATE_INIT DATE NOT NULL,
  DATE_END DATE NOT NULL,
  ID_POSITION INT(10) UNSIGNED NOT NULL,
  COLOR VARCHAR(30) NOT NULL,
  KEY FK_SITE_ID_POSITION (ID_POSITION),
  CONSTRAINT FK_SITE_ID_POSITION FOREIGN KEY (ID_POSITION) REFERENCES POSITION (ID) ON DELETE NO ACTION,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS PHASE;
CREATE TABLE PHASE (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  ID_SITE INT(10) UNSIGNED NOT NULL,
  NUM_WEEK INT(10) UNSIGNED NOT NULL,
  NUM_YEAR INT(10) UNSIGNED NOT NULL,
  KEY FK_PHASE_ID_SITE (ID_SITE),
  CONSTRAINT FK_PHASE_ID_SITE FOREIGN KEY (ID_SITE) REFERENCES SITE (ID),
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS NEED;
CREATE TABLE NEED (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  ID_PHASE INT(10) UNSIGNED NOT NULL,
  ID_CRAFT INT(10) UNSIGNED NOT NULL,
  ID_QUALIFICATION INT(10) UNSIGNED NOT NULL,
  NEED INT(10) UNSIGNED NOT NULL,
  KEY FK_NEED_ID_PHASE (ID_PHASE),
  KEY FK_NEED_ID_CRAFT (ID_CRAFT),
  CONSTRAINT FK_NEED_ID_PHASE FOREIGN KEY (ID_PHASE) REFERENCES PHASE (ID),
  CONSTRAINT FK_NEED_ID_CRAFT FOREIGN KEY (ID_CRAFT) REFERENCES CRAFT (ID),
  CONSTRAINT FK_NEED_ID_QUALIFICATION FOREIGN KEY (ID_QUALIFICATION) REFERENCES QUALIFICATION (ID),
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS WORKER;
CREATE TABLE WORKER (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  NAME VARCHAR(30) NOT NULL,
  FIRST_NAME VARCHAR(30) NOT NULL,
  BIRTHDATE DATE NOT NULL,
  LICENCE VARCHAR(30),
  ID_POSITION INT(10) UNSIGNED NOT NULL,
  ID_QUALIFICATION INT(10) UNSIGNED NOT NULL,
  ID_CRAFT INT(10) UNSIGNED NOT NULL, 
  KEY FK_WORKER_ID_QUALIFICATION (ID_QUALIFICATION),
  CONSTRAINT FK_WORKER_ID_QUALIFICATION FOREIGN KEY (ID_QUALIFICATION) REFERENCES QUALIFICATION (ID),
  KEY FK_WORKER_ID_CRAFT (ID_CRAFT),
  CONSTRAINT FK_WORKER_ID_CRAFT FOREIGN KEY (ID_CRAFT) REFERENCES CRAFT (ID),
  KEY FK_WORKER_ID_POSITION (ID_POSITION),
  CONSTRAINT FK_WORKER_ID_POSITION FOREIGN KEY (ID_POSITION) REFERENCES POSITION (ID),
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS UNAVAILABILITY;
CREATE TABLE UNAVAILABILITY (
  NUM_WEEK INT NOT NULL,
  NUM_YEAR INT NOT NULL,
  ID_WORKER INT(10) UNSIGNED NOT NULL,
  TYPE VARCHAR(45) NULL,
  PRIMARY KEY (NUM_YEAR, ID_WORKER, NUM_WEEK),
  CONSTRAINT FK_ID_WORKER
    FOREIGN KEY (ID_WORKER)
    REFERENCES WORKER (ID)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

DROP TABLE IF EXISTS ASSIGNMENT;
CREATE TABLE ASSIGNMENT (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  ID_PHASE INT(10) UNSIGNED NOT NULL,
  ID_WORKER INT(10) UNSIGNED NOT NULL,
  KEY FK_ASSIGNMENT_ID_PHASE (ID_PHASE),
  KEY FK_ASSIGNMENT_ID_WORKER (ID_WORKER),
  CONSTRAINT FK_ASSIGNMENT_ID_PHASE FOREIGN KEY (ID_PHASE) REFERENCES PHASE (ID) ON DELETE CASCADE,
  CONSTRAINT FK_ASSIGNMENT_ID_WORKER FOREIGN KEY (ID_WORKER) REFERENCES WORKER (ID) ON DELETE CASCADE,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS CAR;
CREATE TABLE CAR (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  PLATE VARCHAR(30) NOT NULL,
  MODEL VARCHAR(30) NOT NULL,
  NB_PLACE INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS SHUTTLE;
CREATE TABLE SHUTTLE (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  ID_DRIVER INT(10) UNSIGNED NOT NULL,
  ID_CAR INT(10) UNSIGNED NOT NULL,
  ID_PHASE INT(10) UNSIGNED NOT NULL,
  KEY FK_SHUTTLE_ID_DRIVER (ID_DRIVER),
  KEY FK_SHUTTLE_ID_CAR (ID_CAR),
  KEY FK_SHUTTLE_ID_PHASE (ID_PHASE),
  CONSTRAINT FK_SHUTTLE_ID_DRIVER FOREIGN KEY (ID_DRIVER) REFERENCES WORKER (ID) ON DELETE CASCADE,
  CONSTRAINT FK_SHUTTLE_ID_CAR FOREIGN KEY (ID_CAR) REFERENCES CAR (ID) ON DELETE CASCADE,
  CONSTRAINT FK_SHUTTLE_ID_PHASE FOREIGN KEY (ID_PHASE) REFERENCES PHASE (ID) ON DELETE CASCADE,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS PASSENGER;
CREATE TABLE PASSENGER (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  ID_SHUTTLE INT(10) UNSIGNED NOT NULL,
  ID_WORKER INT(10) UNSIGNED NOT NULL,
  KEY FK_PASSENGER_ID_SHUTTLE (ID_SHUTTLE),
  KEY FK_PASSENGER_ID_WORKER (ID_WORKER),
  CONSTRAINT FK_PASSENGER_ID_SHUTTLE FOREIGN KEY (ID_SHUTTLE) REFERENCES SHUTTLE (ID) ON DELETE CASCADE,
  CONSTRAINT FK_PASSENGER_ID_WORKER FOREIGN KEY (ID_WORKER) REFERENCES WORKER (ID) ON DELETE CASCADE,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS PICKUP;
CREATE TABLE PICKUP (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  ID_POSITION INT(10) UNSIGNED NOT NULL,
  KEY FK_PICKUP_ID_POSITION (ID_POSITION),
  CONSTRAINT FK_PICKUP_ID_POSITION FOREIGN KEY (ID_POSITION) REFERENCES POSITION (ID) ON DELETE CASCADE,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS PICKUP_LINK;
CREATE TABLE PICKUP_LINK (
  ID INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  ID_PICKUP INT(10) UNSIGNED NOT NULL,
  ID_SHUTTLE INT(10) UNSIGNED NOT NULL,
  KEY FK_PICKUP_LINK_ID_PICKUP (ID_PICKUP),
  KEY FK_PICKUP_LINK_ID_SHUTTLE (ID_SHUTTLE),
  CONSTRAINT FK_PICKUP_LINK_ID_PICKUP FOREIGN KEY (ID_PICKUP) REFERENCES PICKUP (ID) ON DELETE CASCADE,
  CONSTRAINT FK_PICKUP_LINK_ID_SHUTTLE FOREIGN KEY (ID_SHUTTLE) REFERENCES SHUTTLE (ID) ON DELETE CASCADE,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TRIGGER POS_WORKER_DELETE
AFTER DELETE ON WORKER
FOR EACH ROW
  DELETE FROM POSITION WHERE ID=old.ID_POSITION;

CREATE TRIGGER POS_SITE_DELETE
AFTER DELETE ON SITE
FOR EACH ROW
  DELETE FROM POSITION WHERE ID=old.ID_POSITION;

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataConsumers.csv"
INTO TABLE CONSUMER
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(LOGIN, PWD, LVL, FIRSTNAME, NAME,ID);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataQualification.csv"
INTO TABLE QUALIFICATION
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(NAME, ID);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataCraft.csv"
INTO TABLE CRAFT
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(NAME, ID);


LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataPosition.csv"
INTO TABLE POSITION
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(LATITUDE, LONGITUDE, ADDRESS);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataWorker.csv"
INTO TABLE WORKER
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(NAME, FIRST_NAME, BIRTHDATE, LICENCE, ID_POSITION, ID_CRAFT, ID_QUALIFICATION);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataSite.csv"
INTO TABLE SITE
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID, NUM_SITE, NAME, SITE_MASTER, SITE_MANAGER, DATE_INIT, DATE_END, ID_POSITION, COLOR);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataPhase.csv"
INTO TABLE PHASE
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID_SITE, NUM_WEEK, NUM_YEAR);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataNeed.csv"
INTO TABLE NEED
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID_PHASE, ID_CRAFT, ID_QUALIFICATION, NEED);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataAssignment.csv"
INTO TABLE ASSIGNMENT
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID_PHASE, ID_WORKER);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataCar.csv"
INTO TABLE CAR
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(MODEL,PLATE, NB_PLACE);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataPickup.csv"
INTO TABLE PICKUP
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID_POSITION);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataShuttle.csv"
INTO TABLE SHUTTLE
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID_DRIVER, ID_CAR, ID_PHASE);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataPassenger.csv"
INTO TABLE PASSENGER
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID_SHUTTLE, ID_WORKER);

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/demo/dataPickupLink.csv"
INTO TABLE PICKUP_LINK
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID_PICKUP, ID_SHUTTLE);