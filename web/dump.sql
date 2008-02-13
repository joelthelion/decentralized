-- MySQL dump 10.11
--
-- Host: localhost    Database: prout
-- ------------------------------------------------------
-- Server version	5.0.32-Debian_7etch5-log

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
-- Table structure for table `bayes_data`
--

DROP TABLE IF EXISTS `bayes_data`;
CREATE TABLE `bayes_data` (
  `user_id` int(11) NOT NULL default '0',
  `symbol` varchar(255) NOT NULL default '',
  `good_count` int(11) default NULL,
  `bad_count` int(11) default NULL,
  PRIMARY KEY  (`user_id`,`symbol`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `bayes_data`
--

LOCK TABLES `bayes_data` WRITE;
/*!40000 ALTER TABLE `bayes_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `bayes_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feed`
--

DROP TABLE IF EXISTS `feed`;
CREATE TABLE `feed` (
  `id` int(11) NOT NULL auto_increment,
  `url` mediumtext,
  `url_md5` char(32) default NULL,
  `fetch_date` datetime default NULL,
  `hit_count` int(11) default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `url_md5` (`url_md5`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `feed`
--

LOCK TABLES `feed` WRITE;
/*!40000 ALTER TABLE `feed` DISABLE KEYS */;
INSERT INTO `feed` VALUES (1,'http://delicious.com/rss/tag/color','a6e2da4534fb1546e95c1e6e34b2c298',NULL,0),(2,'http://delicious.com/rss/tag/china','993b5d3c53b04767de43898dab6452f6',NULL,0),(3,'http://delicious.com/rss/tag/arab','8f7fce248b25928b29433591ebda22ac',NULL,0),(4,'http://delicious.com/rss/tag/hebrew','a426d51aef8188452735f52f31aa5e8f',NULL,0);
/*!40000 ALTER TABLE `feed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feed_story`
--

DROP TABLE IF EXISTS `feed_story`;
CREATE TABLE `feed_story` (
  `story_id` int(11) NOT NULL default '0',
  `feed_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`story_id`,`feed_id`),
  KEY `feed_id` (`feed_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `feed_story`
--

LOCK TABLES `feed_story` WRITE;
/*!40000 ALTER TABLE `feed_story` DISABLE KEYS */;
/*!40000 ALTER TABLE `feed_story` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kolmognus_user`
--

DROP TABLE IF EXISTS `kolmognus_user`;
CREATE TABLE `kolmognus_user` (
  `id` int(11) NOT NULL auto_increment,
  `login` varchar(30) default NULL,
  `pass` char(41) default NULL,
  `last_login_date` datetime default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `kolmognus_user`
--

LOCK TABLES `kolmognus_user` WRITE;
/*!40000 ALTER TABLE `kolmognus_user` DISABLE KEYS */;
INSERT INTO `kolmognus_user` VALUES (1,'joel','*0D3CED9BEC10A777AEC23CCC353A8C08A633045E',NULL),(2,'pierre','*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29',NULL);
/*!40000 ALTER TABLE `kolmognus_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recommended_story`
--

DROP TABLE IF EXISTS `recommended_story`;
CREATE TABLE `recommended_story` (
  `user_id` int(11) NOT NULL default '0',
  `story_id` int(11) NOT NULL default '0',
  `computed_rating` float default NULL,
  `user_rating` enum('G','B','?') default '?',
  `learned` tinyint(1) default NULL,
  PRIMARY KEY  (`user_id`,`story_id`),
  KEY `story_id` (`story_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `recommended_story`
--

LOCK TABLES `recommended_story` WRITE;
/*!40000 ALTER TABLE `recommended_story` DISABLE KEYS */;
INSERT INTO `recommended_story` VALUES (1,1,0.5,'?',NULL),(2,1,0.5,'?',NULL);
/*!40000 ALTER TABLE `recommended_story` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
CREATE TABLE `service` (
  `name` varchar(64) NOT NULL,
  `status` varchar(512) default NULL,
  PRIMARY KEY  (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `service`
--

LOCK TABLES `service` WRITE;
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
INSERT INTO `service` VALUES ('fetcher','db reset');
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `story`
--

DROP TABLE IF EXISTS `story`;
CREATE TABLE `story` (
  `id` int(11) NOT NULL auto_increment,
  `url` mediumtext,
  `url_md5` char(32) default NULL,
  `symbols` text,
  `symbol_count` int(11) default NULL,
  `fetch_date` datetime default NULL,
  `hit_count` int(11) default NULL,
  `rated_date` datetime default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `url_md5` (`url_md5`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `story`
--

LOCK TABLES `story` WRITE;
/*!40000 ALTER TABLE `story` DISABLE KEYS */;
INSERT INTO `story` VALUES (1,'http://coincalin.com','fd0ba363e5f5af5eb0443c71a76f971d','coin calin',2,'2008-02-13 21:56:03',1,'2008-02-13 21:56:08');
/*!40000 ALTER TABLE `story` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2008-02-13 22:12:31
