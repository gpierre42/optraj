USE `optraj_bdd`;

LOAD DATA LOCAL INFILE "/vagrant/optraj.istic.univ-rennes1.fr/creation_bdd/baseCardinal/datacars.csv"
REPLACE
INTO TABLE CAR
CHARACTER SET utf8
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
(ID, MODEL, PLATE, NB_PLACE);