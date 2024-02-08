CREATE DATABASE  IF NOT EXISTS `OnStreetParking` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `OnStreetParking`;
-- MySQL dump 10.13  Distrib 8.1.0, for Linux (x86_64)
--
-- Host: 172.17.0.3    Database: OnStreetParking
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ParkingSite`
--

DROP TABLE IF EXISTS `ParkingSite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ParkingSite` (
  `idParkingSite` varchar(45) NOT NULL,
  `ps_description` varchar(45) DEFAULT NULL,
  `ps_location` varchar(45) DEFAULT NULL,
  `ps_max_parking_spots` int DEFAULT NULL,
  PRIMARY KEY (`idParkingSite`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ParkingSite`
--

LOCK TABLES `ParkingSite` WRITE;
/*!40000 ALTER TABLE `ParkingSite` DISABLE KEYS */;
/*!40000 ALTER TABLE `ParkingSite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TrafficViolation`
--

DROP TABLE IF EXISTS `TrafficViolation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TrafficViolation` (
  `tf_id` varchar(100) NOT NULL,
  `tf_desc` varchar(500) DEFAULT NULL,
  `tf_location` varchar(500) DEFAULT NULL,
  `tf_ref_parksite` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`tf_id`),
  UNIQUE KEY `idTrafficViolation_UNIQUE` (`tf_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TrafficViolation`
--

LOCK TABLES `TrafficViolation` WRITE;
/*!40000 ALTER TABLE `TrafficViolation` DISABLE KEYS */;
INSERT INTO `TrafficViolation` VALUES ('ID_SOMETGING_1111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [625.148315, 327.366516]}','ParkingSite_1704641342'),('ID_SOMETGING_11111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [625.148315, 327.366516]}','ParkingSite_1704641342'),('ID_SOMETGING_111111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [625.148315, 327.366516]}','ParkingSite_1704641342'),('ID_SOMETGING_1111111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [625.148315, 327.366516]}','ParkingSite_1704641342'),('ID_SOMETGING_11111111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [38.248736, 21.738931]}','ParkingSite_1704641342'),('ID_SOMETGING_111111111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [38.248736, 21.738931]}','ParkingSite_1704641342'),('ID_SOMETGING_1111111111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [38.248736, 21.738931]}','ParkingSite_1704641342'),('ID_SOMETGING_11111111111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [38.248736, 21.738931]}','ParkingSite_1704641342'),('ID_SOMETGING_111111111111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [38.248736, 21.738931]}','ParkingSite_1704641342'),('ID_SOMETGING_1111111111111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [38.248736, 21.738931]}','ParkingSite_1704641342'),('ID_SOMETGING_11111112111111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [38.248736, 21.738931]}','ParkingSite_1704641342'),('ID_SOMETGING_111111121211111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [38.248736, 21.738931]}','ParkingSite_1704641342'),('ID_SOMETGING_1111111212211111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [38.248736, 21.738931]}','ParkingSite_1704641342'),('ID_SOMETGING_123112','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [625.148315, 327.366516]}','[\"ParkingSite_1704641342\"]'),('ID_SOMETGING_1231123','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [625.148315, 327.366516]}','\"ParkingSite_1704641342\"'),('ID_SOMETGING_12311231','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [625.148315, 327.366516]}','ParkingSite_1704641342'),('ID_SOMETGING_123112311','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [625.148315, 327.366516]}','ParkingSite_1704641342'),('ID_SOMETGING_1231123111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [625.148315, 327.366516]}','ParkingSite_1704641342'),('ID_SOMETGING_12311231111','illegal parking for atleast 8','{\"type\": \"Point\", \"coordinates\": [625.148315, 327.366516]}','ParkingSite_1704641342');
/*!40000 ALTER TABLE `TrafficViolation` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-08  8:40:55
