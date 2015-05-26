USE `optraj_bdd`;

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/dataqualifications.csv"
REPLACE
INTO TABLE QUALIFICATION
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID, NAME);
