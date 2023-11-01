-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ktg_forum_api
-- ------------------------------------------------------
-- Server version	11.1.2-MariaDB

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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id_category` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `created_on` datetime NOT NULL,
  `is_private` tinyint(1) NOT NULL DEFAULT 0,
  `is_locked` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_category`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id_message` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `created_on` datetime NOT NULL,
  `subject` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `id_parent_message` int(11) DEFAULT NULL,
  `id_author` int(11) NOT NULL,
  PRIMARY KEY (`id_message`),
  KEY `fk_messages_users1_idx` (`id_author`),
  CONSTRAINT `fk_messages_users1` FOREIGN KEY (`id_author`) REFERENCES `users` (`id_user`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `private_categories`
--

DROP TABLE IF EXISTS `private_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `private_categories` (
  `categories_id_category` int(11) NOT NULL,
  `users_id_user` int(11) NOT NULL,
  `has_write_access` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`categories_id_category`,`users_id_user`),
  KEY `fk_categories_has_users_users1_idx` (`users_id_user`),
  KEY `fk_categories_has_users_categories_idx` (`categories_id_category`),
  CONSTRAINT `fk_categories_has_users_categories` FOREIGN KEY (`categories_id_category`) REFERENCES `categories` (`id_category`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_categories_has_users_users1` FOREIGN KEY (`users_id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `private_categories`
--

LOCK TABLES `private_categories` WRITE;
/*!40000 ALTER TABLE `private_categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `private_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `replies`
--

DROP TABLE IF EXISTS `replies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `replies` (
  `id_reply` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `topics_id_topic` int(11) NOT NULL,
  `users_id_user` int(11) NOT NULL,
  `created_on` datetime NOT NULL,
  `is_best` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_reply`),
  KEY `fk_table1_topics1_idx` (`topics_id_topic`),
  KEY `fk_replies_users1_idx` (`users_id_user`),
  CONSTRAINT `fk_replies_users1` FOREIGN KEY (`users_id_user`) REFERENCES `users` (`id_user`) ON UPDATE NO ACTION,
  CONSTRAINT `fk_table1_topics1` FOREIGN KEY (`topics_id_topic`) REFERENCES `topics` (`id_topic`) ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `replies`
--

LOCK TABLES `replies` WRITE;
/*!40000 ALTER TABLE `replies` DISABLE KEYS */;
/*!40000 ALTER TABLE `replies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topics`
--

DROP TABLE IF EXISTS `topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topics` (
  `id_topic` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `created_on` datetime NOT NULL,
  `text` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `id_category` int(11) NOT NULL,
  `id_author` int(11) NOT NULL,
  `is_locked` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_topic`),
  UNIQUE KEY `title_UNIQUE` (`title`),
  KEY `fk_topics_categories1_idx` (`id_category`),
  KEY `fk_topics_users1_idx` (`id_author`),
  CONSTRAINT `fk_topics_categories1` FOREIGN KEY (`id_category`) REFERENCES `categories` (`id_category`) ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1` FOREIGN KEY (`id_author`) REFERENCES `users` (`id_user`) ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topics`
--

LOCK TABLES `topics` WRITE;
/*!40000 ALTER TABLE `topics` DISABLE KEYS */;
/*!40000 ALTER TABLE `topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `password` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `created_on` datetime NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'Georgi Tashev','$2b$12$GGuq3fFxL4zP2wthWeR/euU53xz8736C9uRocPlwyuVSbSYGqtFYK','2023-10-19 10:06:45',0),(6,'PetarTashev','$2b$12$8v5EjOgeeJ74Wee5Nhk2M./1S74rMP23oFRVAe73tQyXhxYavRuUG','2023-10-19 10:27:20',0),(7,'Tashev','$2b$12$3aw2UG8zg04W1jT9yeXhNeR1ag0guqzDWv9cw4PufHyysvWnnu6zm','2023-10-19 10:29:52',0),(9,'GTashev','$2b$12$K4Ne2TzzuaG2HBYJgTcEwef7XP/.IawAwVNlT4ogRR2WJ5cRfN6l6','2023-10-19 10:31:01',0),(10,'GVTashev','$2b$12$kpSTcoFBSQQkC94a2dfJZuVazI.W1Xb.ORJXs3v5efl3VFSPJwjiS','2023-10-19 10:37:22',0),(11,'Trifon','$2b$12$0zTZYEsWRCL3N5ce8GrTUud.RJ/HDVt0UZUP2STg36zXp798bLuha','2023-10-19 10:45:19',0),(12,'Trifon1','$2b$12$QeLlIrrF.bf8z0.trUcJcuuV0vYt8pTiogCc6cGEgbd//Ucwzn1j6','2023-10-19 10:48:09',0),(13,'Trifon2','$2b$12$653fnvt3.2knZiFLKggWYO72mZFvjm6wxUIRJaTo.6LB0QJXsPHOi','2023-10-19 11:04:24',0),(14,'Трифон','$2b$12$XJf3cvY5/RVrC0CxSNewYuQ1v61ZFaBFYf48W9ZwTfUBk.AERQrHC','2023-10-19 11:15:25',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_has_messages`
--

DROP TABLE IF EXISTS `users_has_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_has_messages` (
  `id_recipient` int(11) NOT NULL,
  `id_message` int(11) NOT NULL,
  PRIMARY KEY (`id_recipient`,`id_message`),
  KEY `fk_users_has_messages_messages1_idx` (`id_message`),
  KEY `fk_users_has_messages_users1_idx` (`id_recipient`),
  CONSTRAINT `fk_users_has_messages_messages1` FOREIGN KEY (`id_message`) REFERENCES `messages` (`id_message`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_messages_users1` FOREIGN KEY (`id_recipient`) REFERENCES `users` (`id_user`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_has_messages`
--

LOCK TABLES `users_has_messages` WRITE;
/*!40000 ALTER TABLE `users_has_messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_has_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `votes`
--

DROP TABLE IF EXISTS `votes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `votes` (
  `replies_id_reply` int(11) NOT NULL,
  `users_id_user` int(11) NOT NULL,
  `is_upvote` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`replies_id_reply`,`users_id_user`),
  KEY `fk_replies_has_users_users1_idx` (`users_id_user`),
  KEY `fk_replies_has_users_replies1_idx` (`replies_id_reply`),
  CONSTRAINT `fk_replies_has_users_replies1` FOREIGN KEY (`replies_id_reply`) REFERENCES `replies` (`id_reply`) ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_has_users_users1` FOREIGN KEY (`users_id_user`) REFERENCES `users` (`id_user`) ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `votes`
--

LOCK TABLES `votes` WRITE;
/*!40000 ALTER TABLE `votes` DISABLE KEYS */;
/*!40000 ALTER TABLE `votes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'ktg_forum_api'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-19 14:21:31
