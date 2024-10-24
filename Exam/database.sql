-- MySQL dump 10.13  Distrib 8.0.37, for Linux (x86_64)
--
-- Host: std-mysql    Database: std_2380_exam
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('cf649684faf2');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(11) NOT NULL,
  `publisher` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `length` int(11) NOT NULL,
  `cover_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_books_cover_id_covers` (`cover_id`),
  CONSTRAINT `fk_books_cover_id_covers` FOREIGN KEY (`cover_id`) REFERENCES `covers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (52,1949,'АСТ','Джордж Оруэлл',320,13,'1984','«**1984**» (англ. Nineteen Eighty-Four, «тысяча девятьсот восемьдесят четвертый») — роман-антиутопия Джорджа Оруэлла, изданный в 1949 году. Как отмечает членкор РАН М. Ф. Черныш, это самое главное и последнее произведение писателя.  \n\nРоман «1984» наряду с такими произведениями, как «Мы» Евгения Замятина (1920), «О дивный новый мир» Олдоса Хаксли (1932) и «451 градус по Фаренгейту» Рэя Брэдбери (1953) считается одним из образцов антиутопии.'),(53,1949,'АСТ','Джордж Оруэлл',320,13,'1984','«**1984**» (англ. Nineteen Eighty-Four, «тысяча девятьсот восемьдесят четвертый») — роман-антиутопия Джорджа Оруэлла, изданный в 1949 году. Как отмечает членкор РАН М. Ф. Черныш, это самое главное и последнее произведение писателя.  Роман «1984» наряду с такими произведениями, как «Мы» Евгения Замятина (1920), «О дивный новый мир» Олдоса Хаксли (1932) и «451 градус по Фаренгейту» Рэя Брэдбери (1953) считается одним из образцов антиутопии.'),(61,567,'hghg','ghfrde',43545,13,'hftghg','ghfhgfghfhgf'),(62,567,'hghg','ghfrde',43545,13,'hftghg','ghfhgfghfhgf'),(63,567,'hghg','ghfrde',43545,13,'hftghg','ghfhgfghfhgf'),(64,6767,'hghghgf','dgrfghf',6768,13,'nbnvgbnvgj','fhgdhgdgdh'),(65,6767,'hghghgf','dgrfghf',6768,13,'nbnvgbnvgj','fhgdhgdgdh'),(66,6767,'hghghgf','dgrfghf',6768,13,'nbnvgbnvgj','fhgdhgdgdh'),(67,6767,'hghghgf','dgrfghf',6768,13,'nbnvgbnvgj','fhgdhgdgdh'),(68,6767,'hghghgf','dgrfghf',6768,13,'nbnvgbnvgj','fhgdhgdgdh'),(69,6767,'hghghgf','dgrfghf',6768,13,'nbnvgbnvgj','fhgdhgdgdh'),(70,6767,'hghghgf','dgrfghf',6768,13,'nbnvgbnvgj','fhgdhgdgdh'),(71,6767,'hghghgf','dgrfghf',6768,13,'nbnvgbnvgj','fhgdhgdgdh');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `covers`
--

DROP TABLE IF EXISTS `covers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `covers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `md5_hash` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `covers`
--

LOCK TABLES `covers` WRITE;
/*!40000 ALTER TABLE `covers` DISABLE KEYS */;
INSERT INTO `covers` VALUES (13,'e5f82111504d28779262bf2dca0fad56.png','image/png','e5f82111504d28779262bf2dca0fad56');
/*!40000 ALTER TABLE `covers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genre_to_book`
--

DROP TABLE IF EXISTS `genre_to_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genre_to_book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_genre_to_book_book_id_books` (`book_id`),
  KEY `fk_genre_to_book_genre_id_genres` (`genre_id`),
  CONSTRAINT `fk_genre_to_book_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_genre_to_book_genre_id_genres` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genre_to_book`
--

LOCK TABLES `genre_to_book` WRITE;
/*!40000 ALTER TABLE `genre_to_book` DISABLE KEYS */;
INSERT INTO `genre_to_book` VALUES (143,52,21),(144,52,3),(160,53,21),(161,53,3),(170,61,21),(171,62,21),(172,63,21),(173,64,12),(174,65,12),(175,66,12),(176,67,12),(177,68,12),(178,69,12),(179,70,12),(180,71,12);
/*!40000 ALTER TABLE `genre_to_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_genres_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (17,'Автобиография'),(21,'Антиутопия'),(7,'Биография'),(2,'Детектив'),(12,'Драма'),(8,'История'),(13,'Комедия'),(18,'Мемуары'),(6,'Научная литература'),(11,'Поэзия'),(5,'Приключения'),(9,'Психология'),(3,'Роман'),(20,'Справочник'),(14,'Триллер'),(15,'Ужасы'),(1,'Фантастика'),(10,'Философия'),(4,'Фэнтези'),(19,'Энциклопедия'),(16,'Эссе');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review_status`
--

DROP TABLE IF EXISTS `review_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_review_status_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review_status`
--

LOCK TABLES `review_status` WRITE;
/*!40000 ALTER TABLE `review_status` DISABLE KEYS */;
INSERT INTO `review_status` VALUES (1,'На рассмотрении'),(2,'Одобрено'),(3,'Отклонено');
/*!40000 ALTER TABLE `review_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL,
  `status_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_reviews_book_id_books` (`book_id`),
  KEY `fk_reviews_user_id_users` (`user_id`),
  KEY `fk_reviews_status_id_review_status` (`status_id`),
  CONSTRAINT `fk_reviews_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_reviews_status_id_review_status` FOREIGN KEY (`status_id`) REFERENCES `review_status` (`id`),
  CONSTRAINT `fk_reviews_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (21,53,1,5,'123sdsdfgsdfgsedgsdfgsdf123sdsdfgsdfgsedgsdfgsdf123sdsdfgsdfgsedgsdfgsdf123sdsdfgsdfgsedgsdfgsdf123sdsdfgsdfgsedgsdfgsdf123sdsdfgsdfgsedgsdfgsdf123sdsdfgsdfgsedgsdfgsdf','2024-06-04 14:51:05',2),(24,52,3,5,'567123sdsdfgsdf','2024-06-04 16:55:54',2),(26,52,1,5,'gyhjmyhgjhjh','2024-06-04 18:05:06',3),(29,63,1,5,'ghfhgghfhg','2024-06-04 18:18:58',2),(30,61,1,5,'hvhgfghdhgfh','2024-06-04 18:19:47',2),(31,62,1,5,'ghfghghghfghf','2024-06-04 18:19:56',2),(32,62,1,5,'ghfghghghfghf','2024-06-04 18:19:58',2),(33,64,1,5,'hjhgkhgkhgk','2024-06-04 18:21:09',2),(34,71,1,5,'hjhgkgjhkgh','2024-06-04 18:21:30',2),(35,65,1,5,'hkkhgkhgh','2024-06-04 18:21:45',2),(36,66,1,5,'hkgkghkhkhg','2024-06-04 18:21:54',2),(37,66,1,5,'hkgkghkhkhg','2024-06-04 18:21:56',2),(38,67,1,5,'khgkhgkkh','2024-06-04 18:22:03',2),(39,68,1,5,'hkkhgkghkhg','2024-06-04 18:22:10',2),(40,69,1,5,'khgkhkhghkg','2024-06-04 18:22:17',2),(41,70,1,5,'hkgkhkhg','2024-06-04 18:22:23',2);
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `desc` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_roles_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Администратор','Суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),(2,'Модератор','Может редактировать данные книг и производить модерацию рецензий'),(3,'Пользователь','Может оставлять рецензии');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(100) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_login` (`login`),
  KEY `fk_users_role_id_roles` (`role_id`),
  CONSTRAINT `fk_users_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','scrypt:32768:8:1$lEhYws8C2g40QjCh$fd36ff4c8e874ab7fca114f675d77d6b4c30f15f4ab9547fa0abb6711162435dd8d4cd478edcaeb9a89f8e49c1eeada8cbc82444d668e6a36d159fe451439b20','admin','admin',NULL,1),(2,'moderator','scrypt:32768:8:1$s66g5HI0fq94owog$2eb383923b1b03865d889127274d1729d0ed1ea146b3b003fd9897f6dc207cccfa866a37bfd27da82ac992338180dcbfdfcbadfd4689619db3dcd1df4f198528','moderator','moderator',NULL,2),(3,'user','scrypt:32768:8:1$0KOB7myGKDeHKMad$9dbe2c9933ddafa6b431a2b092b89c519548815f726325deafe73f45ecc6c32966e298a6b3b32f57b00fa42364335ee596c01a6018226472e43e727566076cb4','user','user',NULL,3);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-24 17:26:39
