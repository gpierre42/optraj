CREATE DATABASE  IF NOT EXISTS `optraj_bdd` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `optraj_bdd`;
-- MySQL dump 10.13  Distrib 5.5.37, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: optraj_bdd
-- ------------------------------------------------------
-- Server version	5.5.37-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ASSIGNMENT`
--

DROP TABLE IF EXISTS `ASSIGNMENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ASSIGNMENT` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ID_PHASE` int(10) unsigned NOT NULL,
  `ID_WORKER` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_ASSIGNMENT_ID_PHASE` (`ID_PHASE`),
  KEY `FK_ASSIGNMENT_ID_WORKER` (`ID_WORKER`),
  CONSTRAINT `FK_ASSIGNMENT_ID_PHASE` FOREIGN KEY (`ID_PHASE`) REFERENCES `PHASE` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `FK_ASSIGNMENT_ID_WORKER` FOREIGN KEY (`ID_WORKER`) REFERENCES `WORKER` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ASSIGNMENT`
--

LOCK TABLES `ASSIGNMENT` WRITE;
/*!40000 ALTER TABLE `ASSIGNMENT` DISABLE KEYS */;
/*!40000 ALTER TABLE `ASSIGNMENT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CAR`
--

DROP TABLE IF EXISTS `CAR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CAR` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `PLATE` varchar(30) NOT NULL,
  `MODEL` varchar(30) NOT NULL,
  `NB_PLACE` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=236 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CAR`
--

LOCK TABLES `CAR` WRITE;
/*!40000 ALTER TABLE `CAR` DISABLE KEYS */;
INSERT INTO `CAR` VALUES (1,'MAN','5879XT35',2),(2,'A4','AX-267-WN',5),(3,'Berlingo \'600\' (XUD9)','472YE35',2),(4,'Berlingo \'600\' (XUD9)','3186VV56',2),(5,'Berlingo  \'600\' (XUD7)','5963YK35',2),(6,'Berlingo  \'800\' (DW8)','2891YS35',2),(7,'Berlingo  \'800\' (DW8)','2892YS35',2),(8,'Berlingo \'600\' (DW8)','2125YX35',2),(9,'Berlingo \'600\' (DW8)','433YY35',2),(10,'Berlingo \'600\'','464ZB35',2),(11,'Berlingo \'600\' (DW8)','3752ZH35',2),(12,'Berlingo \'600\' (DW8)','3222ZJ35',2),(13,'Berlingo II \'600\'','898ACP35',2),(14,'Berlingo II \'600\' (DW8)','639ADN35',2),(15,'Berlingo II \'600\' (DW8)','197AEF35',2),(16,'Berlingo II \'600\' (DW8)','867AES35',2),(17,'Berlingo II \'600\'','161AGL35',2),(18,'Berlingo II \'600\'','160AGL35',2),(19,'Berlingo II \'600\'','923AKT35',2),(20,'Berlingo II \'600\' (DW8)','493APT35',2),(21,'Berlingo II \'600\'','BP-571-PE',2),(22,'Berlingo III','BX-026-HE',3),(23,'Berlingo III','CC-010-DP',2),(24,'Berlingo II \'600\'','BS-628-XW',2),(25,'Berlingo III','BP-363-QX',2),(26,'Berlingo III','BP-438-PG',2),(27,'Berlingo II \'600\'','AA-428-YS',2),(28,'Berlingo III','AC-883-QL',2),(29,'Berlingo II \'600\'','AC-862-RG',2),(30,'Berlingo III','AD-594-JJ',2),(31,'Berlingo II \'600\'','AL-101-KC',2),(32,'Berlingo III','AL-372-NQ',2),(33,'Berlingo III','AL-109-NQ',2),(34,'Berlingo','AL-675-XF',5),(35,'Berlingo','AL-736-XF',5),(36,'Berlingo III','AS-585-HJ',2),(37,'Berlingo III','BH-644-BW',2),(38,'Berlingo III','BH-641-BW',2),(39,'Berlingo III','BH-612-BW',2),(40,'Berlingo','BH-410-NM',5),(41,'Berlingo III  ','BH-126-ZC',2),(42,'Berlingo II \'800\'','CB-615-YW',2),(43,'C1','DC-967-YP',2),(44,'C1','DD-243-BY',2),(45,'C15','7797XR35',5),(46,'C2','936AWA35',2),(47,'C3','318ABF35',2),(48,'C3','467ABG35',2),(49,'C3','291ACL35',2),(50,'C3','919AEY35',2),(51,'C3','690AYL35',2),(52,'C3','727AFZ35',2),(53,'C3','877AJP35',2),(54,'C3 II','889APX35',2),(55,'C3 II','242APY35',2),(56,'C3 II','BP-299-NJ',2),(57,'C3 II','BT-019-HJ',2),(58,'C3 II DURISOTTI','DB-451-AC',2),(59,'C3 II','DB-252-AC',2),(60,'C3 II','AB-139-QY',2),(61,'C3 II','AC-876-PC',2),(62,'C3 II','AE-444-WB',2),(63,'C3 II','AJ-399-TB',2),(64,'C3 II','AJ-441-YL',2),(65,'C3 II','AR-320-RH',2),(66,'C3 II','AR-227-RH',2),(67,'C3 II','AR-435-RH',2),(68,'C3 II (A51) entreprise 5 porte','AR-694-ZT',2),(69,'C3 PICASSO airdream confort','BB-270-EF',2),(70,'C3 II','BC-575-CM',2),(71,'C3 PICASSO Confort entreprise','BN-285-AV',2),(72,'C3 PICASSO Confort entreprise','BN-616-VN',2),(73,'C3 PICASSO Confort entreprise','BQ-692-FP',2),(74,'C3 II Business 1.4HDI 70 FAP','CE-582-QG',5),(75,'C4 (3ptes)','BQ-136-SF',2),(76,'C4 (3ptes)','CA-914-BN',2),(77,'C4 1.6L HDI 92cv (DV6ATED4)','BR-882-TJ',5),(78,'C4 (3ptes)','404BBE35',2),(79,'C4 3PTES (DV6ATED4)','141BBS35',2),(80,'C4 HDI 92 AIRDREAM Confort ','CY-606-NP',5),(81,'C4 1.6L HDI 92 (DV6ATED4)','AB-274-QX',5),(82,'C4 1.6L HDI 92 (DV6ATED4)','AD-034-JS',5),(83,'C4 5PTES','AE-973-JR',2),(84,'C4 1.6L HDI 92 (DV6ATED4)','AM-321-FC',5),(85,'C4 HDI 90 Business (DV6ATED4)','CQ-182-NB',5),(86,'C4 HDI 90 Business (DV6ATED4)','CQ-986-NB',5),(87,'C4 HDI 90 Business (DV6ATED4)','CQ-668-NA',5),(88,'C4 PICASSO 1.6 HDI 110 Fap (DV','689AXG35',5),(89,'C4 PICASSO 1.6 HDI 110 Fap (DV','AR-623-YS',5),(90,'C4 PICASSO 1.6L HDI 110 Fap Br','AV-747-NR',7),(91,'C4 PICASSO BREAK (DV6C) BVMP6','BK-627-HR',7),(92,'C5 2.0L HDI 110 (DW10ATED)','8216ZS35',5),(93,'C5 1.6L HDI 110 Fap TOURER (X7','217BCH35',5),(94,'C5 1.6L HDI 110 Fap TOURER (X7','350BCV35',5),(95,'C5 2.0L HDI 138 Fap (X7)  BVM','BJ-951-QP',5),(96,'C5 2.0L HDI 138 Fap 16S 140cv','CF-241-ZR',5),(97,'Jumper benne','6804ZR35',7),(98,'Jumper','7221YZ35',3),(99,'Jumper','7452VV56',6),(100,'Jumper ','7663YE35',9),(101,'Jumper I','5965YK35',3),(102,'Jumper','3479YW35',3),(103,'Jumper ','8396ZF35',3),(104,'Jumper','8378ZF35',3),(105,'Jumper','7284ZM35',3),(106,'Jumper','2963ZR35',3),(107,'Jumper II','8302ZV35',2),(108,'Jumper II','4013ZX35',3),(109,'Jumper ','5453ZY35',9),(110,'Jumper II','2382XE56',3),(111,'Jumper II','251AAX35',3),(112,'Jumper II','9379XH56',7),(113,'Jumper II','955ASL35',3),(114,'Jumper II','179AED35',3),(115,'Jumper','723AFG35',3),(116,'Jumper II','724AFG35',3),(117,'Jumper II','84AFH35',3),(118,'Jumper II','196AFJ35',3),(119,'Jumper II','140AFK35',3),(120,'Jumper II','182AFN35',3),(121,'Jumper II','231AFZ35',3),(122,'Jumper II','321AGM35',3),(123,'Jumper II','904AHT35',3),(124,'Jumper II','BS-809-BB',3),(125,'Jumper II','339AMV35',3),(126,'Jumper II','578ASJ35',3),(127,'Jumper III','CS-170-WR',3),(128,'Jumpy','266WK56',3),(129,'Jumpy','988ZP35',3),(130,'Jumpy','637ADN35',6),(131,'Jumpy','820ADW35',3),(132,'Jumpy','785AFK35',6),(133,'Jumpy','675AER35',3),(134,'Jumpy','672AFB35',6),(135,'Jumpy','787AFK35',6),(136,'Jumpy','985AFP35',6),(137,'Jumpy','146AFS35',6),(138,'Jumpy','CL-899-ZV (48AFT35)',3),(139,'Jumpy','227AGV35',6),(140,'Jumpy','CX-752-RA (139CHW44)',3),(141,'Jumpy','752AJT35',3),(142,'Jumpy','748AJT35',3),(143,'Jumpy','749AJT35',6),(144,'Jumpy','91AKZ35',5),(145,'Jumpy','AW-548-LZ',6),(146,'Jumpy','429ALB35',6),(147,'Jumpy','186ALC35',3),(148,'Jumpy','804ANL35',6),(149,'Jumpy','662ANM35',6),(150,'Jumpy','917ANX35',3),(151,'Jumpy','24AWA35',6),(152,'Jumpy','AD-392-EE',6),(153,'Jumpy III','AM-925-BE',3),(154,'Jumpy III','BB-810-FB',6),(155,'Jumpy III','BG-721-VF',3),(156,'Jumpy III','CC-490-CP',3),(157,'Xsara Picasso 1.6L HDI 92','332ASM35',5),(158,'Xsara Picasso 1.6L HDI 92','911ASW35',5),(159,'Xsara Picasso 1.6L HDI 92','908BAD35',5),(160,'Xsara Picasso 1.6L HDI 92','907BAD35',5),(161,'Saxo','5964YK35',2),(162,'Saxo','9643YY35',2),(163,'Saxo','894ZA35',2),(164,'Saxo','2663ZQ35',2),(165,'Saxo','2662ZQ35',2),(166,'Saxo','106AWD35',2),(167,'Saxo','275AWJ35',2),(168,'Saxo','CX-238-KA (657BZX44)',2),(169,'Saxo (3 Portes)','457AVD35',2),(170,'Saxo','694ACM35',2),(171,'Saxo','719ACX35',2),(172,'Xsara','8606ZH35',2),(173,'Xsara','8163WG56',2),(174,'Xsara','1619ZJ35',2),(175,'Xsara II','3730ZS35',2),(176,'ZX','1826YC35',2),(177,'ZX','1825YC35',2),(178,'TRANSIT','9076ZC35',3),(179,'TRANSIT','2141WP56',6),(180,'308','2185YD35',3),(181,'410','4898XB35',3),(182,'410','2868TZ56',3),(183,'SPRINTER','3229YD35',8),(184,'SPRINTER','3267YV35',3),(185,'PRINTER','CN-400-LP (4730YW35)',3),(186,'SPRINTER','110ZN35',9),(187,'SPRINTER','674AXJ35',3),(188,'VITO','8177ZZ35',3),(189,'CANTER MITSUBISHI','536BBH35',3),(190,'MOVANO','CX-555-RA (127BKW44)',3),(191,'MOVANO','CY-542-PC (339BQC44)',3),(192,'IVARO','DA-782-GV (374BKN44)',3),(193,'VIVARO','CY-556-PC (504BRH44)',3),(194,'307 HDI','CF-861-PD (3388XQ35)',7),(195,'307 HDI','CX-722-RA (635BGZ44)',2),(196,'307 HDI','CX-701-RA (755BSE44)',2),(197,'07','308ASZ35',5),(198,'Boxer','CX-574-RA (602AJH44)',2),(199,'Boxer','368AFC35',3),(200,'Boxer','CY-487-PC (503BJF44)',3),(201,'Boxer','CY-575-PC (208BKB44)',3),(202,'Boxer','341ANX35',3),(203,'Boxer II','2148YE56',3),(204,'Boxer','CD-425-AN',3),(205,'Expert','3012XW35',3),(206,'Expert','495 ATK 35',6),(207,'PARTNER','319ABR35',2),(208,'PARTNER','229ANX35',2),(209,'CLIO','511YY35',2),(210,'CLIO','CD-736-KC (922AMT35)',2),(211,'CLIO II','CN-454-LP (921AMT35)',2),(212,'EXPRESS','510YY35',5),(213,'KANGOO','CF-581-PJ (643ATG35)',2),(214,'MASTER','CF-632-PJ (952AMT35)',3),(215,'MASTER','CN-427-LP (8318ZQ35)',3),(216,'MASCOTT','CY-433-VQ (978AXP44)',3),(217,'MASCOTT','CY-087-XW',3),(218,'SCUDO','CF-612-PJ (1320XZ35)',2),(219,'SCUDO','CD-687-KC (8527XZ35)',5),(220,'DOBLO','CJ-391-DE (6802ZW35)',2),(221,'DOBLO','CL-919-ZV (206BAT35)',2),(222,'DOBLO','CL-907-ZV (929BBS35)',2),(223,'DUCATO','AV-137-FE',9),(224,'DUCATO','AV-834-FE',9),(225,'DUCATO','AV-168-JV',9),(226,'DUCATO','AV-610-JX',9),(227,'DAILY II 2','479WM56',5),(228,'DAILY 35C9','CN-537-WD (465ZM35)',3),(229,'IVECO','CX-655-RA (480AGD44)',3),(230,'IVECO','AR-656-JC',7),(231,'IVECO','CY-036-NW (479CEN44)',3),(232,'IVECO','CY-023-NW (488CEN44)',3),(233,'IVECO','AA-953-WQ',3),(234,'IVECO','AA-981-WQ',3),(235,'IVECO','BJ-244-SB',3);
/*!40000 ALTER TABLE `CAR` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CONSUMER`
--

DROP TABLE IF EXISTS `CONSUMER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CONSUMER` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `LOGIN` varchar(30) NOT NULL,
  `PWD` varchar(100) NOT NULL,
  `LVL` int(10) unsigned NOT NULL,
  `FIRSTNAME` varchar(30) NOT NULL,
  `NAME` varchar(30) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `login_unicity` (`LOGIN`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CONSUMER`
--

LOCK TABLES `CONSUMER` WRITE;
/*!40000 ALTER TABLE `CONSUMER` DISABLE KEYS */;
INSERT INTO `CONSUMER` VALUES (1,'vcollin','21232f297a57a5a743894a0e4a801fc3',3,'Vincent','Collin'),(2,'lgicquel','5f4dcc3b5aa765d61d8327deb882cf99',1,'Lionel','Gicquel'),(3,'mdugenou','5f4dcc3b5aa765d61d8327deb882cf99',2,'Maurice','Dugenoux'),(4,'gdupain','5f4dcc3b5aa765d61d8327deb882cf99',2,'Gérard','Dupain'),(5,'admin','21232f297a57a5a743894a0e4a801fc3',3,'Super','User');
/*!40000 ALTER TABLE `CONSUMER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CRAFT`
--

DROP TABLE IF EXISTS `CRAFT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CRAFT` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `NAME` varchar(30) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CRAFT`
--

LOCK TABLES `CRAFT` WRITE;
/*!40000 ALTER TABLE `CRAFT` DISABLE KEYS */;
INSERT INTO `CRAFT` VALUES (1,'Chef de Chantier'),(2,'Maçon'),(3,'Chef de parc'),(4,'Ravaleur'),(5,'Carotteur'),(6,'Coffreur'),(7,'Agent d\'entretien'),(8,'Chauffeur'),(9,'Finisseur'),(10,'Chef d\'équipe'),(11,'Mécanicien'),(12,'Grutier'),(13,'Carreleur'),(16,'Formateur'),(17,'Apprenti'),(18,'Manoeuvre');
/*!40000 ALTER TABLE `CRAFT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `NEED`
--

DROP TABLE IF EXISTS `NEED`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `NEED` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ID_PHASE` int(10) unsigned NOT NULL,
  `ID_CRAFT` int(10) unsigned NOT NULL,
  `ID_QUALIFICATION` int(10) unsigned NOT NULL,
  `NEED` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_NEED_ID_PHASE` (`ID_PHASE`),
  KEY `FK_NEED_ID_CRAFT` (`ID_CRAFT`),
  KEY `FK_NEED_ID_QUALIFICATION` (`ID_QUALIFICATION`),
  CONSTRAINT `FK_NEED_ID_PHASE` FOREIGN KEY (`ID_PHASE`) REFERENCES `PHASE` (`ID`),
  CONSTRAINT `FK_NEED_ID_CRAFT` FOREIGN KEY (`ID_CRAFT`) REFERENCES `CRAFT` (`ID`),
  CONSTRAINT `FK_NEED_ID_QUALIFICATION` FOREIGN KEY (`ID_QUALIFICATION`) REFERENCES `QUALIFICATION` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `NEED`
--

LOCK TABLES `NEED` WRITE;
/*!40000 ALTER TABLE `NEED` DISABLE KEYS */;
/*!40000 ALTER TABLE `NEED` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PASSENGER`
--
DROP TABLE IF EXISTS `PASSENGER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PASSENGER` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ID_SHUTTLE` int(10) unsigned NOT NULL,
  `ID_WORKER` int(10) unsigned NOT NULL,
  `ID_PICKUP` int(10) unsigned,
  PRIMARY KEY (`ID`),
  KEY `FK_PASSENGER_ID_SHUTTLE` (`ID_SHUTTLE`),
  KEY `FK_PASSENGER_ID_WORKER` (`ID_WORKER`),
  KEY `FK_PASSENGER_ID_PICKUP` (`ID_PICKUP`),
  CONSTRAINT `FK_PASSENGER_ID_SHUTTLE` FOREIGN KEY (`ID_SHUTTLE`) REFERENCES `SHUTTLE` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `FK_PASSENGER_ID_WORKER` FOREIGN KEY (`ID_WORKER`) REFERENCES `WORKER` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `FK_PASSENGER_ID_PICKUP` FOREIGN KEY (`ID_PICKUP`) REFERENCES `PICKUP` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PASSENGER`
--

LOCK TABLES `PASSENGER` WRITE;
/*!40000 ALTER TABLE `PASSENGER` DISABLE KEYS */;
/*!40000 ALTER TABLE `PASSENGER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PHASE`
--

DROP TABLE IF EXISTS `PHASE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PHASE` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ID_SITE` int(10) unsigned NOT NULL,
  `NUM_WEEK` int(10) unsigned NOT NULL,
  `NUM_YEAR` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_PHASE_ID_SITE` (`ID_SITE`),
  CONSTRAINT `FK_PHASE_ID_SITE` FOREIGN KEY (`ID_SITE`) REFERENCES `SITE` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PHASE`
--

LOCK TABLES `PHASE` WRITE;
/*!40000 ALTER TABLE `PHASE` DISABLE KEYS */;
/*!40000 ALTER TABLE `PHASE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PICKUP`
--

DROP TABLE IF EXISTS `PICKUP`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PICKUP` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ID_POSITION` int(10) unsigned NOT NULL,
  `ID_SITE` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_PICKUP_ID_POSITION` (`ID_POSITION`),
  KEY `FK_PICKUP_ID_SITE` (`ID_SITE`),
  CONSTRAINT `FK_PICKUP_ID_POSITION` FOREIGN KEY (`ID_POSITION`) REFERENCES `POSITION` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `FK_PICKUP_ID_SITE` FOREIGN KEY (`ID_SITE`) REFERENCES `SITE` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PICKUP`
--

LOCK TABLES `PICKUP` WRITE;
/*!40000 ALTER TABLE `PICKUP` DISABLE KEYS */;
INSERT INTO `PICKUP` VALUES (1,301,1),(2,302,1),(3,303,1),(4,304,1),(5,305,1),(6,306,1);
/*!40000 ALTER TABLE `PICKUP` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PICKUP_LINK`
--

DROP TABLE IF EXISTS `PICKUP_LINK`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PICKUP_LINK` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ID_PICKUP` int(10) unsigned NOT NULL,
  `ID_SHUTTLE` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_PICKUP_LINK_ID_PICKUP` (`ID_PICKUP`),
  KEY `FK_PICKUP_LINK_ID_SHUTTLE` (`ID_SHUTTLE`),
  CONSTRAINT `FK_PICKUP_LINK_ID_PICKUP` FOREIGN KEY (`ID_PICKUP`) REFERENCES `PICKUP` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `FK_PICKUP_LINK_ID_SHUTTLE` FOREIGN KEY (`ID_SHUTTLE`) REFERENCES `SHUTTLE` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PICKUP_LINK`
--

LOCK TABLES `PICKUP_LINK` WRITE;
/*!40000 ALTER TABLE `PICKUP_LINK` DISABLE KEYS */;
/*!40000 ALTER TABLE `PICKUP_LINK` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `POSITION`
--

DROP TABLE IF EXISTS `POSITION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `POSITION` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `LATITUDE` float NOT NULL,
  `LONGITUDE` float NOT NULL,
  `ADDRESS` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=539 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `POSITION`
--

LOCK TABLES `POSITION` WRITE;
/*!40000 ALTER TABLE `POSITION` DISABLE KEYS */;
INSERT INTO `POSITION` VALUES (301,47.8506,-1.69502,'Bain de Bretagne'),(302,47.8909,-1.98968,'Maure de Bretagne'),(303,47.8668,-1.88595,'Loheac'),(304,48.0674,-1.71435,'Saint-Jacques-de-la-Lande'),(305,48.0832,-1.67616,'Alma'),(306,48.1539,-1.68651,'Saint-Grégoire'),(512,47.239,-1.51653,'Rue de la Souillarderie, Nantes'),(513,48.1306,-1.67649,'Maurepas-Patton - Les Gayeulles, Rennes, France'),(514,48.0909,-1.69586,'11 Rue des 25 Fusillés du 30 Novembre 1942, 35136 Saint-Jacques-de-la-Lande'),(515,47.2284,-1.61044,'16 Allée Armand Trousseau, 44800 Saint-Herblain, France'),(516,47.2135,-1.55968,'passage pommeraye, Nantes'),(517,48.1066,-1.67624,'esplanade charles de gaulle, Rennes'),(518,47.6576,-2.07704,'CHEZ M ET MME DELANNEE JOEL 10'),(519,48.6236,-2.03625,'4 Avenue des Tamaris, 35800 Dinard, France'),(520,47.2735,-2.21385,'Saint Nazaire'),(521,47.6502,-2.09042,'résid Les Charmilles r Lucien Poulard, 35600 REDON'),(522,47.2444,-1.53387,'509 Route de Saint-Joseph, 44000 Nantes'),(523,47.3178,-2.18912,'Trignac'),(524,48.1098,-1.6792,'place de la république, Rennes'),(525,47.9653,-1.49285,'Parc de l\'Yve 35150  Janzé'),(526,47.218,-1.58154,'11 Rue du Calvaire de Grillaud, 44100 Nantes, France'),(527,48.1542,-1.82883,'5 Rue du Prieuré, 35590 Saint-Gilles'),(528,43.6637,7.14882,'Cagnes'),(529,43.6637,7.14882,'Cagnes'),(530,48.1038,-1.69429,'20 Rue Claude Bernard, 35000 Rennes, France'),(531,48.1173,-1.67779,'Rennes'),(532,48.1063,-1.67645,'Esplanade Charles de Gaulle, 35000 Rennes, France'),(533,48.1038,-1.69429,'20 Rue Claude Bernard, 35000 Rennes, France'),(534,48.5705,-1.09579,'Place de Bretagne 50600 Saint-Hilaire-du-Harcouët'),(535,47.6976,-2.80589,'Plescop'),(536,47.589,-3.01532,'D781, 56470 Saint-Philibert, France'),(537,47.2184,-1.55362,'Nantes'),(538,47.4852,-0.55532,'CHU angers');
/*!40000 ALTER TABLE `POSITION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `QUALIFICATION`
--

DROP TABLE IF EXISTS `QUALIFICATION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `QUALIFICATION` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `NAME` varchar(30) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `QUALIFICATION`
--

LOCK TABLES `QUALIFICATION` WRITE;
/*!40000 ALTER TABLE `QUALIFICATION` DISABLE KEYS */;
INSERT INTO `QUALIFICATION` VALUES (1,'ETAM'),(2,'N4P2'),(3,'N4P1'),(4,'N3P2'),(5,'N3P1'),(6,'N2'),(7,'N1P2'),(8,'N1P1');
/*!40000 ALTER TABLE `QUALIFICATION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SHUTTLE`
--

DROP TABLE IF EXISTS `SHUTTLE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SHUTTLE` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ID_DRIVER` int(10) unsigned NOT NULL,
  `ID_CAR` int(10) unsigned NOT NULL,
  `ID_PHASE` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_SHUTTLE_ID_DRIVER` (`ID_DRIVER`),
  KEY `FK_SHUTTLE_ID_CAR` (`ID_CAR`),
  KEY `FK_SHUTTLE_ID_PHASE` (`ID_PHASE`),
  CONSTRAINT `FK_SHUTTLE_ID_DRIVER` FOREIGN KEY (`ID_DRIVER`) REFERENCES `WORKER` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `FK_SHUTTLE_ID_CAR` FOREIGN KEY (`ID_CAR`) REFERENCES `CAR` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `FK_SHUTTLE_ID_PHASE` FOREIGN KEY (`ID_PHASE`) REFERENCES `PHASE` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SHUTTLE`
--

LOCK TABLES `SHUTTLE` WRITE;
/*!40000 ALTER TABLE `SHUTTLE` DISABLE KEYS */;
/*!40000 ALTER TABLE `SHUTTLE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SITE`
--

DROP TABLE IF EXISTS `SITE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SITE` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `NUM_SITE` varchar(9) NOT NULL,
  `NAME` varchar(255) NOT NULL,
  `SITE_MASTER` varchar(30) NOT NULL,
  `SITE_MANAGER` varchar(30) NOT NULL,
  `DATE_INIT` date NOT NULL,
  `DATE_END` date NOT NULL,
  `ID_POSITION` int(10) unsigned NOT NULL,
  `COLOR` varchar(30) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_SITE_ID_POSITION` (`ID_POSITION`),
  CONSTRAINT `FK_SITE_ID_POSITION` FOREIGN KEY (`ID_POSITION`) REFERENCES `POSITION` (`ID`) ON DELETE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SITE`
--

LOCK TABLES `SITE` WRITE;
/*!40000 ALTER TABLE `SITE` DISABLE KEYS */;
INSERT INTO `SITE` VALUES (1,'13003NANT','Cap Eolia - Nantes','WALLET Guy','BODERE Vincent','2014-06-01','2014-12-31',512,'#fff240'),(2,'12019RENN','Les Manades','?','BODERE Vincent','2014-06-01','2014-12-31',513,'#fff240'),(3,'12032STJA','Mairie - St Jacques','?','BODERE Vincent','2014-06-01','2014-12-31',514,'#fff240'),(4,'12005STHE','4 Saisons - St Herblain','?','FORTIN Paul-Henri','2014-06-01','2014-12-31',515,'#00a0fb'),(5,'14001NANT','Ilot Presse Océan - Nantes','?','FORTIN Paul-Henri','2014-06-01','2014-12-31',516,'#00a0fb'),(6,'13024RENN','Cité internationale - Rennes','?','FORTIN Paul-Henri','2014-06-01','2014-12-31',517,'#00a0fb'),(7,'12027DINA','kersao','?','GUERGNON Mathieu','2014-06-01','2014-12-31',519,'#23b500'),(8,'12033STNA','EHPAD G1/G2 - St Nazaire','?','GUERGNON Mathieu','2014-06-01','2014-12-31',520,'#23b500'),(9,'12031REDO','EHPAD les charmilles','?','GUERGNON Mathieu','2014-06-01','2014-12-31',521,'#23b500'),(10,'14002NANT','Gymnase St Joseph','?','GUERGNON Mathieu','2014-06-01','2014-12-31',522,'#23b500'),(11,'13016TRIG','OCEANE - Trignac','?','GUERGNON Mathieu','2014-06-01','2014-12-31',523,'#23b500'),(12,'14004RENN','Lot 3 Métro','?','GUERGNON Mathieu','2014-06-01','2014-12-31',524,'#23b500'),(13,'12020JANZ','Piscine - Janzé','?','JULES','2014-06-01','2014-12-31',525,'#6700d3'),(14,'12036NANT','High Park - Nantes','?','JULES','2014-06-01','2014-12-31',526,'#6700d3'),(15,'13025STGI','Mairie - Saint Gilles','?','JULES','2014-06-01','2014-12-31',527,'#6700d3'),(16,'13017CAGN','Polygone Riviera - Cagnes sur Mer','?','MASSIOT Régis','2014-06-01','2014-12-31',528,'#ff8a18'),(17,'13021CAGN','Polygone Riviera (Zone A)','?','MASSIOT Régis','2014-06-01','2014-12-31',529,'#ff8a18'),(18,'13022RENN','ZAC B Duval - Ilot B7','?','NAIGEON Marc','2014-06-01','2014-12-31',530,'#fb00a0'),(19,'13001RENN','Equipement Socio Culturel - Rennes','?','NAIGEON Marc','2014-06-01','2014-12-31',531,'#fb00a0'),(20,'13002RENN','maison des associations - Rennes','?','NAIGEON Marc','2014-06-01','2014-12-31',532,'#fb00a0'),(21,'13023RENN','ZAC B Duval - ilot C2','?','NAIGEON Marc','2014-06-01','2014-12-31',533,'#fb00a0'),(22,'13007STHI','CH - Saint Hilaire','?','NAIGEON Marc','2014-06-01','2014-12-31',534,'#fb00a0'),(23,'13014PLES','Villa Natura - Plescop','?','OGERON Clément','2014-06-01','2014-12-31',535,'#00a187'),(24,'12023AURA','Kerfanny - Auray','?','OGERON Clément','2014-06-01','2014-12-31',536,'#00a187'),(25,'12035NANT','Crédit agricole CA44','?','OGERON Clément','2014-06-01','2014-12-31',537,'#00a187'),(26,'13013ANG','CHU - Angers','?','OGERON Clément','2014-06-01','2014-12-31',538,'#00a187');
/*!40000 ALTER TABLE `SITE` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER POS_SITE_DELETE
AFTER DELETE ON SITE
FOR EACH ROW
  DELETE FROM POSITION WHERE ID=old.ID_POSITION */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `UNAVAILABILITY`
--

DROP TABLE IF EXISTS `UNAVAILABILITY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UNAVAILABILITY` (
  `NUM_WEEK` int(11) NOT NULL,
  `NUM_YEAR` int(11) NOT NULL,
  `ID_WORKER` int(10) unsigned NOT NULL,
  `TYPE` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`NUM_YEAR`,`ID_WORKER`,`NUM_WEEK`),
  KEY `FK_ID_WORKER` (`ID_WORKER`),
  CONSTRAINT `FK_ID_WORKER` FOREIGN KEY (`ID_WORKER`) REFERENCES `WORKER` (`ID`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UNAVAILABILITY`
--

LOCK TABLES `UNAVAILABILITY` WRITE;
/*!40000 ALTER TABLE `UNAVAILABILITY` DISABLE KEYS */;
/*!40000 ALTER TABLE `UNAVAILABILITY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `WORKER`
--

DROP TABLE IF EXISTS `WORKER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `WORKER` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `NAME` varchar(30) NOT NULL,
  `FIRST_NAME` varchar(30) NOT NULL,
  `BIRTHDATE` date NOT NULL,
  `LICENCE` varchar(30) DEFAULT NULL,
  `ID_POSITION` int(10) unsigned NOT NULL,
  `ID_QUALIFICATION` int(10) unsigned NOT NULL,
  `ID_CRAFT` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_WORKER_ID_QUALIFICATION` (`ID_QUALIFICATION`),
  KEY `FK_WORKER_ID_CRAFT` (`ID_CRAFT`),
  KEY `FK_WORKER_ID_POSITION` (`ID_POSITION`),
  CONSTRAINT `FK_WORKER_ID_QUALIFICATION` FOREIGN KEY (`ID_QUALIFICATION`) REFERENCES `QUALIFICATION` (`ID`),
  CONSTRAINT `FK_WORKER_ID_CRAFT` FOREIGN KEY (`ID_CRAFT`) REFERENCES `CRAFT` (`ID`),
  CONSTRAINT `FK_WORKER_ID_POSITION` FOREIGN KEY (`ID_POSITION`) REFERENCES `POSITION` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `WORKER`
--

LOCK TABLES `WORKER` WRITE;
/*!40000 ALTER TABLE `WORKER` DISABLE KEYS */;
/*!40000 ALTER TABLE `WORKER` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER POS_WORKER_DELETE
AFTER DELETE ON WORKER
FOR EACH ROW
  DELETE FROM POSITION WHERE ID=old.ID_POSITION */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-06-12  9:37:36
