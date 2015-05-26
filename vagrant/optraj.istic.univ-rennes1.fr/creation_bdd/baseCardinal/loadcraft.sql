USE `optraj_bdd`;

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/datacrafts.csv"
REPLACE
INTO TABLE CRAFT
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID, NAME);