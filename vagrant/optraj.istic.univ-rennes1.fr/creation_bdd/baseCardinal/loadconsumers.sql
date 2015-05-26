USE `optraj_bdd`;

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/dataconsumers.csv"
REPLACE
INTO TABLE CONSUMER
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID, LOGIN, PWD, LVL, FIRSTNAME, NAME);