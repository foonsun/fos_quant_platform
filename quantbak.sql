-- MySQL dump 10.13  Distrib 5.6.42, for Linux (x86_64)
--
-- Host: localhost    Database: quant
-- ------------------------------------------------------
-- Server version	5.6.42

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
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) COLLATE utf8_unicode_ci NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `account_emailaddress_user_id_2c513194_fk_auth_user_id` (`user_id`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `email_address_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address_country`
--

DROP TABLE IF EXISTS `address_country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address_country` (
  `iso_3166_1_a2` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `iso_3166_1_a3` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `iso_3166_1_numeric` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `printable_name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `display_order` smallint(5) unsigned NOT NULL,
  `is_shipping_country` tinyint(1) NOT NULL,
  PRIMARY KEY (`iso_3166_1_a2`),
  KEY `address_country_display_order_dc88cde8` (`display_order`),
  KEY `address_country_is_shipping_country_f7b6c461` (`is_shipping_country`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_country`
--

LOCK TABLES `address_country` WRITE;
/*!40000 ALTER TABLE `address_country` DISABLE KEYS */;
/*!40000 ALTER TABLE `address_country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address_useraddress`
--

DROP TABLE IF EXISTS `address_useraddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address_useraddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line1` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line2` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line3` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line4` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `state` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `postcode` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `search_text` longtext COLLATE utf8_unicode_ci NOT NULL,
  `phone_number` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `notes` longtext COLLATE utf8_unicode_ci NOT NULL,
  `is_default_for_shipping` tinyint(1) NOT NULL,
  `is_default_for_billing` tinyint(1) NOT NULL,
  `num_orders_as_shipping_address` int(10) unsigned NOT NULL,
  `hash` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `country_id` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  `num_orders_as_billing_address` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `address_useraddress_user_id_hash_9d1738c7_uniq` (`user_id`,`hash`),
  KEY `address_useraddress_country_id_fa26a249_fk_address_c` (`country_id`),
  KEY `address_useraddress_hash_e0a6b290` (`hash`),
  CONSTRAINT `address_useraddress_country_id_fa26a249_fk_address_c` FOREIGN KEY (`country_id`) REFERENCES `address_country` (`iso_3166_1_a2`),
  CONSTRAINT `address_useraddress_user_id_6edf0244_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_useraddress`
--

LOCK TABLES `address_useraddress` WRITE;
/*!40000 ALTER TABLE `address_useraddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `address_useraddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analytics_productrecord`
--

DROP TABLE IF EXISTS `analytics_productrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analytics_productrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num_views` int(10) unsigned NOT NULL,
  `num_basket_additions` int(10) unsigned NOT NULL,
  `num_purchases` int(10) unsigned NOT NULL,
  `score` double NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`),
  KEY `analytics_productrecord_num_purchases_405301a0` (`num_purchases`),
  CONSTRAINT `analytics_productrec_product_id_dad3a871_fk_catalogue` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analytics_productrecord`
--

LOCK TABLES `analytics_productrecord` WRITE;
/*!40000 ALTER TABLE `analytics_productrecord` DISABLE KEYS */;
INSERT INTO `analytics_productrecord` VALUES (1,239,51,6,0,3);
/*!40000 ALTER TABLE `analytics_productrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analytics_userproductview`
--

DROP TABLE IF EXISTS `analytics_userproductview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analytics_userproductview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `product_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `analytics_userproduc_product_id_a55b87ad_fk_catalogue` (`product_id`),
  KEY `analytics_userproductview_user_id_5e49a8b1_fk_auth_user_id` (`user_id`),
  CONSTRAINT `analytics_userproduc_product_id_a55b87ad_fk_catalogue` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`),
  CONSTRAINT `analytics_userproductview_user_id_5e49a8b1_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=232 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analytics_userproductview`
--

LOCK TABLES `analytics_userproductview` WRITE;
/*!40000 ALTER TABLE `analytics_userproductview` DISABLE KEYS */;
INSERT INTO `analytics_userproductview` VALUES (1,'2019-03-17 13:01:39.329411',3,1),(2,'2019-03-17 13:02:06.213498',3,1),(3,'2019-03-17 13:02:17.011093',3,1),(4,'2019-03-17 13:02:23.751181',3,1),(5,'2019-03-17 13:02:41.982429',3,1),(6,'2019-03-17 13:02:53.653871',3,1),(7,'2019-03-17 13:31:40.311104',3,1),(8,'2019-03-17 13:31:54.776603',3,1),(9,'2019-03-17 13:32:43.753273',3,1),(10,'2019-03-17 13:32:54.001562',3,1),(11,'2019-03-17 13:33:14.395352',3,1),(12,'2019-03-17 13:33:17.338964',3,1),(13,'2019-03-17 14:15:07.566874',3,1),(14,'2019-03-17 14:15:11.717017',3,1),(15,'2019-03-17 14:15:14.261394',3,1),(16,'2019-03-17 14:18:47.666399',3,1),(17,'2019-03-17 14:18:46.761337',3,1),(18,'2019-03-17 14:18:56.470924',3,1),(19,'2019-03-17 14:31:22.693592',3,1),(20,'2019-03-17 14:32:41.234503',3,1),(21,'2019-03-17 14:32:51.347427',3,1),(22,'2019-03-17 14:32:57.118344',3,1),(23,'2019-03-17 14:48:51.370898',3,1),(24,'2019-03-17 14:49:31.477996',3,1),(25,'2019-03-17 14:49:44.516150',3,1),(26,'2019-03-17 14:50:08.397491',3,1),(27,'2019-03-17 14:51:09.313196',3,1),(28,'2019-03-17 14:51:19.010561',3,1),(29,'2019-03-17 14:51:24.298277',3,1),(30,'2019-03-17 14:52:23.118477',3,1),(31,'2019-03-17 14:52:28.087129',3,1),(32,'2019-03-17 15:07:38.300307',3,1),(33,'2019-03-17 15:07:44.350318',3,1),(34,'2019-03-17 15:07:53.333196',3,1),(35,'2019-03-17 15:16:51.697255',3,1),(36,'2019-03-17 15:34:41.082684',3,1),(37,'2019-03-17 15:37:29.381195',3,1),(38,'2019-03-17 15:37:33.908315',3,1),(39,'2019-03-17 15:37:50.297050',3,1),(40,'2019-03-17 15:37:54.579166',3,1),(41,'2019-03-17 15:40:16.300445',3,1),(42,'2019-03-17 15:40:21.977112',3,1),(43,'2019-03-17 15:41:53.171776',3,1),(44,'2019-03-17 15:41:58.521649',3,1),(45,'2019-03-18 00:59:57.002202',3,1),(46,'2019-03-18 01:00:06.540583',3,1),(47,'2019-03-18 01:14:15.878446',3,1),(48,'2019-03-18 01:14:25.449047',3,1),(49,'2019-03-18 01:14:33.172000',3,1),(50,'2019-03-18 01:14:37.419036',3,1),(51,'2019-03-18 01:14:46.506176',3,1),(52,'2019-03-18 01:14:56.690916',3,1),(53,'2019-03-18 01:26:33.861497',3,1),(54,'2019-03-18 02:41:23.583059',3,1),(55,'2019-03-18 02:51:27.412407',3,1),(56,'2019-03-18 02:53:59.436899',3,1),(57,'2019-03-18 02:54:13.364038',3,1),(58,'2019-03-18 02:59:34.672713',3,1),(59,'2019-03-18 03:00:34.286294',3,1),(60,'2019-03-18 03:00:44.022153',3,1),(61,'2019-03-18 03:02:24.506636',3,1),(62,'2019-03-18 03:03:59.419214',3,1),(63,'2019-03-18 03:04:39.113674',3,1),(64,'2019-03-18 03:04:48.787384',3,1),(65,'2019-03-18 03:06:40.737059',3,1),(66,'2019-03-18 03:06:45.654521',3,1),(67,'2019-03-18 03:06:48.587749',3,1),(68,'2019-03-18 03:07:06.892566',3,1),(69,'2019-03-18 03:07:13.317967',3,1),(70,'2019-03-18 03:11:26.415989',3,1),(71,'2019-03-18 03:14:31.602491',3,1),(72,'2019-03-18 03:15:56.196973',3,1),(73,'2019-03-18 03:16:20.646150',3,1),(74,'2019-03-18 03:17:50.540858',3,1),(75,'2019-03-18 03:17:55.327971',3,1),(76,'2019-03-18 03:17:58.697668',3,1),(77,'2019-03-18 03:18:10.153799',3,1),(78,'2019-03-18 03:27:46.781425',3,1),(79,'2019-03-18 03:28:14.562268',3,1),(80,'2019-03-18 03:42:57.606810',3,1),(81,'2019-03-18 03:43:34.134466',3,1),(82,'2019-03-18 03:43:42.363522',3,1),(83,'2019-03-18 03:43:49.596723',3,1),(84,'2019-03-18 03:43:54.705253',3,1),(85,'2019-03-18 03:43:59.539448',3,1),(86,'2019-03-18 03:45:11.167569',3,1),(87,'2019-03-18 03:45:14.185169',3,1),(88,'2019-03-18 03:45:20.550670',3,1),(89,'2019-03-18 03:46:11.075939',3,1),(90,'2019-03-18 03:46:19.992291',3,1),(91,'2019-03-18 03:47:43.294580',3,1),(92,'2019-03-18 03:47:47.544892',3,1),(93,'2019-03-18 03:48:26.071365',3,1),(94,'2019-03-18 03:48:37.123387',3,1),(95,'2019-03-18 04:36:20.675157',3,1),(96,'2019-03-18 04:53:52.525009',3,1),(97,'2019-03-18 04:54:09.420515',3,1),(98,'2019-03-18 04:54:12.656299',3,1),(99,'2019-03-18 06:16:10.792149',3,1),(100,'2019-03-18 06:17:04.175597',3,1),(101,'2019-03-18 06:34:51.818118',3,1),(102,'2019-03-18 06:34:58.360714',3,1),(103,'2019-03-18 06:42:25.073913',3,1),(104,'2019-03-18 06:48:42.250781',3,1),(105,'2019-03-18 07:41:01.740278',3,1),(106,'2019-03-18 07:41:38.990916',3,1),(107,'2019-03-18 07:45:43.589284',3,1),(108,'2019-03-18 07:46:21.335686',3,1),(109,'2019-03-18 07:46:39.544323',3,1),(110,'2019-03-18 07:48:24.892693',3,1),(111,'2019-03-18 07:58:49.108631',3,1),(112,'2019-03-18 07:58:54.402474',3,1),(113,'2019-03-18 08:04:00.753632',3,1),(114,'2019-03-18 08:04:04.983214',3,1),(115,'2019-03-18 08:11:31.120751',3,1),(116,'2019-03-18 08:12:03.764934',3,1),(117,'2019-03-18 08:13:34.680422',3,1),(118,'2019-03-18 08:14:30.354280',3,1),(119,'2019-03-18 08:15:17.323212',3,1),(120,'2019-03-18 08:22:54.940164',3,1),(121,'2019-03-18 08:23:10.286512',3,1),(122,'2019-03-18 08:27:33.049220',3,1),(123,'2019-03-18 10:43:35.060491',3,1),(124,'2019-03-18 14:52:01.183560',3,1),(125,'2019-03-18 14:52:09.251739',3,1),(126,'2019-03-18 14:52:20.790156',3,1),(127,'2019-03-18 14:59:06.365403',3,1),(128,'2019-03-18 15:13:25.225793',3,1),(129,'2019-03-18 15:13:32.121225',3,1),(130,'2019-03-18 15:13:37.844857',3,1),(131,'2019-03-18 15:13:42.836454',3,1),(132,'2019-03-18 15:13:47.266968',3,1),(133,'2019-03-18 15:13:51.652852',3,1),(134,'2019-03-18 15:13:55.791455',3,1),(135,'2019-03-19 02:33:07.012624',3,1),(136,'2019-03-19 02:33:19.476944',3,1),(137,'2019-03-19 02:41:06.783946',3,1),(138,'2019-03-19 03:35:06.294156',3,1),(139,'2019-03-19 03:35:47.949066',3,1),(140,'2019-03-19 03:38:16.368056',3,1),(141,'2019-03-19 03:38:20.069204',3,1),(142,'2019-03-19 03:43:27.867208',3,1),(143,'2019-03-19 03:43:31.343160',3,1),(144,'2019-03-19 03:44:44.417664',3,1),(145,'2019-03-19 03:44:48.108024',3,1),(146,'2019-03-19 08:41:06.701462',3,1),(147,'2019-03-19 08:58:22.035046',3,1),(148,'2019-03-19 08:58:29.681083',3,1),(149,'2019-03-19 10:22:26.362949',3,1),(150,'2019-03-19 10:22:48.309312',3,1),(151,'2019-03-19 10:41:44.826691',3,1),(152,'2019-03-19 12:44:32.754214',3,1),(153,'2019-03-19 12:44:42.171562',3,1),(154,'2019-03-19 13:07:31.232968',3,1),(155,'2019-03-19 13:07:31.934100',3,1),(156,'2019-03-19 13:07:34.313230',3,1),(157,'2019-03-19 13:11:10.105977',3,1),(158,'2019-03-19 15:36:30.917630',3,1),(159,'2019-03-19 15:50:24.633026',3,1),(160,'2019-03-20 01:33:07.754960',3,1),(161,'2019-03-20 01:33:17.107268',3,1),(162,'2019-03-20 01:33:34.817028',3,1),(163,'2019-03-20 03:13:40.977571',3,1),(164,'2019-03-20 03:13:56.875619',3,1),(165,'2019-03-20 05:52:45.580299',3,1),(166,'2019-03-20 05:52:53.997780',3,1),(167,'2019-03-20 05:53:03.826324',3,1),(168,'2019-03-20 05:56:25.156160',3,1),(169,'2019-03-22 02:06:56.904467',3,1),(170,'2019-03-27 10:41:57.594845',3,1),(171,'2019-03-27 12:20:14.883763',3,1),(172,'2019-03-27 12:20:24.764743',3,1),(173,'2019-03-27 12:20:39.245940',3,1),(174,'2019-03-27 12:20:55.020257',3,1),(175,'2019-03-27 12:21:10.572602',3,1),(176,'2019-03-27 12:23:58.452879',3,1),(177,'2019-03-27 12:24:07.536867',3,1),(178,'2019-03-27 12:25:20.035715',3,1),(179,'2019-03-27 12:25:48.148155',3,1),(180,'2019-03-27 13:14:12.944573',3,1),(181,'2019-03-27 14:06:52.767675',3,1),(182,'2019-03-27 14:10:22.875844',3,1),(183,'2019-03-27 14:11:23.988592',3,1),(184,'2019-03-27 14:11:47.583244',3,1),(185,'2019-03-28 01:35:02.578950',3,1),(186,'2019-03-28 01:38:53.250447',3,1),(187,'2019-03-31 06:15:51.066321',3,1),(188,'2019-03-31 06:17:07.827992',3,1),(189,'2019-03-31 06:17:13.252415',3,1),(190,'2019-03-31 06:30:25.846028',3,1),(191,'2019-03-31 06:30:35.614493',3,1),(192,'2019-03-31 06:31:00.291163',3,1),(193,'2019-04-01 00:29:12.710092',3,1),(194,'2019-04-01 00:29:21.166236',3,1),(195,'2019-04-01 09:49:53.841989',3,1),(196,'2019-04-01 09:49:59.206180',3,1),(197,'2019-04-01 10:50:12.933721',3,1),(198,'2019-04-01 13:43:21.307081',3,1),(199,'2019-04-01 13:43:25.695761',3,1),(200,'2019-04-01 13:50:11.528996',3,1),(201,'2019-04-01 13:50:21.973485',3,1),(202,'2019-04-01 14:00:16.836887',3,1),(203,'2019-04-01 14:00:20.936617',3,1),(204,'2019-04-01 14:21:54.022041',3,1),(205,'2019-04-01 23:33:40.783264',3,1),(206,'2019-04-01 23:34:32.035154',3,1),(207,'2019-04-01 23:35:44.547981',3,1),(208,'2019-04-01 23:35:51.051557',3,1),(209,'2019-04-01 23:36:00.592386',3,1),(210,'2019-04-01 23:36:05.010909',3,1),(211,'2019-04-01 23:36:13.485149',3,1),(212,'2019-04-01 23:41:56.326584',3,1),(213,'2019-04-01 23:42:05.701521',3,1),(214,'2019-04-01 23:45:36.117930',3,1),(215,'2019-04-01 23:45:42.147507',3,1),(216,'2019-04-04 03:25:38.108631',3,1),(217,'2019-04-04 07:11:18.835880',3,1),(218,'2019-04-04 07:11:36.737355',3,1),(219,'2019-04-04 07:11:49.003640',3,1),(220,'2019-04-04 07:26:31.059564',3,1),(221,'2019-04-05 12:48:46.827001',3,1),(222,'2019-04-05 12:48:52.170728',3,1),(223,'2019-04-05 12:52:12.448220',3,1),(224,'2019-04-05 12:52:55.564322',3,1),(225,'2019-04-06 06:55:44.002944',3,1),(226,'2019-04-06 11:49:11.993596',3,1),(227,'2019-04-06 11:49:22.483328',3,1),(228,'2019-04-06 11:54:10.028845',3,1),(229,'2019-04-06 12:19:31.505472',3,1),(230,'2019-04-13 01:25:39.313179',3,1),(231,'2019-04-13 07:12:03.390651',3,1);
/*!40000 ALTER TABLE `analytics_userproductview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analytics_userrecord`
--

DROP TABLE IF EXISTS `analytics_userrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analytics_userrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num_product_views` int(10) unsigned NOT NULL,
  `num_basket_additions` int(10) unsigned NOT NULL,
  `num_orders` int(10) unsigned NOT NULL,
  `num_order_lines` int(10) unsigned NOT NULL,
  `num_order_items` int(10) unsigned NOT NULL,
  `total_spent` decimal(12,2) NOT NULL,
  `date_last_order` datetime(6) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `analytics_userrecord_num_orders_b352ffd1` (`num_orders`),
  KEY `analytics_userrecord_num_order_lines_97cc087f` (`num_order_lines`),
  KEY `analytics_userrecord_num_order_items_fb2a8304` (`num_order_items`),
  CONSTRAINT `analytics_userrecord_user_id_702cff4c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analytics_userrecord`
--

LOCK TABLES `analytics_userrecord` WRITE;
/*!40000 ALTER TABLE `analytics_userrecord` DISABLE KEYS */;
INSERT INTO `analytics_userrecord` VALUES (1,231,49,2,2,6,18000.00,'2019-04-01 14:03:25.860806',1);
/*!40000 ALTER TABLE `analytics_userrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analytics_usersearch`
--

DROP TABLE IF EXISTS `analytics_usersearch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analytics_usersearch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `query` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `analytics_usersearch_user_id_1775992d_fk_auth_user_id` (`user_id`),
  KEY `analytics_usersearch_query_ad36478b` (`query`),
  CONSTRAINT `analytics_usersearch_user_id_1775992d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analytics_usersearch`
--

LOCK TABLES `analytics_usersearch` WRITE;
/*!40000 ALTER TABLE `analytics_usersearch` DISABLE KEYS */;
INSERT INTO `analytics_usersearch` VALUES (1,'','2019-04-01 23:41:49.623593',1),(2,'e','2019-04-13 11:14:04.020083',1);
/*!40000 ALTER TABLE `analytics_usersearch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=357 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add captcha store',1,'add_captchastore'),(2,'Can change captcha store',1,'change_captchastore'),(3,'Can delete captcha store',1,'delete_captchastore'),(4,'Can add log entry',2,'add_logentry'),(5,'Can change log entry',2,'change_logentry'),(6,'Can delete log entry',2,'delete_logentry'),(7,'Can add permission',3,'add_permission'),(8,'Can change permission',3,'change_permission'),(9,'Can delete permission',3,'delete_permission'),(10,'Can add group',4,'add_group'),(11,'Can change group',4,'change_group'),(12,'Can delete group',4,'delete_group'),(13,'Can add user',5,'add_user'),(14,'Can change user',5,'change_user'),(15,'Can delete user',5,'delete_user'),(16,'Can add content type',6,'add_contenttype'),(17,'Can change content type',6,'change_contenttype'),(18,'Can delete content type',6,'delete_contenttype'),(19,'Can add session',7,'add_session'),(20,'Can change session',7,'change_session'),(21,'Can delete session',7,'delete_session'),(22,'Can add site',8,'add_site'),(23,'Can change site',8,'change_site'),(24,'Can delete site',8,'delete_site'),(25,'Can add flat page',9,'add_flatpage'),(26,'Can change flat page',9,'change_flatpage'),(27,'Can delete flat page',9,'delete_flatpage'),(28,'Can add quant_policy',10,'add_quantpolicy'),(29,'Can change quant_policy',10,'change_quantpolicy'),(30,'Can delete quant_policy',10,'delete_quantpolicy'),(31,'Can view quant_policy',10,'view_quantpolicy'),(32,'Can add quant_policy_order',11,'add_quantpolicyorder'),(33,'Can change quant_policy_order',11,'change_quantpolicyorder'),(34,'Can delete quant_policy_order',11,'delete_quantpolicyorder'),(35,'Can view quant_policy_order',11,'view_quantpolicyorder'),(36,'Can add email address',12,'add_emailaddress'),(37,'Can change email address',12,'change_emailaddress'),(38,'Can delete email address',12,'delete_emailaddress'),(39,'Can add email confirmation',13,'add_emailconfirmation'),(40,'Can change email confirmation',13,'change_emailconfirmation'),(41,'Can delete email confirmation',13,'delete_emailconfirmation'),(42,'Can add social account',14,'add_socialaccount'),(43,'Can change social account',14,'change_socialaccount'),(44,'Can delete social account',14,'delete_socialaccount'),(45,'Can add social application',15,'add_socialapp'),(46,'Can change social application',15,'change_socialapp'),(47,'Can delete social application',15,'delete_socialapp'),(48,'Can add social application token',16,'add_socialtoken'),(49,'Can change social application token',16,'change_socialtoken'),(50,'Can delete social application token',16,'delete_socialtoken'),(51,'Can add crontab',17,'add_crontabschedule'),(52,'Can change crontab',17,'change_crontabschedule'),(53,'Can delete crontab',17,'delete_crontabschedule'),(54,'Can add interval',18,'add_intervalschedule'),(55,'Can change interval',18,'change_intervalschedule'),(56,'Can delete interval',18,'delete_intervalschedule'),(57,'Can add periodic task',19,'add_periodictask'),(58,'Can change periodic task',19,'change_periodictask'),(59,'Can delete periodic task',19,'delete_periodictask'),(60,'Can add periodic tasks',20,'add_periodictasks'),(61,'Can change periodic tasks',20,'change_periodictasks'),(62,'Can delete periodic tasks',20,'delete_periodictasks'),(63,'Can add solar event',21,'add_solarschedule'),(64,'Can change solar event',21,'change_solarschedule'),(65,'Can delete solar event',21,'delete_solarschedule'),(66,'Can add Product record',22,'add_productrecord'),(67,'Can change Product record',22,'change_productrecord'),(68,'Can delete Product record',22,'delete_productrecord'),(69,'Can add User product view',23,'add_userproductview'),(70,'Can change User product view',23,'change_userproductview'),(71,'Can delete User product view',23,'delete_userproductview'),(72,'Can add User record',24,'add_userrecord'),(73,'Can change User record',24,'change_userrecord'),(74,'Can delete User record',24,'delete_userrecord'),(75,'Can add User search query',25,'add_usersearch'),(76,'Can change User search query',25,'change_usersearch'),(77,'Can delete User search query',25,'delete_usersearch'),(78,'Can add Country',26,'add_country'),(79,'Can change Country',26,'change_country'),(80,'Can delete Country',26,'delete_country'),(81,'Can add User address',27,'add_useraddress'),(82,'Can change User address',27,'change_useraddress'),(83,'Can delete User address',27,'delete_useraddress'),(84,'Can add Order and Item Charge',28,'add_orderanditemcharges'),(85,'Can change Order and Item Charge',28,'change_orderanditemcharges'),(86,'Can delete Order and Item Charge',28,'delete_orderanditemcharges'),(87,'Can add Weight Band',29,'add_weightband'),(88,'Can change Weight Band',29,'change_weightband'),(89,'Can delete Weight Band',29,'delete_weightband'),(90,'Can add Weight-based Shipping Method',30,'add_weightbased'),(91,'Can change Weight-based Shipping Method',30,'change_weightbased'),(92,'Can delete Weight-based Shipping Method',30,'delete_weightbased'),(93,'Can add Attribute option',31,'add_attributeoption'),(94,'Can change Attribute option',31,'change_attributeoption'),(95,'Can delete Attribute option',31,'delete_attributeoption'),(96,'Can add Attribute option group',32,'add_attributeoptiongroup'),(97,'Can change Attribute option group',32,'change_attributeoptiongroup'),(98,'Can delete Attribute option group',32,'delete_attributeoptiongroup'),(99,'Can add Category',33,'add_category'),(100,'Can change Category',33,'change_category'),(101,'Can delete Category',33,'delete_category'),(102,'Can add Option',34,'add_option'),(103,'Can change Option',34,'change_option'),(104,'Can delete Option',34,'delete_option'),(105,'Can add Product',35,'add_product'),(106,'Can change Product',35,'change_product'),(107,'Can delete Product',35,'delete_product'),(108,'Can add Product attribute',36,'add_productattribute'),(109,'Can change Product attribute',36,'change_productattribute'),(110,'Can delete Product attribute',36,'delete_productattribute'),(111,'Can add Product attribute value',37,'add_productattributevalue'),(112,'Can change Product attribute value',37,'change_productattributevalue'),(113,'Can delete Product attribute value',37,'delete_productattributevalue'),(114,'Can add Product category',38,'add_productcategory'),(115,'Can change Product category',38,'change_productcategory'),(116,'Can delete Product category',38,'delete_productcategory'),(117,'Can add Product class',39,'add_productclass'),(118,'Can change Product class',39,'change_productclass'),(119,'Can delete Product class',39,'delete_productclass'),(120,'Can add Product image',40,'add_productimage'),(121,'Can change Product image',40,'change_productimage'),(122,'Can delete Product image',40,'delete_productimage'),(123,'Can add Product recommendation',41,'add_productrecommendation'),(124,'Can change Product recommendation',41,'change_productrecommendation'),(125,'Can delete Product recommendation',41,'delete_productrecommendation'),(126,'Can add Product review',42,'add_productreview'),(127,'Can change Product review',42,'change_productreview'),(128,'Can delete Product review',42,'delete_productreview'),(129,'Can add Vote',43,'add_vote'),(130,'Can change Vote',43,'change_vote'),(131,'Can delete Vote',43,'delete_vote'),(132,'Can add Fulfillment partner',44,'add_partner'),(133,'Can change Fulfillment partner',44,'change_partner'),(134,'Can delete Fulfillment partner',44,'delete_partner'),(135,'Can access dashboard',44,'dashboard_access'),(136,'Can add Partner address',45,'add_partneraddress'),(137,'Can change Partner address',45,'change_partneraddress'),(138,'Can delete Partner address',45,'delete_partneraddress'),(139,'Can add Stock alert',46,'add_stockalert'),(140,'Can change Stock alert',46,'change_stockalert'),(141,'Can delete Stock alert',46,'delete_stockalert'),(142,'Can add Stock record',47,'add_stockrecord'),(143,'Can change Stock record',47,'change_stockrecord'),(144,'Can delete Stock record',47,'delete_stockrecord'),(145,'Can add Basket',48,'add_basket'),(146,'Can change Basket',48,'change_basket'),(147,'Can delete Basket',48,'delete_basket'),(148,'Can add Basket line',49,'add_line'),(149,'Can change Basket line',49,'change_line'),(150,'Can delete Basket line',49,'delete_line'),(151,'Can add Line attribute',50,'add_lineattribute'),(152,'Can change Line attribute',50,'change_lineattribute'),(153,'Can delete Line attribute',50,'delete_lineattribute'),(154,'Can add Bankcard',51,'add_bankcard'),(155,'Can change Bankcard',51,'change_bankcard'),(156,'Can delete Bankcard',51,'delete_bankcard'),(157,'Can add Source',52,'add_source'),(158,'Can change Source',52,'change_source'),(159,'Can delete Source',52,'delete_source'),(160,'Can add Source Type',53,'add_sourcetype'),(161,'Can change Source Type',53,'change_sourcetype'),(162,'Can delete Source Type',53,'delete_sourcetype'),(163,'Can add Transaction',54,'add_transaction'),(164,'Can change Transaction',54,'change_transaction'),(165,'Can delete Transaction',54,'delete_transaction'),(166,'Can add Benefit',55,'add_benefit'),(167,'Can change Benefit',55,'change_benefit'),(168,'Can delete Benefit',55,'delete_benefit'),(169,'Can add Condition',56,'add_condition'),(170,'Can change Condition',56,'change_condition'),(171,'Can delete Condition',56,'delete_condition'),(172,'Can add Conditional offer',57,'add_conditionaloffer'),(173,'Can change Conditional offer',57,'change_conditionaloffer'),(174,'Can delete Conditional offer',57,'delete_conditionaloffer'),(175,'Can add Range',58,'add_range'),(176,'Can change Range',58,'change_range'),(177,'Can delete Range',58,'delete_range'),(178,'Can add range product',59,'add_rangeproduct'),(179,'Can change range product',59,'change_rangeproduct'),(180,'Can delete range product',59,'delete_rangeproduct'),(181,'Can add Range Product Uploaded File',60,'add_rangeproductfileupload'),(182,'Can change Range Product Uploaded File',60,'change_rangeproductfileupload'),(183,'Can delete Range Product Uploaded File',60,'delete_rangeproductfileupload'),(184,'Can add Absolute discount benefit',55,'add_absolutediscountbenefit'),(185,'Can change Absolute discount benefit',55,'change_absolutediscountbenefit'),(186,'Can delete Absolute discount benefit',55,'delete_absolutediscountbenefit'),(187,'Can add Count condition',56,'add_countcondition'),(188,'Can change Count condition',56,'change_countcondition'),(189,'Can delete Count condition',56,'delete_countcondition'),(190,'Can add Coverage Condition',56,'add_coveragecondition'),(191,'Can change Coverage Condition',56,'change_coveragecondition'),(192,'Can delete Coverage Condition',56,'delete_coveragecondition'),(193,'Can add Fixed price benefit',55,'add_fixedpricebenefit'),(194,'Can change Fixed price benefit',55,'change_fixedpricebenefit'),(195,'Can delete Fixed price benefit',55,'delete_fixedpricebenefit'),(196,'Can add Multibuy discount benefit',55,'add_multibuydiscountbenefit'),(197,'Can change Multibuy discount benefit',55,'change_multibuydiscountbenefit'),(198,'Can delete Multibuy discount benefit',55,'delete_multibuydiscountbenefit'),(199,'Can add Percentage discount benefit',55,'add_percentagediscountbenefit'),(200,'Can change Percentage discount benefit',55,'change_percentagediscountbenefit'),(201,'Can delete Percentage discount benefit',55,'delete_percentagediscountbenefit'),(202,'Can add shipping benefit',55,'add_shippingbenefit'),(203,'Can change shipping benefit',55,'change_shippingbenefit'),(204,'Can delete shipping benefit',55,'delete_shippingbenefit'),(205,'Can add Shipping absolute discount benefit',55,'add_shippingabsolutediscountbenefit'),(206,'Can change Shipping absolute discount benefit',55,'change_shippingabsolutediscountbenefit'),(207,'Can delete Shipping absolute discount benefit',55,'delete_shippingabsolutediscountbenefit'),(208,'Can add Fixed price shipping benefit',55,'add_shippingfixedpricebenefit'),(209,'Can change Fixed price shipping benefit',55,'change_shippingfixedpricebenefit'),(210,'Can delete Fixed price shipping benefit',55,'delete_shippingfixedpricebenefit'),(211,'Can add Shipping percentage discount benefit',55,'add_shippingpercentagediscountbenefit'),(212,'Can change Shipping percentage discount benefit',55,'change_shippingpercentagediscountbenefit'),(213,'Can delete Shipping percentage discount benefit',55,'delete_shippingpercentagediscountbenefit'),(214,'Can add Value condition',56,'add_valuecondition'),(215,'Can change Value condition',56,'change_valuecondition'),(216,'Can delete Value condition',56,'delete_valuecondition'),(217,'Can add Billing address',72,'add_billingaddress'),(218,'Can change Billing address',72,'change_billingaddress'),(219,'Can delete Billing address',72,'delete_billingaddress'),(220,'Can add Communication Event',73,'add_communicationevent'),(221,'Can change Communication Event',73,'change_communicationevent'),(222,'Can delete Communication Event',73,'delete_communicationevent'),(223,'Can add Order Line',74,'add_line'),(224,'Can change Order Line',74,'change_line'),(225,'Can delete Order Line',74,'delete_line'),(226,'Can add Line Attribute',75,'add_lineattribute'),(227,'Can change Line Attribute',75,'change_lineattribute'),(228,'Can delete Line Attribute',75,'delete_lineattribute'),(229,'Can add Line Price',76,'add_lineprice'),(230,'Can change Line Price',76,'change_lineprice'),(231,'Can delete Line Price',76,'delete_lineprice'),(232,'Can add Order',77,'add_order'),(233,'Can change Order',77,'change_order'),(234,'Can delete Order',77,'delete_order'),(235,'Can add Order Discount',78,'add_orderdiscount'),(236,'Can change Order Discount',78,'change_orderdiscount'),(237,'Can delete Order Discount',78,'delete_orderdiscount'),(238,'Can add Order Note',79,'add_ordernote'),(239,'Can change Order Note',79,'change_ordernote'),(240,'Can delete Order Note',79,'delete_ordernote'),(241,'Can add Payment Event',80,'add_paymentevent'),(242,'Can change Payment Event',80,'change_paymentevent'),(243,'Can delete Payment Event',80,'delete_paymentevent'),(244,'Can add Payment Event Quantity',81,'add_paymenteventquantity'),(245,'Can change Payment Event Quantity',81,'change_paymenteventquantity'),(246,'Can delete Payment Event Quantity',81,'delete_paymenteventquantity'),(247,'Can add Payment Event Type',82,'add_paymenteventtype'),(248,'Can change Payment Event Type',82,'change_paymenteventtype'),(249,'Can delete Payment Event Type',82,'delete_paymenteventtype'),(250,'Can add Shipping address',83,'add_shippingaddress'),(251,'Can change Shipping address',83,'change_shippingaddress'),(252,'Can delete Shipping address',83,'delete_shippingaddress'),(253,'Can add Shipping Event',84,'add_shippingevent'),(254,'Can change Shipping Event',84,'change_shippingevent'),(255,'Can delete Shipping Event',84,'delete_shippingevent'),(256,'Can add Shipping Event Quantity',85,'add_shippingeventquantity'),(257,'Can change Shipping Event Quantity',85,'change_shippingeventquantity'),(258,'Can delete Shipping Event Quantity',85,'delete_shippingeventquantity'),(259,'Can add Shipping Event Type',86,'add_shippingeventtype'),(260,'Can change Shipping Event Type',86,'change_shippingeventtype'),(261,'Can delete Shipping Event Type',86,'delete_shippingeventtype'),(262,'Can add Communication event type',87,'add_communicationeventtype'),(263,'Can change Communication event type',87,'change_communicationeventtype'),(264,'Can delete Communication event type',87,'delete_communicationeventtype'),(265,'Can add Email',88,'add_email'),(266,'Can change Email',88,'change_email'),(267,'Can delete Email',88,'delete_email'),(268,'Can add Notification',89,'add_notification'),(269,'Can change Notification',89,'change_notification'),(270,'Can delete Notification',89,'delete_notification'),(271,'Can add Product alert',90,'add_productalert'),(272,'Can change Product alert',90,'change_productalert'),(273,'Can delete Product alert',90,'delete_productalert'),(274,'Can add Automatic product list',91,'add_automaticproductlist'),(275,'Can change Automatic product list',91,'change_automaticproductlist'),(276,'Can delete Automatic product list',91,'delete_automaticproductlist'),(277,'Can add Hand Picked Product List',92,'add_handpickedproductlist'),(278,'Can change Hand Picked Product List',92,'change_handpickedproductlist'),(279,'Can delete Hand Picked Product List',92,'delete_handpickedproductlist'),(280,'Can add Image',93,'add_image'),(281,'Can change Image',93,'change_image'),(282,'Can delete Image',93,'delete_image'),(283,'Can add Keyword Promotion',94,'add_keywordpromotion'),(284,'Can change Keyword Promotion',94,'change_keywordpromotion'),(285,'Can delete Keyword Promotion',94,'delete_keywordpromotion'),(286,'Can add Multi Image',95,'add_multiimage'),(287,'Can change Multi Image',95,'change_multiimage'),(288,'Can delete Multi Image',95,'delete_multiimage'),(289,'Can add Ordered product',96,'add_orderedproduct'),(290,'Can change Ordered product',96,'change_orderedproduct'),(291,'Can delete Ordered product',96,'delete_orderedproduct'),(292,'Can add Ordered Product List',97,'add_orderedproductlist'),(293,'Can change Ordered Product List',97,'change_orderedproductlist'),(294,'Can delete Ordered Product List',97,'delete_orderedproductlist'),(295,'Can add Page Promotion',98,'add_pagepromotion'),(296,'Can change Page Promotion',98,'change_pagepromotion'),(297,'Can delete Page Promotion',98,'delete_pagepromotion'),(298,'Can add Raw HTML',99,'add_rawhtml'),(299,'Can change Raw HTML',99,'change_rawhtml'),(300,'Can delete Raw HTML',99,'delete_rawhtml'),(301,'Can add Single product',100,'add_singleproduct'),(302,'Can change Single product',100,'change_singleproduct'),(303,'Can delete Single product',100,'delete_singleproduct'),(304,'Can add Tabbed Block',101,'add_tabbedblock'),(305,'Can change Tabbed Block',101,'change_tabbedblock'),(306,'Can delete Tabbed Block',101,'delete_tabbedblock'),(307,'Can add Voucher',102,'add_voucher'),(308,'Can change Voucher',102,'change_voucher'),(309,'Can delete Voucher',102,'delete_voucher'),(310,'Can add Voucher Application',103,'add_voucherapplication'),(311,'Can change Voucher Application',103,'change_voucherapplication'),(312,'Can delete Voucher Application',103,'delete_voucherapplication'),(313,'Can add VoucherSet',104,'add_voucherset'),(314,'Can change VoucherSet',104,'change_voucherset'),(315,'Can delete VoucherSet',104,'delete_voucherset'),(316,'Can add Wish list line',105,'add_line'),(317,'Can change Wish list line',105,'change_line'),(318,'Can delete Wish list line',105,'delete_line'),(319,'Can add Wish List',106,'add_wishlist'),(320,'Can change Wish List',106,'change_wishlist'),(321,'Can delete Wish List',106,'delete_wishlist'),(322,'Can add kv store',107,'add_kvstore'),(323,'Can change kv store',107,'change_kvstore'),(324,'Can delete kv store',107,'delete_kvstore'),(325,'Can add account',108,'add_account'),(326,'Can change account',108,'change_account'),(327,'Can delete account',108,'delete_account'),(328,'Can add account type',109,'add_accounttype'),(329,'Can change account type',109,'change_accounttype'),(330,'Can delete account type',109,'delete_accounttype'),(331,'Can add IP address record',110,'add_ipaddressrecord'),(332,'Can change IP address record',110,'change_ipaddressrecord'),(333,'Can delete IP address record',110,'delete_ipaddressrecord'),(334,'Can add transaction',111,'add_transaction'),(335,'Can change transaction',111,'change_transaction'),(336,'Can delete transaction',111,'delete_transaction'),(337,'Can add transfer',112,'add_transfer'),(338,'Can change transfer',112,'change_transfer'),(339,'Can delete transfer',112,'delete_transfer'),(340,'Can add api key',113,'add_apikey'),(341,'Can change api key',113,'change_apikey'),(342,'Can delete api key',113,'delete_apikey'),(343,'Can add express transaction',114,'add_expresstransaction'),(344,'Can change express transaction',114,'change_expresstransaction'),(345,'Can delete express transaction',114,'delete_expresstransaction'),(346,'Can add payflow transaction',115,'add_payflowtransaction'),(347,'Can change payflow transaction',115,'change_payflowtransaction'),(348,'Can delete payflow transaction',115,'delete_payflowtransaction'),(349,'Can add 三角策略',116,'add_sanjiaopolicy'),(350,'Can change 三角策略',116,'change_sanjiaopolicy'),(351,'Can delete 三角策略',116,'delete_sanjiaopolicy'),(352,'Can view 三角策略',116,'view_sanjiaopolicy'),(353,'Can add 对敲策略',117,'add_duiqiaopolicy'),(354,'Can change 对敲策略',117,'change_duiqiaopolicy'),(355,'Can delete 对敲策略',117,'delete_duiqiaopolicy'),(356,'Can view 对敲策略',117,'view_duiqiaopolicy');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$36000$AhApnOebfhag$Uw3SFhj8ML6LyY+tyUaxmCAfLvE2eFKHd+JHzZe4W8A=','2019-03-27 07:07:07.303090',1,'foonsun','','','andyjoe318@gmail.com',1,1,'2019-03-17 12:53:55.848925');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `basket_basket`
--

DROP TABLE IF EXISTS `basket_basket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basket_basket` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_merged` datetime(6) DEFAULT NULL,
  `date_submitted` datetime(6) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `basket_basket_owner_id_3a018de5_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `basket_basket_owner_id_3a018de5_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `basket_basket`
--

LOCK TABLES `basket_basket` WRITE;
/*!40000 ALTER TABLE `basket_basket` DISABLE KEYS */;
INSERT INTO `basket_basket` VALUES (1,'Frozen','2019-03-17 12:54:33.285753',NULL,NULL,1),(2,'Merged','2019-03-18 10:12:24.195233','2019-03-18 10:12:42.105206',NULL,NULL),(3,'Frozen','2019-03-19 07:53:41.813580',NULL,NULL,1),(4,'Frozen','2019-03-19 08:40:45.930861',NULL,NULL,1),(5,'Frozen','2019-03-19 10:22:14.774130',NULL,NULL,1),(6,'Frozen','2019-03-19 10:41:31.644252',NULL,NULL,1),(7,'Frozen','2019-03-20 01:34:11.947375',NULL,NULL,1),(8,'Merged','2019-03-27 07:06:56.016561','2019-03-27 07:07:07.451253',NULL,NULL),(9,'Submitted','2019-03-27 07:07:19.149927',NULL,'2019-03-28 00:59:26.164430',1),(10,'Merged','2019-03-27 14:58:50.135134','2019-03-27 14:59:13.591174',NULL,1),(11,'Frozen','2019-03-28 01:07:07.201110',NULL,NULL,1),(12,'Frozen','2019-03-28 01:17:27.993249',NULL,NULL,1),(13,'Submitted','2019-03-31 09:37:14.345051',NULL,'2019-04-01 14:03:26.098435',1),(14,'Open','2019-04-01 14:03:42.652758',NULL,NULL,1);
/*!40000 ALTER TABLE `basket_basket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `basket_basket_vouchers`
--

DROP TABLE IF EXISTS `basket_basket_vouchers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basket_basket_vouchers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basket_id` int(11) NOT NULL,
  `voucher_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `basket_basket_vouchers_basket_id_voucher_id_0731eee2_uniq` (`basket_id`,`voucher_id`),
  KEY `basket_basket_vouchers_voucher_id_c2b66981_fk_voucher_voucher_id` (`voucher_id`),
  CONSTRAINT `basket_basket_vouchers_basket_id_f857c2f8_fk_basket_basket_id` FOREIGN KEY (`basket_id`) REFERENCES `basket_basket` (`id`),
  CONSTRAINT `basket_basket_vouchers_voucher_id_c2b66981_fk_voucher_voucher_id` FOREIGN KEY (`voucher_id`) REFERENCES `voucher_voucher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `basket_basket_vouchers`
--

LOCK TABLES `basket_basket_vouchers` WRITE;
/*!40000 ALTER TABLE `basket_basket_vouchers` DISABLE KEYS */;
/*!40000 ALTER TABLE `basket_basket_vouchers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `basket_line`
--

DROP TABLE IF EXISTS `basket_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basket_line` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `line_reference` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `quantity` int(10) unsigned NOT NULL,
  `price_currency` varchar(12) COLLATE utf8_unicode_ci NOT NULL,
  `price_excl_tax` decimal(12,2) DEFAULT NULL,
  `price_incl_tax` decimal(12,2) DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  `basket_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `stockrecord_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `basket_line_basket_id_line_reference_8977e974_uniq` (`basket_id`,`line_reference`),
  KEY `basket_line_line_reference_08e91113` (`line_reference`),
  KEY `basket_line_product_id_303d743e_fk_catalogue_product_id` (`product_id`),
  KEY `basket_line_stockrecord_id_7039d8a4_fk_partner_stockrecord_id` (`stockrecord_id`),
  CONSTRAINT `basket_line_basket_id_b615c905_fk_basket_basket_id` FOREIGN KEY (`basket_id`) REFERENCES `basket_basket` (`id`),
  CONSTRAINT `basket_line_product_id_303d743e_fk_catalogue_product_id` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`),
  CONSTRAINT `basket_line_stockrecord_id_7039d8a4_fk_partner_stockrecord_id` FOREIGN KEY (`stockrecord_id`) REFERENCES `partner_stockrecord` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `basket_line`
--

LOCK TABLES `basket_line` WRITE;
/*!40000 ALTER TABLE `basket_line` DISABLE KEYS */;
INSERT INTO `basket_line` VALUES (3,'3_1',10,'RMB',3000.00,3000.00,'2019-03-18 03:45:13.967255',1,3,1),(5,'3_1',1,'RMB',3000.00,3000.00,'2019-03-19 07:53:52.975477',3,3,1),(6,'3_1',2,'RMB',3000.00,3000.00,'2019-03-19 08:40:55.091997',4,3,1),(7,'3_1',1,'RMB',3000.00,3000.00,'2019-03-19 10:22:48.075244',5,3,1),(8,'3_1',2,'RMB',3000.00,3000.00,'2019-03-19 10:42:11.126074',6,3,1),(9,'3_1',1,'RMB',3000.00,3000.00,'2019-03-27 07:06:56.094837',7,3,1),(10,'3_1',1,'RMB',3000.00,3000.00,'2019-03-27 09:54:45.923486',9,3,1),(11,'3_1',1,'RMB',3000.00,3000.00,'2019-03-28 01:07:14.949997',11,3,1),(12,'3_1',4,'RMB',3000.00,3000.00,'2019-03-28 01:17:37.181056',12,3,1),(13,'3_1',5,'RMB',3000.00,3000.00,'2019-03-31 10:39:11.099145',13,3,1),(14,'3_1',1,'RMB',3000.00,3000.00,'2019-04-05 12:48:51.598494',14,3,1);
/*!40000 ALTER TABLE `basket_line` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `basket_lineattribute`
--

DROP TABLE IF EXISTS `basket_lineattribute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basket_lineattribute` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line_id` int(11) NOT NULL,
  `option_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `basket_lineattribute_line_id_c41e0cdf_fk_basket_line_id` (`line_id`),
  KEY `basket_lineattribute_option_id_9387a3f7_fk_catalogue_option_id` (`option_id`),
  CONSTRAINT `basket_lineattribute_line_id_c41e0cdf_fk_basket_line_id` FOREIGN KEY (`line_id`) REFERENCES `basket_line` (`id`),
  CONSTRAINT `basket_lineattribute_option_id_9387a3f7_fk_catalogue_option_id` FOREIGN KEY (`option_id`) REFERENCES `catalogue_option` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `basket_lineattribute`
--

LOCK TABLES `basket_lineattribute` WRITE;
/*!40000 ALTER TABLE `basket_lineattribute` DISABLE KEYS */;
/*!40000 ALTER TABLE `basket_lineattribute` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `captcha_captchastore`
--

DROP TABLE IF EXISTS `captcha_captchastore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `captcha_captchastore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `response` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `hashkey` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `expiration` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashkey` (`hashkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `captcha_captchastore`
--

LOCK TABLES `captcha_captchastore` WRITE;
/*!40000 ALTER TABLE `captcha_captchastore` DISABLE KEYS */;
/*!40000 ALTER TABLE `captcha_captchastore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_attributeoption`
--

DROP TABLE IF EXISTS `catalogue_attributeoption`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_attributeoption` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `option` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `catalogue_attributeoption_group_id_option_7a8f6c11_uniq` (`group_id`,`option`),
  CONSTRAINT `catalogue_attributeo_group_id_3d4a5e24_fk_catalogue` FOREIGN KEY (`group_id`) REFERENCES `catalogue_attributeoptiongroup` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_attributeoption`
--

LOCK TABLES `catalogue_attributeoption` WRITE;
/*!40000 ALTER TABLE `catalogue_attributeoption` DISABLE KEYS */;
/*!40000 ALTER TABLE `catalogue_attributeoption` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_attributeoptiongroup`
--

DROP TABLE IF EXISTS `catalogue_attributeoptiongroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_attributeoptiongroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_attributeoptiongroup`
--

LOCK TABLES `catalogue_attributeoptiongroup` WRITE;
/*!40000 ALTER TABLE `catalogue_attributeoptiongroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `catalogue_attributeoptiongroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_category`
--

DROP TABLE IF EXISTS `catalogue_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `depth` int(10) unsigned NOT NULL,
  `numchild` int(10) unsigned NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `image` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `slug` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path` (`path`),
  KEY `catalogue_category_name_1f342ac2` (`name`),
  KEY `catalogue_category_slug_9635febd` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_category`
--

LOCK TABLES `catalogue_category` WRITE;
/*!40000 ALTER TABLE `catalogue_category` DISABLE KEYS */;
INSERT INTO `catalogue_category` VALUES (1,'0001',1,0,'量化策略','','','u91cfu5316u7b56u7565');
/*!40000 ALTER TABLE `catalogue_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_option`
--

DROP TABLE IF EXISTS `catalogue_option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_option` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_option`
--

LOCK TABLES `catalogue_option` WRITE;
/*!40000 ALTER TABLE `catalogue_option` DISABLE KEYS */;
/*!40000 ALTER TABLE `catalogue_option` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_product`
--

DROP TABLE IF EXISTS `catalogue_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `structure` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `upc` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `slug` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `rating` double DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `is_discountable` tinyint(1) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `product_class_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `upc` (`upc`),
  KEY `catalogue_product_slug_c8e2e2b9` (`slug`),
  KEY `catalogue_product_date_updated_d3a1785d` (`date_updated`),
  KEY `catalogue_product_parent_id_9bfd2382_fk_catalogue_product_id` (`parent_id`),
  KEY `catalogue_product_product_class_id_0c6c5b54_fk_catalogue` (`product_class_id`),
  CONSTRAINT `catalogue_product_parent_id_9bfd2382_fk_catalogue_product_id` FOREIGN KEY (`parent_id`) REFERENCES `catalogue_product` (`id`),
  CONSTRAINT `catalogue_product_product_class_id_0c6c5b54_fk_catalogue` FOREIGN KEY (`product_class_id`) REFERENCES `catalogue_productclass` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_product`
--

LOCK TABLES `catalogue_product` WRITE;
/*!40000 ALTER TABLE `catalogue_product` DISABLE KEYS */;
INSERT INTO `catalogue_product` VALUES (3,'standalone','1','经典对敲挖矿交易策略','u7ecfu5178u5bf9u6572u6316u77ffu4ea4u6613u7b56u7565','<p>经典对敲挖矿交易策略，买一卖一同时进行。</p>',4,'2019-03-17 13:01:35.542400','2019-03-18 03:07:02.494283',1,NULL,1);
/*!40000 ALTER TABLE `catalogue_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_product_product_options`
--

DROP TABLE IF EXISTS `catalogue_product_product_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_product_product_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `option_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `catalogue_product_produc_product_id_option_id_9b3abb31_uniq` (`product_id`,`option_id`),
  KEY `catalogue_product_pr_option_id_ff470e13_fk_catalogue` (`option_id`),
  CONSTRAINT `catalogue_product_pr_option_id_ff470e13_fk_catalogue` FOREIGN KEY (`option_id`) REFERENCES `catalogue_option` (`id`),
  CONSTRAINT `catalogue_product_pr_product_id_ad2b46bd_fk_catalogue` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_product_product_options`
--

LOCK TABLES `catalogue_product_product_options` WRITE;
/*!40000 ALTER TABLE `catalogue_product_product_options` DISABLE KEYS */;
/*!40000 ALTER TABLE `catalogue_product_product_options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_productattribute`
--

DROP TABLE IF EXISTS `catalogue_productattribute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_productattribute` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `required` tinyint(1) NOT NULL,
  `option_group_id` int(11) DEFAULT NULL,
  `product_class_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `catalogue_productattribute_code_9ffea293` (`code`),
  KEY `catalogue_productatt_product_class_id_7af808ec_fk_catalogue` (`product_class_id`),
  KEY `catalogue_productatt_option_group_id_6b422dc2_fk_catalogue` (`option_group_id`),
  CONSTRAINT `catalogue_productatt_option_group_id_6b422dc2_fk_catalogue` FOREIGN KEY (`option_group_id`) REFERENCES `catalogue_attributeoptiongroup` (`id`),
  CONSTRAINT `catalogue_productatt_product_class_id_7af808ec_fk_catalogue` FOREIGN KEY (`product_class_id`) REFERENCES `catalogue_productclass` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_productattribute`
--

LOCK TABLES `catalogue_productattribute` WRITE;
/*!40000 ALTER TABLE `catalogue_productattribute` DISABLE KEYS */;
INSERT INTO `catalogue_productattribute` VALUES (2,'月数','month','integer',1,NULL,1);
/*!40000 ALTER TABLE `catalogue_productattribute` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_productattributevalue`
--

DROP TABLE IF EXISTS `catalogue_productattributevalue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_productattributevalue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value_text` longtext COLLATE utf8_unicode_ci,
  `value_integer` int(11) DEFAULT NULL,
  `value_boolean` tinyint(1) DEFAULT NULL,
  `value_float` double DEFAULT NULL,
  `value_richtext` longtext COLLATE utf8_unicode_ci,
  `value_date` date DEFAULT NULL,
  `value_file` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `value_image` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `entity_object_id` int(10) unsigned DEFAULT NULL,
  `attribute_id` int(11) NOT NULL,
  `entity_content_type_id` int(11) DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  `value_option_id` int(11) DEFAULT NULL,
  `value_datetime` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `catalogue_productattribu_attribute_id_product_id_1e8e7112_uniq` (`attribute_id`,`product_id`),
  KEY `catalogue_productatt_entity_content_type__f7186ab5_fk_django_co` (`entity_content_type_id`),
  KEY `catalogue_productatt_product_id_a03cd90e_fk_catalogue` (`product_id`),
  KEY `catalogue_productatt_value_option_id_21026066_fk_catalogue` (`value_option_id`),
  CONSTRAINT `catalogue_productatt_attribute_id_0287c1e7_fk_catalogue` FOREIGN KEY (`attribute_id`) REFERENCES `catalogue_productattribute` (`id`),
  CONSTRAINT `catalogue_productatt_entity_content_type__f7186ab5_fk_django_co` FOREIGN KEY (`entity_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `catalogue_productatt_product_id_a03cd90e_fk_catalogue` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`),
  CONSTRAINT `catalogue_productatt_value_option_id_21026066_fk_catalogue` FOREIGN KEY (`value_option_id`) REFERENCES `catalogue_attributeoption` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_productattributevalue`
--

LOCK TABLES `catalogue_productattributevalue` WRITE;
/*!40000 ALTER TABLE `catalogue_productattributevalue` DISABLE KEYS */;
INSERT INTO `catalogue_productattributevalue` VALUES (4,NULL,1,NULL,NULL,NULL,NULL,'','',NULL,2,NULL,3,NULL,NULL);
/*!40000 ALTER TABLE `catalogue_productattributevalue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_productattributevalue_value_multi_option`
--

DROP TABLE IF EXISTS `catalogue_productattributevalue_value_multi_option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_productattributevalue_value_multi_option` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productattributevalue_id` int(11) NOT NULL,
  `attributeoption_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `catalogue_productattribu_productattributevalue_id_a1760824_uniq` (`productattributevalue_id`,`attributeoption_id`),
  KEY `catalogue_productatt_attributeoption_id_962b600b_fk_catalogue` (`attributeoption_id`),
  CONSTRAINT `catalogue_productatt_attributeoption_id_962b600b_fk_catalogue` FOREIGN KEY (`attributeoption_id`) REFERENCES `catalogue_attributeoption` (`id`),
  CONSTRAINT `catalogue_productatt_productattributevalu_9c7c031e_fk_catalogue` FOREIGN KEY (`productattributevalue_id`) REFERENCES `catalogue_productattributevalue` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_productattributevalue_value_multi_option`
--

LOCK TABLES `catalogue_productattributevalue_value_multi_option` WRITE;
/*!40000 ALTER TABLE `catalogue_productattributevalue_value_multi_option` DISABLE KEYS */;
/*!40000 ALTER TABLE `catalogue_productattributevalue_value_multi_option` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_productcategory`
--

DROP TABLE IF EXISTS `catalogue_productcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_productcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `catalogue_productcategory_product_id_category_id_8f0dbfe2_uniq` (`product_id`,`category_id`),
  KEY `catalogue_productcat_category_id_176db535_fk_catalogue` (`category_id`),
  CONSTRAINT `catalogue_productcat_category_id_176db535_fk_catalogue` FOREIGN KEY (`category_id`) REFERENCES `catalogue_category` (`id`),
  CONSTRAINT `catalogue_productcat_product_id_846a4061_fk_catalogue` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_productcategory`
--

LOCK TABLES `catalogue_productcategory` WRITE;
/*!40000 ALTER TABLE `catalogue_productcategory` DISABLE KEYS */;
INSERT INTO `catalogue_productcategory` VALUES (1,1,3);
/*!40000 ALTER TABLE `catalogue_productcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_productclass`
--

DROP TABLE IF EXISTS `catalogue_productclass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_productclass` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `slug` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `requires_shipping` tinyint(1) NOT NULL,
  `track_stock` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_productclass`
--

LOCK TABLES `catalogue_productclass` WRITE;
/*!40000 ALTER TABLE `catalogue_productclass` DISABLE KEYS */;
INSERT INTO `catalogue_productclass` VALUES (1,'量化策略','u91cfu5316u7b56u7565',0,0);
/*!40000 ALTER TABLE `catalogue_productclass` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_productclass_options`
--

DROP TABLE IF EXISTS `catalogue_productclass_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_productclass_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productclass_id` int(11) NOT NULL,
  `option_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `catalogue_productclass_o_productclass_id_option_i_2266c635_uniq` (`productclass_id`,`option_id`),
  KEY `catalogue_productcla_option_id_b099542c_fk_catalogue` (`option_id`),
  CONSTRAINT `catalogue_productcla_option_id_b099542c_fk_catalogue` FOREIGN KEY (`option_id`) REFERENCES `catalogue_option` (`id`),
  CONSTRAINT `catalogue_productcla_productclass_id_732df4c8_fk_catalogue` FOREIGN KEY (`productclass_id`) REFERENCES `catalogue_productclass` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_productclass_options`
--

LOCK TABLES `catalogue_productclass_options` WRITE;
/*!40000 ALTER TABLE `catalogue_productclass_options` DISABLE KEYS */;
/*!40000 ALTER TABLE `catalogue_productclass_options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_productimage`
--

DROP TABLE IF EXISTS `catalogue_productimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_productimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `original` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `caption` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `display_order` int(10) unsigned NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `catalogue_productimage_product_id_49474fe8` (`product_id`),
  CONSTRAINT `catalogue_productima_product_id_49474fe8_fk_catalogue` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_productimage`
--

LOCK TABLES `catalogue_productimage` WRITE;
/*!40000 ALTER TABLE `catalogue_productimage` DISABLE KEYS */;
INSERT INTO `catalogue_productimage` VALUES (1,'images/products/2019/03/duiqiao.gif','',0,'2019-03-17 13:01:35.582680',3);
/*!40000 ALTER TABLE `catalogue_productimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogue_productrecommendation`
--

DROP TABLE IF EXISTS `catalogue_productrecommendation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalogue_productrecommendation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ranking` smallint(5) unsigned NOT NULL,
  `primary_id` int(11) NOT NULL,
  `recommendation_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `catalogue_productrecomme_primary_id_recommendatio_da1fdf43_uniq` (`primary_id`,`recommendation_id`),
  KEY `catalogue_productrec_recommendation_id_daf8ae95_fk_catalogue` (`recommendation_id`),
  CONSTRAINT `catalogue_productrec_primary_id_6e51a55c_fk_catalogue` FOREIGN KEY (`primary_id`) REFERENCES `catalogue_product` (`id`),
  CONSTRAINT `catalogue_productrec_recommendation_id_daf8ae95_fk_catalogue` FOREIGN KEY (`recommendation_id`) REFERENCES `catalogue_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogue_productrecommendation`
--

LOCK TABLES `catalogue_productrecommendation` WRITE;
/*!40000 ALTER TABLE `catalogue_productrecommendation` DISABLE KEYS */;
/*!40000 ALTER TABLE `catalogue_productrecommendation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_communicationeventtype`
--

DROP TABLE IF EXISTS `customer_communicationeventtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_communicationeventtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `category` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `email_subject_template` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email_body_template` longtext COLLATE utf8_unicode_ci,
  `email_body_html_template` longtext COLLATE utf8_unicode_ci,
  `sms_template` varchar(170) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_communicationeventtype`
--

LOCK TABLES `customer_communicationeventtype` WRITE;
/*!40000 ALTER TABLE `customer_communicationeventtype` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_communicationeventtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_email`
--

DROP TABLE IF EXISTS `customer_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_email` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` longtext COLLATE utf8_unicode_ci NOT NULL,
  `body_text` longtext COLLATE utf8_unicode_ci NOT NULL,
  `body_html` longtext COLLATE utf8_unicode_ci NOT NULL,
  `date_sent` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `email` varchar(254) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_email_user_id_a69ad588_fk_auth_user_id` (`user_id`),
  CONSTRAINT `customer_email_user_id_a69ad588_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_email`
--

LOCK TABLES `customer_email` WRITE;
/*!40000 ALTER TABLE `customer_email` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_email` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_notification`
--

DROP TABLE IF EXISTS `customer_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `body` longtext COLLATE utf8_unicode_ci NOT NULL,
  `category` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `location` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `date_sent` datetime(6) NOT NULL,
  `date_read` datetime(6) DEFAULT NULL,
  `recipient_id` int(11) NOT NULL,
  `sender_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_notification_recipient_id_d99de5c8_fk_auth_user_id` (`recipient_id`),
  KEY `customer_notification_sender_id_affa1632_fk_auth_user_id` (`sender_id`),
  CONSTRAINT `customer_notification_recipient_id_d99de5c8_fk_auth_user_id` FOREIGN KEY (`recipient_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `customer_notification_sender_id_affa1632_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_notification`
--

LOCK TABLES `customer_notification` WRITE;
/*!40000 ALTER TABLE `customer_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_productalert`
--

DROP TABLE IF EXISTS `customer_productalert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_productalert` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) COLLATE utf8_unicode_ci NOT NULL,
  `key` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_confirmed` datetime(6) DEFAULT NULL,
  `date_cancelled` datetime(6) DEFAULT NULL,
  `date_closed` datetime(6) DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_productaler_product_id_7e529a41_fk_catalogue` (`product_id`),
  KEY `customer_productalert_user_id_677ad6d6_fk_auth_user_id` (`user_id`),
  KEY `customer_productalert_email_e5f35f45` (`email`),
  KEY `customer_productalert_key_a26f3bdc` (`key`),
  CONSTRAINT `customer_productaler_product_id_7e529a41_fk_catalogue` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`),
  CONSTRAINT `customer_productalert_user_id_677ad6d6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_productalert`
--

LOCK TABLES `customer_productalert` WRITE;
/*!40000 ALTER TABLE `customer_productalert` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_productalert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_crontabschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) COLLATE utf8_unicode_ci NOT NULL,
  `hour` varchar(96) COLLATE utf8_unicode_ci NOT NULL,
  `day_of_week` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `day_of_month` varchar(124) COLLATE utf8_unicode_ci NOT NULL,
  `month_of_year` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_crontabschedule`
--

LOCK TABLES `django_celery_beat_crontabschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_intervalschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_intervalschedule`
--

LOCK TABLES `django_celery_beat_intervalschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictask`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `task` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `args` longtext COLLATE utf8_unicode_ci NOT NULL,
  `kwargs` longtext COLLATE utf8_unicode_ci NOT NULL,
  `queue` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `exchange` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `routing_key` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `interval_id` int(11) DEFAULT NULL,
  `solar_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` (`crontab_id`),
  KEY `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` (`interval_id`),
  KEY `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` (`solar_id`),
  CONSTRAINT `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` FOREIGN KEY (`solar_id`) REFERENCES `django_celery_beat_solarschedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictask`
--

LOCK TABLES `django_celery_beat_periodictask` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictask` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictasks`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictasks`
--

LOCK TABLES `django_celery_beat_periodictasks` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_solarschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_solarschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_solarschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event` varchar(24) COLLATE utf8_unicode_ci NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq` (`event`,`latitude`,`longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_solarschedule`
--

LOCK TABLES `django_celery_beat_solarschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (12,'account','emailaddress'),(13,'account','emailconfirmation'),(26,'address','country'),(27,'address','useraddress'),(2,'admin','logentry'),(22,'analytics','productrecord'),(23,'analytics','userproductview'),(24,'analytics','userrecord'),(25,'analytics','usersearch'),(4,'auth','group'),(3,'auth','permission'),(5,'auth','user'),(48,'basket','basket'),(49,'basket','line'),(50,'basket','lineattribute'),(10,'blockuser','quantpolicy'),(11,'blockuser','quantpolicyorder'),(1,'captcha','captchastore'),(31,'catalogue','attributeoption'),(32,'catalogue','attributeoptiongroup'),(33,'catalogue','category'),(34,'catalogue','option'),(35,'catalogue','product'),(36,'catalogue','productattribute'),(37,'catalogue','productattributevalue'),(38,'catalogue','productcategory'),(39,'catalogue','productclass'),(40,'catalogue','productimage'),(41,'catalogue','productrecommendation'),(6,'contenttypes','contenttype'),(87,'customer','communicationeventtype'),(88,'customer','email'),(89,'customer','notification'),(90,'customer','productalert'),(17,'django_celery_beat','crontabschedule'),(18,'django_celery_beat','intervalschedule'),(19,'django_celery_beat','periodictask'),(20,'django_celery_beat','periodictasks'),(21,'django_celery_beat','solarschedule'),(117,'duiqiao','duiqiaopolicy'),(9,'flatpages','flatpage'),(61,'offer','absolutediscountbenefit'),(55,'offer','benefit'),(56,'offer','condition'),(57,'offer','conditionaloffer'),(62,'offer','countcondition'),(63,'offer','coveragecondition'),(64,'offer','fixedpricebenefit'),(65,'offer','multibuydiscountbenefit'),(66,'offer','percentagediscountbenefit'),(58,'offer','range'),(59,'offer','rangeproduct'),(60,'offer','rangeproductfileupload'),(68,'offer','shippingabsolutediscountbenefit'),(67,'offer','shippingbenefit'),(69,'offer','shippingfixedpricebenefit'),(70,'offer','shippingpercentagediscountbenefit'),(71,'offer','valuecondition'),(72,'order','billingaddress'),(73,'order','communicationevent'),(74,'order','line'),(75,'order','lineattribute'),(76,'order','lineprice'),(77,'order','order'),(78,'order','orderdiscount'),(79,'order','ordernote'),(80,'order','paymentevent'),(81,'order','paymenteventquantity'),(82,'order','paymenteventtype'),(83,'order','shippingaddress'),(84,'order','shippingevent'),(85,'order','shippingeventquantity'),(86,'order','shippingeventtype'),(108,'oscar_accounts','account'),(109,'oscar_accounts','accounttype'),(110,'oscar_accounts','ipaddressrecord'),(111,'oscar_accounts','transaction'),(112,'oscar_accounts','transfer'),(113,'oscarapi','apikey'),(44,'partner','partner'),(45,'partner','partneraddress'),(46,'partner','stockalert'),(47,'partner','stockrecord'),(51,'payment','bankcard'),(52,'payment','source'),(53,'payment','sourcetype'),(54,'payment','transaction'),(114,'paypal','expresstransaction'),(115,'paypal','payflowtransaction'),(91,'promotions','automaticproductlist'),(92,'promotions','handpickedproductlist'),(93,'promotions','image'),(94,'promotions','keywordpromotion'),(95,'promotions','multiimage'),(96,'promotions','orderedproduct'),(97,'promotions','orderedproductlist'),(98,'promotions','pagepromotion'),(99,'promotions','rawhtml'),(100,'promotions','singleproduct'),(101,'promotions','tabbedblock'),(42,'reviews','productreview'),(43,'reviews','vote'),(116,'sanjiao','sanjiaopolicy'),(7,'sessions','session'),(28,'shipping','orderanditemcharges'),(29,'shipping','weightband'),(30,'shipping','weightbased'),(8,'sites','site'),(14,'socialaccount','socialaccount'),(15,'socialaccount','socialapp'),(16,'socialaccount','socialtoken'),(107,'thumbnail','kvstore'),(102,'voucher','voucher'),(103,'voucher','voucherapplication'),(104,'voucher','voucherset'),(105,'wishlists','line'),(106,'wishlists','wishlist');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_flatpage`
--

DROP TABLE IF EXISTS `django_flatpage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_flatpage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `content` longtext COLLATE utf8_unicode_ci NOT NULL,
  `enable_comments` tinyint(1) NOT NULL,
  `template_name` varchar(70) COLLATE utf8_unicode_ci NOT NULL,
  `registration_required` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_flatpage_url_41612362` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_flatpage`
--

LOCK TABLES `django_flatpage` WRITE;
/*!40000 ALTER TABLE `django_flatpage` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_flatpage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_flatpage_sites`
--

DROP TABLE IF EXISTS `django_flatpage_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_flatpage_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flatpage_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_flatpage_sites_flatpage_id_site_id_0d29d9d1_uniq` (`flatpage_id`,`site_id`),
  KEY `django_flatpage_sites_site_id_bfd8ea84_fk_django_site_id` (`site_id`),
  CONSTRAINT `django_flatpage_sites_flatpage_id_078bbc8b_fk_django_flatpage_id` FOREIGN KEY (`flatpage_id`) REFERENCES `django_flatpage` (`id`),
  CONSTRAINT `django_flatpage_sites_site_id_bfd8ea84_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_flatpage_sites`
--

LOCK TABLES `django_flatpage_sites` WRITE;
/*!40000 ALTER TABLE `django_flatpage_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_flatpage_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2019-03-15 11:57:18.293969'),(2,'auth','0001_initial','2019-03-15 11:57:19.527458'),(3,'account','0001_initial','2019-03-15 11:57:19.807425'),(4,'account','0002_email_max_length','2019-03-15 11:57:19.899212'),(5,'address','0001_initial','2019-03-15 11:57:20.470231'),(6,'address','0002_auto_20150927_1547','2019-03-15 11:57:20.636723'),(7,'address','0003_auto_20150927_1551','2019-03-15 11:57:20.708670'),(8,'address','0004_auto_20170226_1122','2019-03-15 11:57:20.772124'),(9,'address','0005_regenerate_user_address_hashes','2019-03-15 11:57:20.831864'),(10,'admin','0001_initial','2019-03-15 11:57:21.051233'),(11,'admin','0002_logentry_remove_auto_add','2019-03-15 11:57:21.140980'),(12,'catalogue','0001_initial','2019-03-15 11:57:24.076585'),(13,'analytics','0001_initial','2019-03-15 11:57:24.717574'),(14,'analytics','0002_auto_20140827_1705','2019-03-15 11:57:25.192850'),(15,'contenttypes','0002_remove_content_type_name','2019-03-15 11:57:25.438747'),(16,'auth','0002_alter_permission_name_max_length','2019-03-15 11:57:25.570506'),(17,'auth','0003_alter_user_email_max_length','2019-03-15 11:57:25.728578'),(18,'auth','0004_alter_user_username_opts','2019-03-15 11:57:25.817774'),(19,'auth','0005_alter_user_last_login_null','2019-03-15 11:57:25.955131'),(20,'auth','0006_require_contenttypes_0002','2019-03-15 11:57:26.027582'),(21,'auth','0007_alter_validators_add_error_messages','2019-03-15 11:57:26.128919'),(22,'auth','0008_alter_user_username_max_length','2019-03-15 11:57:26.274654'),(23,'sites','0001_initial','2019-03-15 11:57:26.399981'),(24,'partner','0001_initial','2019-03-15 11:57:27.603329'),(25,'customer','0001_initial','2019-03-15 11:57:28.634457'),(26,'basket','0001_initial','2019-03-15 11:57:29.002215'),(27,'basket','0002_auto_20140827_1705','2019-03-15 11:57:29.826208'),(28,'order','0001_initial','2019-03-15 11:57:36.712470'),(29,'offer','0001_initial','2019-03-15 11:57:39.767105'),(30,'voucher','0001_initial','2019-03-15 11:57:40.805412'),(31,'basket','0003_basket_vouchers','2019-03-15 11:57:41.428241'),(32,'basket','0004_auto_20141007_2032','2019-03-15 11:57:41.635471'),(33,'basket','0005_auto_20150604_1450','2019-03-15 11:57:42.072475'),(34,'basket','0006_auto_20160111_1108','2019-03-15 11:57:42.271912'),(35,'basket','0007_slugfield_noop','2019-03-15 11:57:42.490244'),(36,'captcha','0001_initial','2019-03-15 11:57:42.717192'),(37,'catalogue','0002_auto_20150217_1221','2019-03-15 11:57:42.950644'),(38,'catalogue','0003_data_migration_slugs','2019-03-15 11:57:43.193635'),(39,'catalogue','0004_auto_20150217_1710','2019-03-15 11:57:43.397415'),(40,'catalogue','0005_auto_20150604_1450','2019-03-15 11:57:43.711641'),(41,'catalogue','0006_auto_20150807_1725','2019-03-15 11:57:43.884173'),(42,'catalogue','0007_auto_20151207_1440','2019-03-15 11:57:44.081486'),(43,'catalogue','0008_auto_20160304_1652','2019-03-15 11:57:44.281565'),(44,'catalogue','0009_slugfield_noop','2019-03-15 11:57:44.495178'),(45,'catalogue','0010_auto_20170420_0439','2019-03-15 11:57:45.198340'),(46,'catalogue','0011_auto_20170422_1355','2019-03-15 11:57:45.491381'),(47,'catalogue','0012_auto_20170609_1902','2019-03-15 11:57:45.891638'),(48,'catalogue','0013_auto_20170821_1548','2019-03-15 11:57:46.225864'),(49,'customer','0002_auto_20150807_1725','2019-03-15 11:57:46.392462'),(50,'customer','0003_update_email_length','2019-03-15 11:57:46.672745'),(51,'customer','0004_email_save','2019-03-15 11:57:47.114193'),(52,'django_celery_beat','0001_initial','2019-03-15 11:57:47.659862'),(53,'django_celery_beat','0002_auto_20161118_0346','2019-03-15 11:57:47.970513'),(54,'django_celery_beat','0003_auto_20161209_0049','2019-03-15 11:57:48.175638'),(55,'django_celery_beat','0004_auto_20170221_0000','2019-03-15 11:57:48.319732'),(56,'django_celery_beat','0005_add_solarschedule_events_choices','2019-03-15 11:57:48.475134'),(57,'django_celery_beat','0006_auto_20180210_1226','2019-03-15 11:57:48.769602'),(58,'flatpages','0001_initial','2019-03-15 11:57:49.287835'),(59,'offer','0002_auto_20151210_1053','2019-03-15 11:57:49.504282'),(60,'offer','0003_auto_20161120_1707','2019-03-15 11:57:49.734928'),(61,'offer','0004_auto_20170415_1518','2019-03-15 11:57:49.913300'),(62,'offer','0005_auto_20170423_1217','2019-03-15 11:57:50.563949'),(63,'offer','0006_auto_20170504_0616','2019-03-15 11:57:50.807739'),(64,'offer','0007_conditionaloffer_exclusive','2019-03-15 11:57:51.231605'),(65,'order','0002_auto_20141007_2032','2019-03-15 11:57:51.463837'),(66,'order','0003_auto_20150113_1629','2019-03-15 11:57:51.690518'),(67,'order','0004_auto_20160111_1108','2019-03-15 11:57:51.936492'),(68,'order','0005_update_email_length','2019-03-15 11:57:52.235334'),(69,'oscar_accounts','0001_initial','2019-03-15 11:57:54.100453'),(70,'oscar_accounts','0002_core_accounts','2019-03-15 11:57:54.416201'),(71,'oscar_accounts','0003_alter_ip_address','2019-03-15 11:57:54.696888'),(72,'oscarapi','0001_initial','2019-03-15 11:57:55.047118'),(73,'partner','0002_auto_20141007_2032','2019-03-15 11:57:55.454997'),(74,'partner','0003_auto_20150604_1450','2019-03-15 11:57:55.840493'),(75,'partner','0004_auto_20160107_1755','2019-03-15 11:57:56.057147'),(76,'payment','0001_initial','2019-03-15 11:57:57.107227'),(77,'payment','0002_auto_20141007_2032','2019-03-15 11:57:57.371090'),(78,'payment','0003_auto_20160323_1520','2019-03-15 11:57:57.588543'),(79,'paypal','0001_initial','2019-03-15 11:57:58.079559'),(80,'promotions','0001_initial','2019-03-15 11:58:00.463072'),(81,'promotions','0002_auto_20150604_1450','2019-03-15 11:58:01.029108'),(82,'reviews','0001_initial','2019-03-15 11:58:02.180843'),(83,'reviews','0002_update_email_length','2019-03-15 11:58:02.472559'),(84,'reviews','0003_auto_20160802_1358','2019-03-15 11:58:02.739750'),(85,'reviews','0004_auto_20170429_0941','2019-03-15 11:58:03.142441'),(86,'sessions','0001_initial','2019-03-15 11:58:03.472763'),(87,'shipping','0001_initial','2019-03-15 11:58:04.446632'),(88,'shipping','0002_auto_20150604_1450','2019-03-15 11:58:05.279022'),(89,'sites','0002_alter_domain_unique','2019-03-15 11:58:05.552155'),(90,'socialaccount','0001_initial','2019-03-15 11:58:07.124962'),(91,'socialaccount','0002_token_max_lengths','2019-03-15 11:58:07.605319'),(92,'socialaccount','0003_extra_data_default_dict','2019-03-15 11:58:07.941976'),(93,'thumbnail','0001_initial','2019-03-15 11:58:08.427136'),(94,'voucher','0002_auto_20170418_2132','2019-03-15 11:58:09.019001'),(95,'voucher','0003_auto_20171212_0411','2019-03-15 11:58:09.511002'),(96,'voucher','0004_auto_20180228_0940','2019-03-15 11:58:10.257198'),(97,'voucher','0005_auto_20180402_1425','2019-03-15 11:58:10.685668'),(98,'voucher','0006_auto_20180413_0911','2019-03-15 11:58:11.059821'),(99,'wishlists','0001_initial','2019-03-15 11:58:11.983311'),(100,'wishlists','0002_auto_20160111_1108','2019-03-15 11:58:12.295498'),(101,'duiqiao','0001_initial','2019-03-15 11:58:50.673208'),(102,'sanjiao','0001_initial','2019-03-15 11:58:51.250760'),(103,'blockuser','0001_initial','2019-03-17 12:47:28.579440'),(104,'basket','0008_auto_20190318_1429','2019-03-18 06:30:05.839062'),(105,'reviews','0005_auto_20190318_1429','2019-03-18 06:30:06.603410');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4rvr5kzpm394i4fkqakxxy3y46bei3gd','NTY3YjM5ZTk1NDhlNDlmNDVlOTBhMTFjYTQwYjQ3Y2JiNWFmZTU4Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoib3NjYXIuYXBwcy5jdXN0b21lci5hdXRoX2JhY2tlbmRzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImU2YTg5NGIwMzE3OTcyZDAxYTA0OGFhMTExZjQ3ZDNjYTM3MjNiZTgifQ==','2019-03-31 12:54:33.092165'),('szoozmk0f2d3isz21x1hm2jyhospw0yz','YmRjMGQ3NjkzNjYyOTA4Mzc0NzRkYTMxZGVjMTNmZTljNmQxMjgwNzqABJU9BQAAAAAAAH2UKIwNX2F1dGhfdXNlcl9pZJSMATGUjBJfYXV0aF91c2VyX2JhY2tlbmSUjC5vc2Nhci5hcHBzLmN1c3RvbWVyLmF1dGhfYmFja2VuZHMuRW1haWxCYWNrZW5klIwPX2F1dGhfdXNlcl9oYXNolIwoZTZhODk0YjAzMTc5NzJkMDFhMDQ4YWExMTFmNDdkM2NhMzcyM2JlOJSMDWNoZWNrb3V0X2RhdGGUfZQojAhzaGlwcGluZ5R9lIwLbWV0aG9kX2NvZGWUjBRuby1zaGlwcGluZy1yZXF1aXJlZJRzjAdiaWxsaW5nlH2UjApzdWJtaXNzaW9ulH2UKIwMb3JkZXJfbnVtYmVylEqmhgEAjAliYXNrZXRfaWSUSwZ1jAhhY2NvdW50c5R9lIwHcGF5bWVudJR9lIwGc291cmNllIwOYWxpcGF5X3dhcnJhbnSUc4wFb3JkZXKUfZQojAZudW1iZXKUSqaGAQCMCnN1Ym1pc3Npb26UfZQojBBzaGlwcGluZ19hZGRyZXNzlE6MD3NoaXBwaW5nX21ldGhvZJSMG29zY2FyLmFwcHMuc2hpcHBpbmcubWV0aG9kc5SMEk5vU2hpcHBpbmdSZXF1aXJlZJSTlCmBlIwPc2hpcHBpbmdfY2hhcmdllIwRb3NjYXIuY29yZS5wcmljZXOUjAVQcmljZZSTlCmBlH2UKIwIY3VycmVuY3mUjANSTUKUjAhleGNsX3RheJSMB2RlY2ltYWyUjAdEZWNpbWFslJOUjAQwLjAwlIWUUpSMCGluY2xfdGF4lGgvjAQwLjAwlIWUUpSMDGlzX3RheF9rbm93bpSIdWKMD2JpbGxpbmdfYWRkcmVzc5ROjAtvcmRlcl90b3RhbJRoJymBlH2UKGgqaCtoLGgvjAc2MDAwLjAwlIWUUpRoM2gvjAc2MDAwLjAwlIWUUpRoN4h1YowMb3JkZXJfa3dhcmdzlH2UjAdzdWJqZWN0lIwe57uP5YW45a+55pWy5oyW55+/5Lqk5piT562W55WllHOMDnBheW1lbnRfa3dhcmdzlH2UdXWMBmFsaXBheZR9lIwHd2FycmFudJSMEmFsaXBheS5nYXRld2F5aW5mb5SMBkFsaXBheZSTlCmBlH2UKIwDa2V5lIwAlIwDcGlklGhRjA5kZWZhdWx0X3BhcmFtc5R9lCiMDl9pbnB1dF9jaGFyc2V0lIwFdXRmLTiUjAdwYXJ0bmVylGhRjAxwYXltZW50X3R5cGWUaAKMCXNpZ25fdHlwZZSMA01ENZSMCXNlbGxlcl9pZJRoUXWMBnBhcmFtc5R9lChoVWhWaFdoUWhYaAJoWWhaaFtoUYwHc2VydmljZZSMHWNyZWF0ZV9wYXJ0bmVyX3RyYWRlX2J5X2J1eWVylGhEaEWMBXByaWNllGgvjAc2MDAwLjAwlIWUUpSMCHF1YW50aXR5lEsBjA1sb2dpc3RpY3NfZmVllGg2jA5sb2dpc3RpY3NfdHlwZZSMB0VYUFJFU1OUjBFsb2dpc3RpY3NfcGF5bWVudJSMCUJVWUVSX1BBWZSMDG91dF90cmFkZV9ub5RKpoYBAIwKbm90aWZ5X3VybJSMHWh0dHA6Ly8xMjcuMC4wLjE6ODA4NS9yZXNwb25klIwKcmV0dXJuX3VybJSMHWh0dHA6Ly8xMjcuMC4wLjE6ODA4NS9yZXNwb25klHWMCnNpZ25fdHVwbGWUaFloWmhah5SMCHNpZ25fa2V5lIl1YnN1jAxvZmZlcl93aXphcmSUfZR1Lg==','2019-04-03 01:34:08.967100'),('ump5yqt7q7mqlg9ilh9ha7eumjx0rh14','ZDViMmMwYWE0MWI3MTc1YzJhODNiNWY0MDkxZGFjMmQ0MTQ4MGRjYzqABJXvBQAAAAAAAH2UKIwNX2F1dGhfdXNlcl9pZJSMATGUjBJfYXV0aF91c2VyX2JhY2tlbmSUjC5vc2Nhci5hcHBzLmN1c3RvbWVyLmF1dGhfYmFja2VuZHMuRW1haWxCYWNrZW5klIwPX2F1dGhfdXNlcl9oYXNolIwoZTZhODk0YjAzMTc5NzJkMDFhMDQ4YWExMTFmNDdkM2NhMzcyM2JlOJSMDWNoZWNrb3V0X2RhdGGUfZQojAhzaGlwcGluZ5R9lIwLbWV0aG9kX2NvZGWUjBRuby1zaGlwcGluZy1yZXF1aXJlZJRzjAdwYXltZW50lH2UjAZzb3VyY2WUjA1vc2Nhcl9hY2NvdW50lHOMB2JpbGxpbmeUfZSMCnN1Ym1pc3Npb26UfZQojAxvcmRlcl9udW1iZXKUSq2GAQCMCWJhc2tldF9pZJRLDXWMBW9yZGVylH2UKIwGbnVtYmVylEqthgEAaBN9lCiMEHNoaXBwaW5nX2FkZHJlc3OUTowPc2hpcHBpbmdfbWV0aG9klIwbb3NjYXIuYXBwcy5zaGlwcGluZy5tZXRob2RzlIwSTm9TaGlwcGluZ1JlcXVpcmVklJOUKYGUjA9zaGlwcGluZ19jaGFyZ2WUjBFvc2Nhci5jb3JlLnByaWNlc5SMBVByaWNllJOUKYGUfZQojAhjdXJyZW5jeZSMA1JNQpSMCGV4Y2xfdGF4lIwHZGVjaW1hbJSMB0RlY2ltYWyUk5SMBDAuMDCUhZRSlIwIaW5jbF90YXiUaCyMBDAuMDCUhZRSlIwMaXNfdGF4X2tub3dulIh1YowPYmlsbGluZ19hZGRyZXNzlE6MC29yZGVyX3RvdGFslGgkKYGUfZQoaCdoKGgpaCyMBzMwMDAuMDCUhZRSlGgwaCyMBzMwMDAuMDCUhZRSlGg0iHVijAxvcmRlcl9rd2FyZ3OUfZSMB3N1YmplY3SUjB7nu4/lhbjlr7nmlbLmjJbnn7/kuqTmmJPnrZbnlaWUc4wOcGF5bWVudF9rd2FyZ3OUfZR1dYwGYWxpcGF5lH2UjAd3YXJyYW50lIwSYWxpcGF5LmdhdGV3YXlpbmZvlIwGQWxpcGF5lJOUKYGUfZQojANrZXmUjACUjANwaWSUaE6MDmRlZmF1bHRfcGFyYW1zlH2UKIwOX2lucHV0X2NoYXJzZXSUjAV1dGYtOJSMB3BhcnRuZXKUaE6MDHBheW1lbnRfdHlwZZRoAowJc2lnbl90eXBllIwDTUQ1lIwJc2VsbGVyX2lklGhOdYwGcGFyYW1zlH2UKGhSaFNoVGhOaFVoAmhWaFdoWGhOjAdzZXJ2aWNllIwdY3JlYXRlX3BhcnRuZXJfdHJhZGVfYnlfYnV5ZXKUjAdzdWJqZWN0lIwe57uP5YW45a+55pWy5oyW55+/5Lqk5piT562W55WllIwFcHJpY2WUaCyMCDEyMDAwLjAwlIWUUpSMCHF1YW50aXR5lEsBjA1sb2dpc3RpY3NfZmVllGgsjAQwLjAwlIWUUpSMDmxvZ2lzdGljc190eXBllIwHRVhQUkVTU5SMEWxvZ2lzdGljc19wYXltZW50lIwJQlVZRVJfUEFZlIwMb3V0X3RyYWRlX25vlEqshgEAjApub3RpZnlfdXJslIwdaHR0cDovLzEyNy4wLjAuMTo4MDg1L3Jlc3BvbmSUjApyZXR1cm5fdXJslIwdaHR0cDovLzEyNy4wLjAuMTo4MDg1L3Jlc3BvbmSUdYwKc2lnbl90dXBsZZRoVmhXaFeHlIwIc2lnbl9rZXmUiXVic4wFcGF5anOUfZSMBndlaXhpbpSMEXBheWpzLmdhdGV3YXlpbmZvlIwFUGF5anOUk5QpgZR9lCiMDG1lcmNoYW50X2tleZSMA3h4eJSMC21lcmNoYW50X2lklGh9jApub3RpZnlfdXJslGh9dWJzjAhhY2NvdW50c5R9lIwLYWxsb2NhdGlvbnOUjBx7IkFYMzFIVk44TzVRRyI6ICIxNTAwMC4wMCJ9lHN1dS4=','2019-04-19 12:49:11.731004');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `duiqiao`
--

DROP TABLE IF EXISTS `duiqiao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `duiqiao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exchange` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `accesskey` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `secretkey` longtext COLLATE utf8_unicode_ci NOT NULL,
  `symbol` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `max_buy_price` double NOT NULL,
  `min_sell_price` double NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `status` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `operation` int(11) NOT NULL,
  `base_volume` double NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `duiqiao_user_id_8b580dd2_fk_auth_user_id` (`user_id`),
  CONSTRAINT `duiqiao_user_id_8b580dd2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `duiqiao`
--

LOCK TABLES `duiqiao` WRITE;
/*!40000 ALTER TABLE `duiqiao` DISABLE KEYS */;
INSERT INTO `duiqiao` VALUES (1,'huobipro','hello','AKQPk0snmWETzUHw79jCL1GjdUZV_zIg7CpEtAsXKJotFuj_4dmAg0g4q76GVmYUxH6xpX3TquIY','BTC/USDT',3900,3800,'2019-04-03 14:00:00.000000','2019-04-16 05:00:00.000000','2019-04-02 23:51:29.566104','2019-04-02 23:51:29.566124','unstart',0,0.00001,1),(2,'binance','hello','AKQPk0tWB-lZ6nIUrWn4iPoMeurKDErYAr3tXl3v4bKJy89Mju6HKN7vTasw_F8FV9vV8_LK1-s_','BTC/USDT',3900,3800,'2019-04-03 14:00:00.000000','2019-04-16 05:00:00.000000','2019-04-02 23:52:45.044813','2019-04-02 23:52:45.044834','unstart',0,0.00001,1),(3,'huobipro','hello','AKQPk0uJPKGmiubl7dMuunH_y7vgAm3NzdEe7pNVP9uZ86CAkekU7trj2Nj8v_Rk9CKHMqzoEdWo','BTC/USDT',6300,8440,'2019-04-03 14:00:00.000000','2019-04-16 05:00:00.000000','2019-04-02 23:54:02.040801','2019-04-02 23:54:02.040823','unstart',0,11,1),(4,'binance','hello','AKQPk0v2VVTTBCF4lOs_vIHVeUp8bs1QT9xKGAsGPKo0I9DPNyzjyMVibAQYwq0cdmz4jLj59kKB','BTC/USDT',6300,8440,'2019-04-03 14:00:00.000000','2019-04-16 05:00:00.000000','2019-04-02 23:58:21.002623','2019-04-02 23:58:21.002642','unstart',0,11,1),(5,'binance','hello','AKQPk0t3le00w_dvQFWIpi4_HjuhsukzeicpkGhoJXI6lzryrjkLYUh-MGjA0jhLNFIX_PZ0KtmA','BTC/USDT',6300,8440,'2019-04-03 14:00:00.000000','2019-04-16 05:00:00.000000','2019-04-03 11:13:15.296187','2019-04-03 01:10:42.296215','unstart',0,11,1),(6,'binance','dd','AKQPk0u8aazrCVYsQ4BZKKPa7CFagys2MQxRuvHUVt1Ot9ZYkjBRn1vYP9R4vQF0N2WXwkkwkTFP','dd',11,11,'2019-04-03 14:00:00.000000','2019-04-23 13:00:00.000000','2019-04-03 11:14:05.734701','2019-04-03 11:14:05.734722','unstart',0,11,1),(7,'binance','ddd','AKQPk0vDuj3Q2CNzM1_T8lQp9LrYs_UIiNMsM6iGnXLO8nzba3DRBF_939LYR-dKQZFbxB5qSx1g','BTC/USDT',674,444,'2019-04-23 09:00:00.000000','2019-04-30 05:00:00.000000','2019-04-03 11:38:55.502031','2019-04-03 11:38:55.502064','unstart',0,0.00001,1),(8,'binance','ddd','AKQPk0tJXTCc-_u-JLiDgMDdLqGODPAXeiYyxfi_2-h-XDFyMg1M-pGbtczK5csDH-QNX0RWDBXe','2',3,4,'2019-04-02 17:05:00.000000','2019-04-16 05:00:00.000000','2019-04-04 08:24:27.196744','2019-04-04 06:01:56.433554','run',0,5,1),(9,'binance','1','AKQPk0s520NqlPLJCy66emrsE03KQ7fBO4MOn1SNGziIZHRndNnglC2JYDpq_J6fN4EWCxjqUCnw','3',4,5,'2019-04-03 14:00:00.000000','2019-04-30 05:00:00.000000','2019-04-13 07:12:17.881724','2019-04-04 08:26:04.073066','run',0,111,1),(10,'huobipro','28d3ce92-1779ac7b-2e474c13-4750e','AKQPk0u8i5H-Cgk3tBlcMEbgVNXCNo5t8tWcOUDVlAQoWb4uHCgzBU82Dvb_3SVd_WeI3SdCD87TKLAyoEEjW7wn-dRoDjprAtUP6RVINhc_6Sv5qTzO8T0','BTC/USDT',5067,5066,'2019-04-13 08:35:00.000000','2019-04-13 08:55:00.000000','2019-04-13 08:34:48.009093','2019-04-13 07:31:35.823548','stop',0,0.0001,1);
/*!40000 ALTER TABLE `duiqiao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offer_benefit`
--

DROP TABLE IF EXISTS `offer_benefit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offer_benefit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `value` decimal(12,2) DEFAULT NULL,
  `max_affected_items` int(10) unsigned DEFAULT NULL,
  `proxy_class` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `range_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `offer_benefit_range_id_ab19c5ab_fk_offer_range_id` (`range_id`),
  CONSTRAINT `offer_benefit_range_id_ab19c5ab_fk_offer_range_id` FOREIGN KEY (`range_id`) REFERENCES `offer_range` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offer_benefit`
--

LOCK TABLES `offer_benefit` WRITE;
/*!40000 ALTER TABLE `offer_benefit` DISABLE KEYS */;
/*!40000 ALTER TABLE `offer_benefit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offer_condition`
--

DROP TABLE IF EXISTS `offer_condition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offer_condition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `value` decimal(12,2) DEFAULT NULL,
  `proxy_class` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `range_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `offer_condition_range_id_b023a2aa_fk_offer_range_id` (`range_id`),
  CONSTRAINT `offer_condition_range_id_b023a2aa_fk_offer_range_id` FOREIGN KEY (`range_id`) REFERENCES `offer_range` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offer_condition`
--

LOCK TABLES `offer_condition` WRITE;
/*!40000 ALTER TABLE `offer_condition` DISABLE KEYS */;
/*!40000 ALTER TABLE `offer_condition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offer_conditionaloffer`
--

DROP TABLE IF EXISTS `offer_conditionaloffer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offer_conditionaloffer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `slug` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `offer_type` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `status` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `priority` int(11) NOT NULL,
  `start_datetime` datetime(6) DEFAULT NULL,
  `end_datetime` datetime(6) DEFAULT NULL,
  `max_global_applications` int(10) unsigned DEFAULT NULL,
  `max_user_applications` int(10) unsigned DEFAULT NULL,
  `max_basket_applications` int(10) unsigned DEFAULT NULL,
  `max_discount` decimal(12,2) DEFAULT NULL,
  `total_discount` decimal(12,2) NOT NULL,
  `num_applications` int(10) unsigned NOT NULL,
  `num_orders` int(10) unsigned NOT NULL,
  `redirect_url` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `benefit_id` int(11) NOT NULL,
  `condition_id` int(11) NOT NULL,
  `exclusive` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`),
  KEY `offer_conditionaloffer_benefit_id_f43f68b5_fk_offer_benefit_id` (`benefit_id`),
  KEY `offer_conditionaloff_condition_id_e6baa945_fk_offer_con` (`condition_id`),
  CONSTRAINT `offer_conditionaloff_condition_id_e6baa945_fk_offer_con` FOREIGN KEY (`condition_id`) REFERENCES `offer_condition` (`id`),
  CONSTRAINT `offer_conditionaloffer_benefit_id_f43f68b5_fk_offer_benefit_id` FOREIGN KEY (`benefit_id`) REFERENCES `offer_benefit` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offer_conditionaloffer`
--

LOCK TABLES `offer_conditionaloffer` WRITE;
/*!40000 ALTER TABLE `offer_conditionaloffer` DISABLE KEYS */;
/*!40000 ALTER TABLE `offer_conditionaloffer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offer_range`
--

DROP TABLE IF EXISTS `offer_range`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offer_range` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `slug` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  `includes_all_products` tinyint(1) NOT NULL,
  `proxy_class` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`),
  UNIQUE KEY `proxy_class` (`proxy_class`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offer_range`
--

LOCK TABLES `offer_range` WRITE;
/*!40000 ALTER TABLE `offer_range` DISABLE KEYS */;
/*!40000 ALTER TABLE `offer_range` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offer_range_classes`
--

DROP TABLE IF EXISTS `offer_range_classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offer_range_classes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `range_id` int(11) NOT NULL,
  `productclass_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `offer_range_classes_range_id_productclass_id_28eeefae_uniq` (`range_id`,`productclass_id`),
  KEY `offer_range_classes_productclass_id_6f6de46d_fk_catalogue` (`productclass_id`),
  CONSTRAINT `offer_range_classes_productclass_id_6f6de46d_fk_catalogue` FOREIGN KEY (`productclass_id`) REFERENCES `catalogue_productclass` (`id`),
  CONSTRAINT `offer_range_classes_range_id_7d3e573e_fk_offer_range_id` FOREIGN KEY (`range_id`) REFERENCES `offer_range` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offer_range_classes`
--

LOCK TABLES `offer_range_classes` WRITE;
/*!40000 ALTER TABLE `offer_range_classes` DISABLE KEYS */;
/*!40000 ALTER TABLE `offer_range_classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offer_range_excluded_products`
--

DROP TABLE IF EXISTS `offer_range_excluded_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offer_range_excluded_products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `range_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `offer_range_excluded_products_range_id_product_id_eb1cfe87_uniq` (`range_id`,`product_id`),
  KEY `offer_range_excluded_product_id_78c49bfc_fk_catalogue` (`product_id`),
  CONSTRAINT `offer_range_excluded_product_id_78c49bfc_fk_catalogue` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`),
  CONSTRAINT `offer_range_excluded_range_id_cce4a032_fk_offer_ran` FOREIGN KEY (`range_id`) REFERENCES `offer_range` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offer_range_excluded_products`
--

LOCK TABLES `offer_range_excluded_products` WRITE;
/*!40000 ALTER TABLE `offer_range_excluded_products` DISABLE KEYS */;
/*!40000 ALTER TABLE `offer_range_excluded_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offer_range_included_categories`
--

DROP TABLE IF EXISTS `offer_range_included_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offer_range_included_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `range_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `offer_range_included_cat_range_id_category_id_a661d336_uniq` (`range_id`,`category_id`),
  KEY `offer_range_included_category_id_c61569a5_fk_catalogue` (`category_id`),
  CONSTRAINT `offer_range_included_category_id_c61569a5_fk_catalogue` FOREIGN KEY (`category_id`) REFERENCES `catalogue_category` (`id`),
  CONSTRAINT `offer_range_included_range_id_1b616138_fk_offer_ran` FOREIGN KEY (`range_id`) REFERENCES `offer_range` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offer_range_included_categories`
--

LOCK TABLES `offer_range_included_categories` WRITE;
/*!40000 ALTER TABLE `offer_range_included_categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `offer_range_included_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offer_rangeproduct`
--

DROP TABLE IF EXISTS `offer_rangeproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offer_rangeproduct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `display_order` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `range_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `offer_rangeproduct_range_id_product_id_c46b1be8_uniq` (`range_id`,`product_id`),
  KEY `offer_rangeproduct_product_id_723b3ea3_fk_catalogue_product_id` (`product_id`),
  CONSTRAINT `offer_rangeproduct_product_id_723b3ea3_fk_catalogue_product_id` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`),
  CONSTRAINT `offer_rangeproduct_range_id_ee358495_fk_offer_range_id` FOREIGN KEY (`range_id`) REFERENCES `offer_range` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offer_rangeproduct`
--

LOCK TABLES `offer_rangeproduct` WRITE;
/*!40000 ALTER TABLE `offer_rangeproduct` DISABLE KEYS */;
/*!40000 ALTER TABLE `offer_rangeproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offer_rangeproductfileupload`
--

DROP TABLE IF EXISTS `offer_rangeproductfileupload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offer_rangeproductfileupload` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filepath` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `size` int(10) unsigned NOT NULL,
  `date_uploaded` datetime(6) NOT NULL,
  `status` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `error_message` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `date_processed` datetime(6) DEFAULT NULL,
  `num_new_skus` int(10) unsigned DEFAULT NULL,
  `num_unknown_skus` int(10) unsigned DEFAULT NULL,
  `num_duplicate_skus` int(10) unsigned DEFAULT NULL,
  `range_id` int(11) NOT NULL,
  `uploaded_by_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `offer_rangeproductfileupload_range_id_c055ebf8_fk_offer_range_id` (`range_id`),
  KEY `offer_rangeproductfi_uploaded_by_id_c01a3250_fk_auth_user` (`uploaded_by_id`),
  CONSTRAINT `offer_rangeproductfi_uploaded_by_id_c01a3250_fk_auth_user` FOREIGN KEY (`uploaded_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `offer_rangeproductfileupload_range_id_c055ebf8_fk_offer_range_id` FOREIGN KEY (`range_id`) REFERENCES `offer_range` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offer_rangeproductfileupload`
--

LOCK TABLES `offer_rangeproductfileupload` WRITE;
/*!40000 ALTER TABLE `offer_rangeproductfileupload` DISABLE KEYS */;
/*!40000 ALTER TABLE `offer_rangeproductfileupload` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_billingaddress`
--

DROP TABLE IF EXISTS `order_billingaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_billingaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line1` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line2` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line3` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line4` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `state` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `postcode` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `search_text` longtext COLLATE utf8_unicode_ci NOT NULL,
  `country_id` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_billingaddress_country_id_17f57dca_fk_address_c` (`country_id`),
  CONSTRAINT `order_billingaddress_country_id_17f57dca_fk_address_c` FOREIGN KEY (`country_id`) REFERENCES `address_country` (`iso_3166_1_a2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_billingaddress`
--

LOCK TABLES `order_billingaddress` WRITE;
/*!40000 ALTER TABLE `order_billingaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_billingaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_communicationevent`
--

DROP TABLE IF EXISTS `order_communicationevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_communicationevent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `event_type_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_communicatione_event_type_id_4bc9ee29_fk_customer_` (`event_type_id`),
  KEY `order_communicationevent_order_id_94e784ac_fk_order_order_id` (`order_id`),
  CONSTRAINT `order_communicatione_event_type_id_4bc9ee29_fk_customer_` FOREIGN KEY (`event_type_id`) REFERENCES `customer_communicationeventtype` (`id`),
  CONSTRAINT `order_communicationevent_order_id_94e784ac_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_communicationevent`
--

LOCK TABLES `order_communicationevent` WRITE;
/*!40000 ALTER TABLE `order_communicationevent` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_communicationevent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_line`
--

DROP TABLE IF EXISTS `order_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_line` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `partner_name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `partner_sku` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `partner_line_reference` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `partner_line_notes` longtext COLLATE utf8_unicode_ci NOT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `upc` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `quantity` int(10) unsigned NOT NULL,
  `line_price_incl_tax` decimal(12,2) NOT NULL,
  `line_price_excl_tax` decimal(12,2) NOT NULL,
  `line_price_before_discounts_incl_tax` decimal(12,2) NOT NULL,
  `line_price_before_discounts_excl_tax` decimal(12,2) NOT NULL,
  `unit_cost_price` decimal(12,2) DEFAULT NULL,
  `unit_price_incl_tax` decimal(12,2) DEFAULT NULL,
  `unit_price_excl_tax` decimal(12,2) DEFAULT NULL,
  `unit_retail_price` decimal(12,2) DEFAULT NULL,
  `status` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `est_dispatch_date` date DEFAULT NULL,
  `order_id` int(11) NOT NULL,
  `partner_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `stockrecord_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_line_order_id_b9148391_fk_order_order_id` (`order_id`),
  KEY `order_line_partner_id_258a2fb9_fk_partner_partner_id` (`partner_id`),
  KEY `order_line_product_id_e620902d_fk_catalogue_product_id` (`product_id`),
  KEY `order_line_stockrecord_id_1d65aff5_fk_partner_stockrecord_id` (`stockrecord_id`),
  CONSTRAINT `order_line_order_id_b9148391_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`),
  CONSTRAINT `order_line_partner_id_258a2fb9_fk_partner_partner_id` FOREIGN KEY (`partner_id`) REFERENCES `partner_partner` (`id`),
  CONSTRAINT `order_line_product_id_e620902d_fk_catalogue_product_id` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`),
  CONSTRAINT `order_line_stockrecord_id_1d65aff5_fk_partner_stockrecord_id` FOREIGN KEY (`stockrecord_id`) REFERENCES `partner_stockrecord` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_line`
--

LOCK TABLES `order_line` WRITE;
/*!40000 ALTER TABLE `order_line` DISABLE KEYS */;
INSERT INTO `order_line` VALUES (1,'bearquant','1','','','经典对敲挖矿交易策略','1',1,3000.00,3000.00,3000.00,3000.00,3000.00,3000.00,3000.00,3000.00,'Pending',NULL,1,1,3,1),(2,'bearquant','1','','','经典对敲挖矿交易策略','1',5,15000.00,15000.00,15000.00,15000.00,3000.00,3000.00,3000.00,3000.00,'Pending',NULL,2,1,3,1);
/*!40000 ALTER TABLE `order_line` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_lineattribute`
--

DROP TABLE IF EXISTS `order_lineattribute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_lineattribute` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `value` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line_id` int(11) NOT NULL,
  `option_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_lineattribute_line_id_adf6dd87_fk_order_line_id` (`line_id`),
  KEY `order_lineattribute_option_id_b54d597c_fk_catalogue_option_id` (`option_id`),
  CONSTRAINT `order_lineattribute_line_id_adf6dd87_fk_order_line_id` FOREIGN KEY (`line_id`) REFERENCES `order_line` (`id`),
  CONSTRAINT `order_lineattribute_option_id_b54d597c_fk_catalogue_option_id` FOREIGN KEY (`option_id`) REFERENCES `catalogue_option` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_lineattribute`
--

LOCK TABLES `order_lineattribute` WRITE;
/*!40000 ALTER TABLE `order_lineattribute` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_lineattribute` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_lineprice`
--

DROP TABLE IF EXISTS `order_lineprice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_lineprice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quantity` int(10) unsigned NOT NULL,
  `price_incl_tax` decimal(12,2) NOT NULL,
  `price_excl_tax` decimal(12,2) NOT NULL,
  `shipping_incl_tax` decimal(12,2) NOT NULL,
  `shipping_excl_tax` decimal(12,2) NOT NULL,
  `line_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_lineprice_line_id_2de52446_fk_order_line_id` (`line_id`),
  KEY `order_lineprice_order_id_66792e56_fk_order_order_id` (`order_id`),
  CONSTRAINT `order_lineprice_line_id_2de52446_fk_order_line_id` FOREIGN KEY (`line_id`) REFERENCES `order_line` (`id`),
  CONSTRAINT `order_lineprice_order_id_66792e56_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_lineprice`
--

LOCK TABLES `order_lineprice` WRITE;
/*!40000 ALTER TABLE `order_lineprice` DISABLE KEYS */;
INSERT INTO `order_lineprice` VALUES (1,1,3000.00,3000.00,0.00,0.00,1,1),(2,5,3000.00,3000.00,0.00,0.00,2,2);
/*!40000 ALTER TABLE `order_lineprice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_order`
--

DROP TABLE IF EXISTS `order_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `currency` varchar(12) COLLATE utf8_unicode_ci NOT NULL,
  `total_incl_tax` decimal(12,2) NOT NULL,
  `total_excl_tax` decimal(12,2) NOT NULL,
  `shipping_incl_tax` decimal(12,2) NOT NULL,
  `shipping_excl_tax` decimal(12,2) NOT NULL,
  `shipping_method` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `shipping_code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `status` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `guest_email` varchar(254) COLLATE utf8_unicode_ci NOT NULL,
  `date_placed` datetime(6) NOT NULL,
  `basket_id` int(11) DEFAULT NULL,
  `billing_address_id` int(11) DEFAULT NULL,
  `shipping_address_id` int(11) DEFAULT NULL,
  `site_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`),
  KEY `order_order_basket_id_8b0acbb2_fk_basket_basket_id` (`basket_id`),
  KEY `order_order_billing_address_id_8fe537cf_fk_order_bil` (`billing_address_id`),
  KEY `order_order_date_placed_506a9365` (`date_placed`),
  KEY `order_order_shipping_address_id_57e64931_fk_order_shi` (`shipping_address_id`),
  KEY `order_order_site_id_e27f3526_fk_django_site_id` (`site_id`),
  KEY `order_order_user_id_7cf9bc2b_fk_auth_user_id` (`user_id`),
  CONSTRAINT `order_order_basket_id_8b0acbb2_fk_basket_basket_id` FOREIGN KEY (`basket_id`) REFERENCES `basket_basket` (`id`),
  CONSTRAINT `order_order_billing_address_id_8fe537cf_fk_order_bil` FOREIGN KEY (`billing_address_id`) REFERENCES `order_billingaddress` (`id`),
  CONSTRAINT `order_order_shipping_address_id_57e64931_fk_order_shi` FOREIGN KEY (`shipping_address_id`) REFERENCES `order_shippingaddress` (`id`),
  CONSTRAINT `order_order_site_id_e27f3526_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`),
  CONSTRAINT `order_order_user_id_7cf9bc2b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_order`
--

LOCK TABLES `order_order` WRITE;
/*!40000 ALTER TABLE `order_order` DISABLE KEYS */;
INSERT INTO `order_order` VALUES (1,'100009','RMB',3000.00,3000.00,0.00,0.00,'No shipping required','no-shipping-required','Pending','','2019-03-28 00:59:25.827970',9,NULL,NULL,1,1),(2,'100013','RMB',15000.00,15000.00,0.00,0.00,'No shipping required','no-shipping-required','Pending','','2019-04-01 14:03:25.860806',13,NULL,NULL,1,1);
/*!40000 ALTER TABLE `order_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_orderdiscount`
--

DROP TABLE IF EXISTS `order_orderdiscount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_orderdiscount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `offer_id` int(10) unsigned DEFAULT NULL,
  `offer_name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `voucher_id` int(10) unsigned DEFAULT NULL,
  `voucher_code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `frequency` int(10) unsigned DEFAULT NULL,
  `amount` decimal(12,2) NOT NULL,
  `message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_orderdiscount_order_id_bc91e123_fk_order_order_id` (`order_id`),
  KEY `order_orderdiscount_offer_name_706d6119` (`offer_name`),
  KEY `order_orderdiscount_voucher_code_6ee4f360` (`voucher_code`),
  CONSTRAINT `order_orderdiscount_order_id_bc91e123_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_orderdiscount`
--

LOCK TABLES `order_orderdiscount` WRITE;
/*!40000 ALTER TABLE `order_orderdiscount` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_orderdiscount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_ordernote`
--

DROP TABLE IF EXISTS `order_ordernote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_ordernote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `note_type` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `order_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_ordernote_order_id_7d97583d_fk_order_order_id` (`order_id`),
  KEY `order_ordernote_user_id_48d7a672_fk_auth_user_id` (`user_id`),
  CONSTRAINT `order_ordernote_order_id_7d97583d_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`),
  CONSTRAINT `order_ordernote_user_id_48d7a672_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_ordernote`
--

LOCK TABLES `order_ordernote` WRITE;
/*!40000 ALTER TABLE `order_ordernote` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_ordernote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_paymentevent`
--

DROP TABLE IF EXISTS `order_paymentevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_paymentevent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(12,2) NOT NULL,
  `reference` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `event_type_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `shipping_event_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_paymentevent_event_type_id_568c7161_fk_order_pay` (`event_type_id`),
  KEY `order_paymentevent_order_id_395b3e82_fk_order_order_id` (`order_id`),
  KEY `order_paymentevent_shipping_event_id_213dcfb8_fk_order_shi` (`shipping_event_id`),
  CONSTRAINT `order_paymentevent_event_type_id_568c7161_fk_order_pay` FOREIGN KEY (`event_type_id`) REFERENCES `order_paymenteventtype` (`id`),
  CONSTRAINT `order_paymentevent_order_id_395b3e82_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`),
  CONSTRAINT `order_paymentevent_shipping_event_id_213dcfb8_fk_order_shi` FOREIGN KEY (`shipping_event_id`) REFERENCES `order_shippingevent` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_paymentevent`
--

LOCK TABLES `order_paymentevent` WRITE;
/*!40000 ALTER TABLE `order_paymentevent` DISABLE KEYS */;
INSERT INTO `order_paymentevent` VALUES (1,15000.00,'','2019-04-01 14:03:26.030329',1,2,NULL);
/*!40000 ALTER TABLE `order_paymentevent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_paymenteventquantity`
--

DROP TABLE IF EXISTS `order_paymenteventquantity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_paymenteventquantity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quantity` int(10) unsigned NOT NULL,
  `event_id` int(11) NOT NULL,
  `line_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_paymenteventquantity_event_id_line_id_765c5209_uniq` (`event_id`,`line_id`),
  KEY `order_paymenteventquantity_line_id_df44b021_fk_order_line_id` (`line_id`),
  CONSTRAINT `order_paymenteventqu_event_id_a540165a_fk_order_pay` FOREIGN KEY (`event_id`) REFERENCES `order_paymentevent` (`id`),
  CONSTRAINT `order_paymenteventquantity_line_id_df44b021_fk_order_line_id` FOREIGN KEY (`line_id`) REFERENCES `order_line` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_paymenteventquantity`
--

LOCK TABLES `order_paymenteventquantity` WRITE;
/*!40000 ALTER TABLE `order_paymenteventquantity` DISABLE KEYS */;
INSERT INTO `order_paymenteventquantity` VALUES (1,5,1,2);
/*!40000 ALTER TABLE `order_paymenteventquantity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_paymenteventtype`
--

DROP TABLE IF EXISTS `order_paymenteventtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_paymenteventtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_paymenteventtype`
--

LOCK TABLES `order_paymenteventtype` WRITE;
/*!40000 ALTER TABLE `order_paymenteventtype` DISABLE KEYS */;
INSERT INTO `order_paymenteventtype` VALUES (1,'Settle','settle');
/*!40000 ALTER TABLE `order_paymenteventtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_shippingaddress`
--

DROP TABLE IF EXISTS `order_shippingaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_shippingaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line1` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line2` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line3` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line4` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `state` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `postcode` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `search_text` longtext COLLATE utf8_unicode_ci NOT NULL,
  `phone_number` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `notes` longtext COLLATE utf8_unicode_ci NOT NULL,
  `country_id` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_shippingaddres_country_id_29abf9a0_fk_address_c` (`country_id`),
  CONSTRAINT `order_shippingaddres_country_id_29abf9a0_fk_address_c` FOREIGN KEY (`country_id`) REFERENCES `address_country` (`iso_3166_1_a2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_shippingaddress`
--

LOCK TABLES `order_shippingaddress` WRITE;
/*!40000 ALTER TABLE `order_shippingaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_shippingaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_shippingevent`
--

DROP TABLE IF EXISTS `order_shippingevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_shippingevent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `event_type_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_shippingevent_event_type_id_9f1efb20_fk_order_shi` (`event_type_id`),
  KEY `order_shippingevent_order_id_8c031fb6_fk_order_order_id` (`order_id`),
  CONSTRAINT `order_shippingevent_event_type_id_9f1efb20_fk_order_shi` FOREIGN KEY (`event_type_id`) REFERENCES `order_shippingeventtype` (`id`),
  CONSTRAINT `order_shippingevent_order_id_8c031fb6_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_shippingevent`
--

LOCK TABLES `order_shippingevent` WRITE;
/*!40000 ALTER TABLE `order_shippingevent` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_shippingevent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_shippingeventquantity`
--

DROP TABLE IF EXISTS `order_shippingeventquantity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_shippingeventquantity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quantity` int(10) unsigned NOT NULL,
  `event_id` int(11) NOT NULL,
  `line_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_shippingeventquantity_event_id_line_id_91687107_uniq` (`event_id`,`line_id`),
  KEY `order_shippingeventquantity_line_id_3b089ee0_fk_order_line_id` (`line_id`),
  CONSTRAINT `order_shippingeventq_event_id_1c7fb9c7_fk_order_shi` FOREIGN KEY (`event_id`) REFERENCES `order_shippingevent` (`id`),
  CONSTRAINT `order_shippingeventquantity_line_id_3b089ee0_fk_order_line_id` FOREIGN KEY (`line_id`) REFERENCES `order_line` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_shippingeventquantity`
--

LOCK TABLES `order_shippingeventquantity` WRITE;
/*!40000 ALTER TABLE `order_shippingeventquantity` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_shippingeventquantity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_shippingeventtype`
--

DROP TABLE IF EXISTS `order_shippingeventtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_shippingeventtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_shippingeventtype`
--

LOCK TABLES `order_shippingeventtype` WRITE;
/*!40000 ALTER TABLE `order_shippingeventtype` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_shippingeventtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oscar_accounts_account`
--

DROP TABLE IF EXISTS `oscar_accounts_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oscar_accounts_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8_unicode_ci,
  `code` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `status` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `credit_limit` decimal(12,2) DEFAULT NULL,
  `balance` decimal(12,2) DEFAULT NULL,
  `start_date` datetime(6) DEFAULT NULL,
  `end_date` datetime(6) DEFAULT NULL,
  `can_be_used_for_non_products` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `account_type_id` int(11) DEFAULT NULL,
  `primary_user_id` int(11) DEFAULT NULL,
  `product_range_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  KEY `oscar_accounts_accou_account_type_id_ce445182_fk_oscar_acc` (`account_type_id`),
  KEY `oscar_accounts_account_primary_user_id_95919c13_fk_auth_user_id` (`primary_user_id`),
  KEY `oscar_accounts_accou_product_range_id_b773d7c3_fk_offer_ran` (`product_range_id`),
  CONSTRAINT `oscar_accounts_accou_account_type_id_ce445182_fk_oscar_acc` FOREIGN KEY (`account_type_id`) REFERENCES `oscar_accounts_accounttype` (`id`),
  CONSTRAINT `oscar_accounts_accou_product_range_id_b773d7c3_fk_offer_ran` FOREIGN KEY (`product_range_id`) REFERENCES `offer_range` (`id`),
  CONSTRAINT `oscar_accounts_account_primary_user_id_95919c13_fk_auth_user_id` FOREIGN KEY (`primary_user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oscar_accounts_account`
--

LOCK TABLES `oscar_accounts_account` WRITE;
/*!40000 ALTER TABLE `oscar_accounts_account` DISABLE KEYS */;
INSERT INTO `oscar_accounts_account` VALUES (1,'Redemptions',NULL,NULL,'Open',0.00,15000.00,NULL,NULL,1,'2019-03-31 23:32:02.988180',2,NULL,NULL),(2,'Lapsed accounts',NULL,NULL,'Open',0.00,0.00,NULL,NULL,1,'2019-03-31 23:32:02.997337',2,NULL,NULL),(3,'Bank',NULL,NULL,'Open',NULL,0.00,NULL,NULL,1,'2019-03-31 23:32:03.009814',3,NULL,NULL),(4,'Unpaid source',NULL,NULL,'Open',NULL,-100000.00,NULL,NULL,1,'2019-03-31 23:32:03.024182',4,NULL,NULL),(5,'BQ码','','AX31HVN8O5QG','Open',0.00,85000.00,NULL,NULL,1,'2019-04-01 00:04:02.403793',7,NULL,NULL);
/*!40000 ALTER TABLE `oscar_accounts_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oscar_accounts_account_secondary_users`
--

DROP TABLE IF EXISTS `oscar_accounts_account_secondary_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oscar_accounts_account_secondary_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oscar_accounts_account_s_account_id_user_id_87e6566a_uniq` (`account_id`,`user_id`),
  KEY `oscar_accounts_accou_user_id_b4a44a6f_fk_auth_user` (`user_id`),
  CONSTRAINT `oscar_accounts_accou_account_id_5ba1ded6_fk_oscar_acc` FOREIGN KEY (`account_id`) REFERENCES `oscar_accounts_account` (`id`),
  CONSTRAINT `oscar_accounts_accou_user_id_b4a44a6f_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oscar_accounts_account_secondary_users`
--

LOCK TABLES `oscar_accounts_account_secondary_users` WRITE;
/*!40000 ALTER TABLE `oscar_accounts_account_secondary_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `oscar_accounts_account_secondary_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oscar_accounts_accounttype`
--

DROP TABLE IF EXISTS `oscar_accounts_accounttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oscar_accounts_accounttype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `depth` int(10) unsigned NOT NULL,
  `numchild` int(10) unsigned NOT NULL,
  `code` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path` (`path`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oscar_accounts_accounttype`
--

LOCK TABLES `oscar_accounts_accounttype` WRITE;
/*!40000 ALTER TABLE `oscar_accounts_accounttype` DISABLE KEYS */;
INSERT INTO `oscar_accounts_accounttype` VALUES (1,'0001',1,3,NULL,'Assets'),(2,'00010001',2,0,NULL,'Sales'),(3,'00010002',2,0,NULL,'Cash'),(4,'00010003',2,0,NULL,'Unpaid accounts'),(5,'0002',1,1,NULL,'Liabilities'),(6,'00020001',2,1,NULL,'Deferred income'),(7,'000200010001',3,0,NULL,'Dashboard created accounts');
/*!40000 ALTER TABLE `oscar_accounts_accounttype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oscar_accounts_ipaddressrecord`
--

DROP TABLE IF EXISTS `oscar_accounts_ipaddressrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oscar_accounts_ipaddressrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_address` char(39) COLLATE utf8_unicode_ci NOT NULL,
  `total_failures` int(10) unsigned NOT NULL,
  `consecutive_failures` int(10) unsigned NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_last_failure` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip_address` (`ip_address`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oscar_accounts_ipaddressrecord`
--

LOCK TABLES `oscar_accounts_ipaddressrecord` WRITE;
/*!40000 ALTER TABLE `oscar_accounts_ipaddressrecord` DISABLE KEYS */;
INSERT INTO `oscar_accounts_ipaddressrecord` VALUES (1,'127.0.0.1',5,0,'2019-03-18 09:17:36.321192','2019-04-01 13:43:40.872148');
/*!40000 ALTER TABLE `oscar_accounts_ipaddressrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oscar_accounts_transaction`
--

DROP TABLE IF EXISTS `oscar_accounts_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oscar_accounts_transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(12,2) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `account_id` int(11) NOT NULL,
  `transfer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `oscar_accounts_transaction_transfer_id_account_id_051060d4_uniq` (`transfer_id`,`account_id`),
  KEY `oscar_accounts_trans_account_id_c9c544ff_fk_oscar_acc` (`account_id`),
  CONSTRAINT `oscar_accounts_trans_account_id_c9c544ff_fk_oscar_acc` FOREIGN KEY (`account_id`) REFERENCES `oscar_accounts_account` (`id`),
  CONSTRAINT `oscar_accounts_trans_transfer_id_08f32042_fk_oscar_acc` FOREIGN KEY (`transfer_id`) REFERENCES `oscar_accounts_transfer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oscar_accounts_transaction`
--

LOCK TABLES `oscar_accounts_transaction` WRITE;
/*!40000 ALTER TABLE `oscar_accounts_transaction` DISABLE KEYS */;
INSERT INTO `oscar_accounts_transaction` VALUES (1,-100.00,'2019-04-01 00:04:02.506601',4,1),(2,100.00,'2019-04-01 00:04:02.534787',5,1),(3,-11.00,'2019-04-01 00:04:51.106927',4,2),(4,11.00,'2019-04-01 00:04:51.116199',5,2),(5,-1.00,'2019-04-01 00:16:28.822668',5,3),(6,1.00,'2019-04-01 00:16:28.833365',4,3),(7,-110.00,'2019-04-01 00:16:47.708520',5,4),(8,110.00,'2019-04-01 00:16:47.718722',4,4),(9,-100000.00,'2019-04-01 14:01:18.759150',4,5),(10,100000.00,'2019-04-01 14:01:18.769071',5,5),(11,-15000.00,'2019-04-01 14:03:25.611544',5,6),(12,15000.00,'2019-04-01 14:03:25.639214',1,6);
/*!40000 ALTER TABLE `oscar_accounts_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oscar_accounts_transfer`
--

DROP TABLE IF EXISTS `oscar_accounts_transfer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oscar_accounts_transfer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reference` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `amount` decimal(12,2) NOT NULL,
  `merchant_reference` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `username` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `destination_id` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `source_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reference` (`reference`),
  KEY `oscar_accounts_trans_destination_id_540bd15f_fk_oscar_acc` (`destination_id`),
  KEY `oscar_accounts_trans_parent_id_e1d7ef5b_fk_oscar_acc` (`parent_id`),
  KEY `oscar_accounts_trans_source_id_0f016dfb_fk_oscar_acc` (`source_id`),
  KEY `oscar_accounts_transfer_user_id_c34c8716_fk_auth_user_id` (`user_id`),
  CONSTRAINT `oscar_accounts_trans_destination_id_540bd15f_fk_oscar_acc` FOREIGN KEY (`destination_id`) REFERENCES `oscar_accounts_account` (`id`),
  CONSTRAINT `oscar_accounts_trans_parent_id_e1d7ef5b_fk_oscar_acc` FOREIGN KEY (`parent_id`) REFERENCES `oscar_accounts_transfer` (`id`),
  CONSTRAINT `oscar_accounts_trans_source_id_0f016dfb_fk_oscar_acc` FOREIGN KEY (`source_id`) REFERENCES `oscar_accounts_account` (`id`),
  CONSTRAINT `oscar_accounts_transfer_user_id_c34c8716_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oscar_accounts_transfer`
--

LOCK TABLES `oscar_accounts_transfer` WRITE;
/*!40000 ALTER TABLE `oscar_accounts_transfer` DISABLE KEYS */;
INSERT INTO `oscar_accounts_transfer` VALUES (1,'44BD3EEE8EE74CAF4F5384B85D5EBAC9',100.00,NULL,'Creation of account','foonsun','2019-04-01 00:04:02.447642',5,NULL,4,1),(2,'D265B2D400AC133016B975AD65C00F29',11.00,NULL,'Top-up account','foonsun','2019-04-01 00:04:51.086641',5,NULL,4,1),(3,'C095A1C61A582BE8E98F5B2803147E9C',1.00,NULL,'Return funds to source account','foonsun','2019-04-01 00:16:28.802105',4,NULL,5,1),(4,'DE6FE82D233C8CD8036010DA04EB022B',110.00,NULL,'Return funds to source account','foonsun','2019-04-01 00:16:47.688727',4,NULL,5,1),(5,'2D1986C140BB156C54D2C2C82DEFD608',100000.00,NULL,'Top-up account','foonsun','2019-04-01 14:01:18.738788',5,NULL,4,1),(6,'3D1B00DF30A895F57352A302C9343B06',15000.00,'100013','Redeemed to pay for order 100013','foonsun','2019-04-01 14:03:25.557541',1,NULL,5,1);
/*!40000 ALTER TABLE `oscar_accounts_transfer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oscarapi_apikey`
--

DROP TABLE IF EXISTS `oscarapi_apikey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oscarapi_apikey` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oscarapi_apikey`
--

LOCK TABLES `oscarapi_apikey` WRITE;
/*!40000 ALTER TABLE `oscarapi_apikey` DISABLE KEYS */;
/*!40000 ALTER TABLE `oscarapi_apikey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partner_partner`
--

DROP TABLE IF EXISTS `partner_partner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partner_partner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner_partner`
--

LOCK TABLES `partner_partner` WRITE;
/*!40000 ALTER TABLE `partner_partner` DISABLE KEYS */;
INSERT INTO `partner_partner` VALUES (1,'bearquant','bearquant');
/*!40000 ALTER TABLE `partner_partner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partner_partner_users`
--

DROP TABLE IF EXISTS `partner_partner_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partner_partner_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `partner_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `partner_partner_users_partner_id_user_id_9e5c0517_uniq` (`partner_id`,`user_id`),
  KEY `partner_partner_users_user_id_d75d6e40_fk_auth_user_id` (`user_id`),
  CONSTRAINT `partner_partner_users_partner_id_1883dfd9_fk_partner_partner_id` FOREIGN KEY (`partner_id`) REFERENCES `partner_partner` (`id`),
  CONSTRAINT `partner_partner_users_user_id_d75d6e40_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner_partner_users`
--

LOCK TABLES `partner_partner_users` WRITE;
/*!40000 ALTER TABLE `partner_partner_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `partner_partner_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partner_partneraddress`
--

DROP TABLE IF EXISTS `partner_partneraddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partner_partneraddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line1` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line2` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line3` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `line4` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `state` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `postcode` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `search_text` longtext COLLATE utf8_unicode_ci NOT NULL,
  `country_id` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `partner_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `partner_partneraddre_country_id_02c4f979_fk_address_c` (`country_id`),
  KEY `partner_partneraddress_partner_id_59551b0a_fk_partner_partner_id` (`partner_id`),
  CONSTRAINT `partner_partneraddre_country_id_02c4f979_fk_address_c` FOREIGN KEY (`country_id`) REFERENCES `address_country` (`iso_3166_1_a2`),
  CONSTRAINT `partner_partneraddress_partner_id_59551b0a_fk_partner_partner_id` FOREIGN KEY (`partner_id`) REFERENCES `partner_partner` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner_partneraddress`
--

LOCK TABLES `partner_partneraddress` WRITE;
/*!40000 ALTER TABLE `partner_partneraddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `partner_partneraddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partner_stockalert`
--

DROP TABLE IF EXISTS `partner_stockalert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partner_stockalert` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `threshold` int(10) unsigned NOT NULL,
  `status` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_closed` datetime(6) DEFAULT NULL,
  `stockrecord_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `partner_stockalert_stockrecord_id_68ad503a_fk_partner_s` (`stockrecord_id`),
  CONSTRAINT `partner_stockalert_stockrecord_id_68ad503a_fk_partner_s` FOREIGN KEY (`stockrecord_id`) REFERENCES `partner_stockrecord` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner_stockalert`
--

LOCK TABLES `partner_stockalert` WRITE;
/*!40000 ALTER TABLE `partner_stockalert` DISABLE KEYS */;
/*!40000 ALTER TABLE `partner_stockalert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partner_stockrecord`
--

DROP TABLE IF EXISTS `partner_stockrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partner_stockrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `partner_sku` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `price_currency` varchar(12) COLLATE utf8_unicode_ci NOT NULL,
  `price_excl_tax` decimal(12,2) DEFAULT NULL,
  `price_retail` decimal(12,2) DEFAULT NULL,
  `cost_price` decimal(12,2) DEFAULT NULL,
  `num_in_stock` int(10) unsigned DEFAULT NULL,
  `num_allocated` int(11) DEFAULT NULL,
  `low_stock_threshold` int(10) unsigned DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `partner_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `partner_stockrecord_partner_id_partner_sku_8441e010_uniq` (`partner_id`,`partner_sku`),
  KEY `partner_stockrecord_product_id_62fd9e45_fk_catalogue_product_id` (`product_id`),
  KEY `partner_stockrecord_date_updated_e6ae5f14` (`date_updated`),
  CONSTRAINT `partner_stockrecord_partner_id_4155a586_fk_partner_partner_id` FOREIGN KEY (`partner_id`) REFERENCES `partner_partner` (`id`),
  CONSTRAINT `partner_stockrecord_product_id_62fd9e45_fk_catalogue_product_id` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner_stockrecord`
--

LOCK TABLES `partner_stockrecord` WRITE;
/*!40000 ALTER TABLE `partner_stockrecord` DISABLE KEYS */;
INSERT INTO `partner_stockrecord` VALUES (1,'1','RMB',3000.00,3000.00,3000.00,NULL,NULL,NULL,'2019-03-17 13:01:35.594777','2019-03-18 03:07:02.600948',1,3);
/*!40000 ALTER TABLE `partner_stockrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_bankcard`
--

DROP TABLE IF EXISTS `payment_bankcard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_bankcard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `card_type` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `number` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `expiry_date` date NOT NULL,
  `partner_reference` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_bankcard_user_id_08e1d04c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `payment_bankcard_user_id_08e1d04c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_bankcard`
--

LOCK TABLES `payment_bankcard` WRITE;
/*!40000 ALTER TABLE `payment_bankcard` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_bankcard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_source`
--

DROP TABLE IF EXISTS `payment_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `currency` varchar(12) COLLATE utf8_unicode_ci NOT NULL,
  `amount_allocated` decimal(12,2) NOT NULL,
  `amount_debited` decimal(12,2) NOT NULL,
  `amount_refunded` decimal(12,2) NOT NULL,
  `reference` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `label` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `order_id` int(11) NOT NULL,
  `source_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_source_order_id_6b7f2215_fk_order_order_id` (`order_id`),
  KEY `payment_source_source_type_id_700828fe_fk_payment_sourcetype_id` (`source_type_id`),
  CONSTRAINT `payment_source_order_id_6b7f2215_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`),
  CONSTRAINT `payment_source_source_type_id_700828fe_fk_payment_sourcetype_id` FOREIGN KEY (`source_type_id`) REFERENCES `payment_sourcetype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_source`
--

LOCK TABLES `payment_source` WRITE;
/*!40000 ALTER TABLE `payment_source` DISABLE KEYS */;
INSERT INTO `payment_source` VALUES (1,'GBP',0.00,15000.00,0.00,'AX31HVN8O5QG','',2,1);
/*!40000 ALTER TABLE `payment_source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_sourcetype`
--

DROP TABLE IF EXISTS `payment_sourcetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_sourcetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_sourcetype`
--

LOCK TABLES `payment_sourcetype` WRITE;
/*!40000 ALTER TABLE `payment_sourcetype` DISABLE KEYS */;
INSERT INTO `payment_sourcetype` VALUES (1,'Account','account');
/*!40000 ALTER TABLE `payment_sourcetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_transaction`
--

DROP TABLE IF EXISTS `payment_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `txn_type` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `reference` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `status` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `source_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_transaction_source_id_c5ac31e8_fk_payment_source_id` (`source_id`),
  CONSTRAINT `payment_transaction_source_id_c5ac31e8_fk_payment_source_id` FOREIGN KEY (`source_id`) REFERENCES `payment_source` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_transaction`
--

LOCK TABLES `payment_transaction` WRITE;
/*!40000 ALTER TABLE `payment_transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paypal_expresstransaction`
--

DROP TABLE IF EXISTS `paypal_expresstransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paypal_expresstransaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `raw_request` longtext COLLATE utf8_unicode_ci NOT NULL,
  `raw_response` longtext COLLATE utf8_unicode_ci NOT NULL,
  `response_time` double NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `method` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `version` varchar(8) COLLATE utf8_unicode_ci NOT NULL,
  `amount` decimal(12,2) DEFAULT NULL,
  `currency` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ack` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `correlation_id` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `token` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `error_code` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `error_message` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paypal_expresstransaction`
--

LOCK TABLES `paypal_expresstransaction` WRITE;
/*!40000 ALTER TABLE `paypal_expresstransaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `paypal_expresstransaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paypal_payflowtransaction`
--

DROP TABLE IF EXISTS `paypal_payflowtransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paypal_payflowtransaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `raw_request` longtext COLLATE utf8_unicode_ci NOT NULL,
  `raw_response` longtext COLLATE utf8_unicode_ci NOT NULL,
  `response_time` double NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `comment1` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `trxtype` varchar(12) COLLATE utf8_unicode_ci NOT NULL,
  `tender` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `amount` decimal(12,2) DEFAULT NULL,
  `pnref` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ppref` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `result` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `respmsg` varchar(512) COLLATE utf8_unicode_ci NOT NULL,
  `authcode` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `cvv2match` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `avsaddr` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `avszip` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ppref` (`ppref`),
  KEY `paypal_payflowtransaction_comment1_d4d0e6af` (`comment1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paypal_payflowtransaction`
--

LOCK TABLES `paypal_payflowtransaction` WRITE;
/*!40000 ALTER TABLE `paypal_payflowtransaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `paypal_payflowtransaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_automaticproductlist`
--

DROP TABLE IF EXISTS `promotions_automaticproductlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_automaticproductlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `link_url` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `link_text` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `method` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `num_products` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_automaticproductlist`
--

LOCK TABLES `promotions_automaticproductlist` WRITE;
/*!40000 ALTER TABLE `promotions_automaticproductlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_automaticproductlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_handpickedproductlist`
--

DROP TABLE IF EXISTS `promotions_handpickedproductlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_handpickedproductlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `link_url` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `link_text` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_handpickedproductlist`
--

LOCK TABLES `promotions_handpickedproductlist` WRITE;
/*!40000 ALTER TABLE `promotions_handpickedproductlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_handpickedproductlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_image`
--

DROP TABLE IF EXISTS `promotions_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `link_url` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `image` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_image`
--

LOCK TABLES `promotions_image` WRITE;
/*!40000 ALTER TABLE `promotions_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_keywordpromotion`
--

DROP TABLE IF EXISTS `promotions_keywordpromotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_keywordpromotion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(10) unsigned NOT NULL,
  `position` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `display_order` int(10) unsigned NOT NULL,
  `clicks` int(10) unsigned NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `keyword` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `filter` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `promotions_keywordpr_content_type_id_91959aa4_fk_django_co` (`content_type_id`),
  CONSTRAINT `promotions_keywordpr_content_type_id_91959aa4_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_keywordpromotion`
--

LOCK TABLES `promotions_keywordpromotion` WRITE;
/*!40000 ALTER TABLE `promotions_keywordpromotion` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_keywordpromotion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_multiimage`
--

DROP TABLE IF EXISTS `promotions_multiimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_multiimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_multiimage`
--

LOCK TABLES `promotions_multiimage` WRITE;
/*!40000 ALTER TABLE `promotions_multiimage` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_multiimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_multiimage_images`
--

DROP TABLE IF EXISTS `promotions_multiimage_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_multiimage_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `multiimage_id` int(11) NOT NULL,
  `image_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `promotions_multiimage_im_multiimage_id_image_id_29363bca_uniq` (`multiimage_id`,`image_id`),
  KEY `promotions_multiimag_image_id_bb6eca34_fk_promotion` (`image_id`),
  CONSTRAINT `promotions_multiimag_image_id_bb6eca34_fk_promotion` FOREIGN KEY (`image_id`) REFERENCES `promotions_image` (`id`),
  CONSTRAINT `promotions_multiimag_multiimage_id_62ed9a9f_fk_promotion` FOREIGN KEY (`multiimage_id`) REFERENCES `promotions_multiimage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_multiimage_images`
--

LOCK TABLES `promotions_multiimage_images` WRITE;
/*!40000 ALTER TABLE `promotions_multiimage_images` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_multiimage_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_orderedproduct`
--

DROP TABLE IF EXISTS `promotions_orderedproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_orderedproduct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `display_order` int(10) unsigned NOT NULL,
  `list_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `promotions_orderedproduct_list_id_product_id_1e22874a_uniq` (`list_id`,`product_id`),
  KEY `promotions_orderedpr_product_id_94dede36_fk_catalogue` (`product_id`),
  CONSTRAINT `promotions_orderedpr_list_id_94f390b0_fk_promotion` FOREIGN KEY (`list_id`) REFERENCES `promotions_handpickedproductlist` (`id`),
  CONSTRAINT `promotions_orderedpr_product_id_94dede36_fk_catalogue` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_orderedproduct`
--

LOCK TABLES `promotions_orderedproduct` WRITE;
/*!40000 ALTER TABLE `promotions_orderedproduct` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_orderedproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_orderedproductlist`
--

DROP TABLE IF EXISTS `promotions_orderedproductlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_orderedproductlist` (
  `handpickedproductlist_ptr_id` int(11) NOT NULL,
  `display_order` int(10) unsigned NOT NULL,
  `tabbed_block_id` int(11) NOT NULL,
  PRIMARY KEY (`handpickedproductlist_ptr_id`),
  KEY `promotions_orderedpr_tabbed_block_id_a018e8d5_fk_promotion` (`tabbed_block_id`),
  CONSTRAINT `promotions_orderedpr_handpickedproductlis_107cf763_fk_promotion` FOREIGN KEY (`handpickedproductlist_ptr_id`) REFERENCES `promotions_handpickedproductlist` (`id`),
  CONSTRAINT `promotions_orderedpr_tabbed_block_id_a018e8d5_fk_promotion` FOREIGN KEY (`tabbed_block_id`) REFERENCES `promotions_tabbedblock` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_orderedproductlist`
--

LOCK TABLES `promotions_orderedproductlist` WRITE;
/*!40000 ALTER TABLE `promotions_orderedproductlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_orderedproductlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_pagepromotion`
--

DROP TABLE IF EXISTS `promotions_pagepromotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_pagepromotion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(10) unsigned NOT NULL,
  `position` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `display_order` int(10) unsigned NOT NULL,
  `clicks` int(10) unsigned NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `page_url` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `promotions_pagepromo_content_type_id_00707bff_fk_django_co` (`content_type_id`),
  KEY `promotions_pagepromotion_page_url_eee0cc4e` (`page_url`),
  CONSTRAINT `promotions_pagepromo_content_type_id_00707bff_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_pagepromotion`
--

LOCK TABLES `promotions_pagepromotion` WRITE;
/*!40000 ALTER TABLE `promotions_pagepromotion` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_pagepromotion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_rawhtml`
--

DROP TABLE IF EXISTS `promotions_rawhtml`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_rawhtml` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `display_type` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `body` longtext COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_rawhtml`
--

LOCK TABLES `promotions_rawhtml` WRITE;
/*!40000 ALTER TABLE `promotions_rawhtml` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_rawhtml` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_singleproduct`
--

DROP TABLE IF EXISTS `promotions_singleproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_singleproduct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `promotions_singlepro_product_id_d7ad5e03_fk_catalogue` (`product_id`),
  CONSTRAINT `promotions_singlepro_product_id_d7ad5e03_fk_catalogue` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_singleproduct`
--

LOCK TABLES `promotions_singleproduct` WRITE;
/*!40000 ALTER TABLE `promotions_singleproduct` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_singleproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_tabbedblock`
--

DROP TABLE IF EXISTS `promotions_tabbedblock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotions_tabbedblock` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_tabbedblock`
--

LOCK TABLES `promotions_tabbedblock` WRITE;
/*!40000 ALTER TABLE `promotions_tabbedblock` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_tabbedblock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quant_policy`
--

DROP TABLE IF EXISTS `quant_policy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quant_policy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `price` double NOT NULL,
  `content` longtext COLLATE utf8_unicode_ci NOT NULL,
  `exchanges` longtext COLLATE utf8_unicode_ci NOT NULL,
  `status` int(11) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quant_policy`
--

LOCK TABLES `quant_policy` WRITE;
/*!40000 ALTER TABLE `quant_policy` DISABLE KEYS */;
/*!40000 ALTER TABLE `quant_policy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quant_policy_order`
--

DROP TABLE IF EXISTS `quant_policy_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quant_policy_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `policy_id` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `policy_start_time` datetime(6) NOT NULL,
  `policy_end_time` datetime(6) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `policy_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `policy_url_add` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `policy_url_list` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `quant_policy_order_user_id_e9878b6b_fk_auth_user_id` (`user_id`),
  CONSTRAINT `quant_policy_order_user_id_e9878b6b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quant_policy_order`
--

LOCK TABLES `quant_policy_order` WRITE;
/*!40000 ALTER TABLE `quant_policy_order` DISABLE KEYS */;
INSERT INTO `quant_policy_order` VALUES (1,'3','2019-04-01 14:03:25.860806','2020-09-22 14:03:25.860806','2019-04-01 14:41:53.349359','2019-04-01 14:59:04.588218','经典对敲挖矿交易策略','manage_addduiqiao','manage_getduiqiaolist',1);
/*!40000 ALTER TABLE `quant_policy_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_productreview`
--

DROP TABLE IF EXISTS `reviews_productreview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reviews_productreview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `score` smallint(6) NOT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `body` longtext COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8_unicode_ci NOT NULL,
  `homepage` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `status` smallint(6) NOT NULL,
  `total_votes` int(11) NOT NULL,
  `delta_votes` int(11) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reviews_productreview_product_id_user_id_c4fdc4cd_uniq` (`product_id`,`user_id`),
  KEY `reviews_productreview_user_id_8acb5ddd_fk_auth_user_id` (`user_id`),
  KEY `reviews_productreview_delta_votes_bd8ffc87` (`delta_votes`),
  CONSTRAINT `reviews_productrevie_product_id_52e52a32_fk_catalogue` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`),
  CONSTRAINT `reviews_productreview_user_id_8acb5ddd_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_productreview`
--

LOCK TABLES `reviews_productreview` WRITE;
/*!40000 ALTER TABLE `reviews_productreview` DISABLE KEYS */;
INSERT INTO `reviews_productreview` VALUES (1,4,'测试','不错啊','','','',1,0,0,'2019-03-18 02:51:27.178412',3,1);
/*!40000 ALTER TABLE `reviews_productreview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_vote`
--

DROP TABLE IF EXISTS `reviews_vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reviews_vote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delta` smallint(6) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `review_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reviews_vote_user_id_review_id_bb858939_uniq` (`user_id`,`review_id`),
  KEY `reviews_vote_review_id_371b2d8d_fk_reviews_productreview_id` (`review_id`),
  CONSTRAINT `reviews_vote_review_id_371b2d8d_fk_reviews_productreview_id` FOREIGN KEY (`review_id`) REFERENCES `reviews_productreview` (`id`),
  CONSTRAINT `reviews_vote_user_id_5fb87b53_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_vote`
--

LOCK TABLES `reviews_vote` WRITE;
/*!40000 ALTER TABLE `reviews_vote` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews_vote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sanjiao`
--

DROP TABLE IF EXISTS `sanjiao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sanjiao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exchange` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `accesskey` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `secretkey` longtext COLLATE utf8_unicode_ci NOT NULL,
  `symbol` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `max_buy_price` double NOT NULL,
  `min_sell_price` double NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `status` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `operation` int(11) NOT NULL,
  `symbol1` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `symbol2` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `base_volume` double NOT NULL,
  `min_percent` double NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sanjiao_user_id_e421519c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `sanjiao_user_id_e421519c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sanjiao`
--

LOCK TABLES `sanjiao` WRITE;
/*!40000 ALTER TABLE `sanjiao` DISABLE KEYS */;
/*!40000 ALTER TABLE `sanjiao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping_orderanditemcharges`
--

DROP TABLE IF EXISTS `shipping_orderanditemcharges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_orderanditemcharges` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `price_per_order` decimal(12,2) NOT NULL,
  `price_per_item` decimal(12,2) NOT NULL,
  `free_shipping_threshold` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipping_orderanditemcharges`
--

LOCK TABLES `shipping_orderanditemcharges` WRITE;
/*!40000 ALTER TABLE `shipping_orderanditemcharges` DISABLE KEYS */;
/*!40000 ALTER TABLE `shipping_orderanditemcharges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping_orderanditemcharges_countries`
--

DROP TABLE IF EXISTS `shipping_orderanditemcharges_countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_orderanditemcharges_countries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orderanditemcharges_id` int(11) NOT NULL,
  `country_id` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shipping_orderanditemcha_orderanditemcharges_id_c_9f0c9c8f_uniq` (`orderanditemcharges_id`,`country_id`),
  KEY `shipping_orderandite_country_id_30387f2e_fk_address_c` (`country_id`),
  CONSTRAINT `shipping_orderandite_country_id_30387f2e_fk_address_c` FOREIGN KEY (`country_id`) REFERENCES `address_country` (`iso_3166_1_a2`),
  CONSTRAINT `shipping_orderandite_orderanditemcharges__bf5bfee9_fk_shipping_` FOREIGN KEY (`orderanditemcharges_id`) REFERENCES `shipping_orderanditemcharges` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipping_orderanditemcharges_countries`
--

LOCK TABLES `shipping_orderanditemcharges_countries` WRITE;
/*!40000 ALTER TABLE `shipping_orderanditemcharges_countries` DISABLE KEYS */;
/*!40000 ALTER TABLE `shipping_orderanditemcharges_countries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping_weightband`
--

DROP TABLE IF EXISTS `shipping_weightband`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_weightband` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `upper_limit` decimal(12,3) NOT NULL,
  `charge` decimal(12,2) NOT NULL,
  `method_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `shipping_weightband_method_id_b699a1ba_fk_shipping_` (`method_id`),
  CONSTRAINT `shipping_weightband_method_id_b699a1ba_fk_shipping_` FOREIGN KEY (`method_id`) REFERENCES `shipping_weightbased` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipping_weightband`
--

LOCK TABLES `shipping_weightband` WRITE;
/*!40000 ALTER TABLE `shipping_weightband` DISABLE KEYS */;
/*!40000 ALTER TABLE `shipping_weightband` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping_weightbased`
--

DROP TABLE IF EXISTS `shipping_weightbased`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_weightbased` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `default_weight` decimal(12,3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipping_weightbased`
--

LOCK TABLES `shipping_weightbased` WRITE;
/*!40000 ALTER TABLE `shipping_weightbased` DISABLE KEYS */;
/*!40000 ALTER TABLE `shipping_weightbased` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping_weightbased_countries`
--

DROP TABLE IF EXISTS `shipping_weightbased_countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_weightbased_countries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weightbased_id` int(11) NOT NULL,
  `country_id` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shipping_weightbased_cou_weightbased_id_country_i_de8c5e42_uniq` (`weightbased_id`,`country_id`),
  KEY `shipping_weightbased_country_id_06117384_fk_address_c` (`country_id`),
  CONSTRAINT `shipping_weightbased_country_id_06117384_fk_address_c` FOREIGN KEY (`country_id`) REFERENCES `address_country` (`iso_3166_1_a2`),
  CONSTRAINT `shipping_weightbased_weightbased_id_93e3132f_fk_shipping_` FOREIGN KEY (`weightbased_id`) REFERENCES `shipping_weightbased` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipping_weightbased_countries`
--

LOCK TABLES `shipping_weightbased_countries` WRITE;
/*!40000 ALTER TABLE `shipping_weightbased_countries` DISABLE KEYS */;
/*!40000 ALTER TABLE `shipping_weightbased_countries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `uid` varchar(191) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `client_id` varchar(191) COLLATE utf8_unicode_ci NOT NULL,
  `secret` varchar(191) COLLATE utf8_unicode_ci NOT NULL,
  `key` varchar(191) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `socialapp_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` longtext COLLATE utf8_unicode_ci NOT NULL,
  `token_secret` longtext COLLATE utf8_unicode_ci NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `app_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thumbnail_kvstore`
--

DROP TABLE IF EXISTS `thumbnail_kvstore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `thumbnail_kvstore` (
  `key` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `value` longtext COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thumbnail_kvstore`
--

LOCK TABLES `thumbnail_kvstore` WRITE;
/*!40000 ALTER TABLE `thumbnail_kvstore` DISABLE KEYS */;
INSERT INTO `thumbnail_kvstore` VALUES ('sorl-thumbnail||image||0dd695ae96adf46a7de7e73128c88d0b','{\"name\": \"images/products/2019/03/duiqiao.gif\", \"storage\": \"django.core.files.storage.FileSystemStorage\", \"size\": [400, 300]}'),('sorl-thumbnail||image||37419a1ab42a785a4d121c7b282e2497','{\"name\": \"cache/da/49/da498dd750eda56d1752cd02238b820a.jpg\", \"storage\": \"django.core.files.storage.FileSystemStorage\", \"size\": [100, 75]}'),('sorl-thumbnail||image||3f1f4803bcc471dba9a96f80b7a00aee','{\"name\": \"cache/80/01/8001f7d2cb102d0c59d5271abee07b33.jpg\", \"storage\": \"django.core.files.storage.FileSystemStorage\", \"size\": [400, 300]}'),('sorl-thumbnail||image||57f29dd72d90d9ca45ec6120c9d48af1','{\"name\": \"cache/67/b7/67b7e95ade589b69e8ae692bf678815c.jpg\", \"storage\": \"django.core.files.storage.FileSystemStorage\", \"size\": [207, 155]}'),('sorl-thumbnail||image||a9471d16ac23a9bfb11b84600a10f67f','{\"name\": \"cache/c3/f9/c3f9a9e5ba5b6112b3d60c847aca2eae.jpg\", \"storage\": \"django.core.files.storage.FileSystemStorage\", \"size\": [70, 52]}'),('sorl-thumbnail||image||b7a0ab9ed4cb19cde9477a5c3bcf3f59','{\"name\": \"cache/fc/6e/fc6e446f11817da4abc1a0c1a89901e3.jpg\", \"storage\": \"django.core.files.storage.FileSystemStorage\", \"size\": [200, 150]}'),('sorl-thumbnail||thumbnails||0dd695ae96adf46a7de7e73128c88d0b','[\"37419a1ab42a785a4d121c7b282e2497\", \"3f1f4803bcc471dba9a96f80b7a00aee\", \"a9471d16ac23a9bfb11b84600a10f67f\"]');
/*!40000 ALTER TABLE `thumbnail_kvstore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voucher_voucher`
--

DROP TABLE IF EXISTS `voucher_voucher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `voucher_voucher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `code` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `usage` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `start_datetime` datetime(6) NOT NULL,
  `end_datetime` datetime(6) NOT NULL,
  `num_basket_additions` int(10) unsigned NOT NULL,
  `num_orders` int(10) unsigned NOT NULL,
  `total_discount` decimal(12,2) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `voucher_set_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `voucher_voucher_voucher_set_id_17b96a54_fk_voucher_voucherset_id` (`voucher_set_id`),
  CONSTRAINT `voucher_voucher_voucher_set_id_17b96a54_fk_voucher_voucherset_id` FOREIGN KEY (`voucher_set_id`) REFERENCES `voucher_voucherset` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voucher_voucher`
--

LOCK TABLES `voucher_voucher` WRITE;
/*!40000 ALTER TABLE `voucher_voucher` DISABLE KEYS */;
/*!40000 ALTER TABLE `voucher_voucher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voucher_voucher_offers`
--

DROP TABLE IF EXISTS `voucher_voucher_offers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `voucher_voucher_offers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `voucher_id` int(11) NOT NULL,
  `conditionaloffer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `voucher_voucher_offers_voucher_id_conditionalof_01628a7f_uniq` (`voucher_id`,`conditionaloffer_id`),
  KEY `voucher_voucher_offe_conditionaloffer_id_f9682bfb_fk_offer_con` (`conditionaloffer_id`),
  CONSTRAINT `voucher_voucher_offe_conditionaloffer_id_f9682bfb_fk_offer_con` FOREIGN KEY (`conditionaloffer_id`) REFERENCES `offer_conditionaloffer` (`id`),
  CONSTRAINT `voucher_voucher_offers_voucher_id_7f9c575d_fk_voucher_voucher_id` FOREIGN KEY (`voucher_id`) REFERENCES `voucher_voucher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voucher_voucher_offers`
--

LOCK TABLES `voucher_voucher_offers` WRITE;
/*!40000 ALTER TABLE `voucher_voucher_offers` DISABLE KEYS */;
/*!40000 ALTER TABLE `voucher_voucher_offers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voucher_voucherapplication`
--

DROP TABLE IF EXISTS `voucher_voucherapplication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `voucher_voucherapplication` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `order_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `voucher_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `voucher_voucherapplication_order_id_30248a05_fk_order_order_id` (`order_id`),
  KEY `voucher_voucherapplication_user_id_df53a393_fk_auth_user_id` (`user_id`),
  KEY `voucher_voucherappli_voucher_id_5204edb7_fk_voucher_v` (`voucher_id`),
  CONSTRAINT `voucher_voucherappli_voucher_id_5204edb7_fk_voucher_v` FOREIGN KEY (`voucher_id`) REFERENCES `voucher_voucher` (`id`),
  CONSTRAINT `voucher_voucherapplication_order_id_30248a05_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`),
  CONSTRAINT `voucher_voucherapplication_user_id_df53a393_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voucher_voucherapplication`
--

LOCK TABLES `voucher_voucherapplication` WRITE;
/*!40000 ALTER TABLE `voucher_voucherapplication` DISABLE KEYS */;
/*!40000 ALTER TABLE `voucher_voucherapplication` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voucher_voucherset`
--

DROP TABLE IF EXISTS `voucher_voucherset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `voucher_voucherset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `count` int(10) unsigned NOT NULL,
  `code_length` int(11) NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `start_datetime` datetime(6) NOT NULL,
  `end_datetime` datetime(6) NOT NULL,
  `offer_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `offer_id` (`offer_id`),
  CONSTRAINT `voucher_voucherset_offer_id_1d10d5d6_fk_offer_con` FOREIGN KEY (`offer_id`) REFERENCES `offer_conditionaloffer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voucher_voucherset`
--

LOCK TABLES `voucher_voucherset` WRITE;
/*!40000 ALTER TABLE `voucher_voucherset` DISABLE KEYS */;
/*!40000 ALTER TABLE `voucher_voucherset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlists_line`
--

DROP TABLE IF EXISTS `wishlists_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wishlists_line` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quantity` int(10) unsigned NOT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `wishlist_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wishlists_line_wishlist_id_product_id_78f04673_uniq` (`wishlist_id`,`product_id`),
  KEY `wishlists_line_product_id_9d6d9b37_fk_catalogue_product_id` (`product_id`),
  CONSTRAINT `wishlists_line_product_id_9d6d9b37_fk_catalogue_product_id` FOREIGN KEY (`product_id`) REFERENCES `catalogue_product` (`id`),
  CONSTRAINT `wishlists_line_wishlist_id_4cffe302_fk_wishlists_wishlist_id` FOREIGN KEY (`wishlist_id`) REFERENCES `wishlists_wishlist` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlists_line`
--

LOCK TABLES `wishlists_line` WRITE;
/*!40000 ALTER TABLE `wishlists_line` DISABLE KEYS */;
/*!40000 ALTER TABLE `wishlists_line` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlists_wishlist`
--

DROP TABLE IF EXISTS `wishlists_wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wishlists_wishlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `key` varchar(6) COLLATE utf8_unicode_ci NOT NULL,
  `visibility` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `owner_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `wishlists_wishlist_owner_id_d5464c62_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `wishlists_wishlist_owner_id_d5464c62_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlists_wishlist`
--

LOCK TABLES `wishlists_wishlist` WRITE;
/*!40000 ALTER TABLE `wishlists_wishlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `wishlists_wishlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-13 11:23:19
