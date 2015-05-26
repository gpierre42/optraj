USE `optraj_bdd`;

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/datapickups.csv"
REPLACE
INTO TABLE PICKUP
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID, ID_POSITION, ID_SITE);
