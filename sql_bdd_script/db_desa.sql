-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:8889
-- Généré le : lun. 05 fév. 2024 à 15:53
-- Version du serveur : 5.7.39
-- Version de PHP : 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `db_desa`
--

-- --------------------------------------------------------

--
-- Structure de la table `comment`
--

CREATE TABLE `comment` (
  `id` int(5) NOT NULL,
  `id_user` int(5) NOT NULL,
  `id_media` int(5) NOT NULL,
  `text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `media`
--

CREATE TABLE `media` (
  `id` int(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `path` varchar(100) NOT NULL,
  `date` varchar(30) NOT NULL,
  `download` int(100) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `media`
--

INSERT INTO `media` (`id`, `title`, `path`, `date`, `download`) VALUES
(1, 'Media', '20240201_134910_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_134910', 0),
(2, 'Media', '20240201_142550_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_142550', 0),
(3, 'Test', '20240201_142649_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_142649', 0),
(4, 'Test', '20240201_142722_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_142722', 0),
(5, 'Test', '20240201_142826_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_142826', 0),
(6, 'Test', '20240201_142932_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_142932', 0),
(7, 'Hello', '20240201_143840_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_143840', 0),
(8, 'Hello', '20240201_144143_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_144143', 0),
(9, 'Hello', '20240201_144641_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_144641', 0),
(10, 'Hello', '20240201_144719_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_144719', 0),
(11, 'hey', '20240201_145105_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_145105', 0),
(12, 'hey', '20240201_145134_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_145134', 0),
(13, 'hey', '20240201_145245_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_145245', 0),
(14, 'hey', '20240201_145437_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_145437', 0),
(15, 'hey', '20240201_145548_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_145548', 0),
(16, 'soleil', '20240201_145723_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_145723', 0),
(17, 'soleil', '20240201_145910_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_145910', 0),
(18, 'sol', '20240201_150139_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_150139', 0),
(19, 'sol', '20240201_150203_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_150203', 0),
(20, 'sol', '20240201_150220_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_150220', 0),
(21, 'hey', '20240201_150323_Capture_decran_2024-02-01_a_10.49.08.png', '20240201_150322', 0);

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(11) NOT NULL,
  `firstname` varchar(11) NOT NULL,
  `username` varchar(11) NOT NULL,
  `password` varchar(11) NOT NULL,
  `stateUser` int(11) NOT NULL DEFAULT '1',
  `role` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`id`, `name`, `firstname`, `username`, `password`, `stateUser`, `role`) VALUES
(1, 'Jean', 'Paul', 'jpol', '1234', 1, 2),
(2, 'Marie', 'Sarah', 'nakite', '1234', 2, 1);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_user` (`id_user`),
  ADD KEY `FK_media` (`id_media`);

--
-- Index pour la table `media`
--
ALTER TABLE `media`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `comment`
--
ALTER TABLE `comment`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `media`
--
ALTER TABLE `media`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `FK_media` FOREIGN KEY (`id_media`) REFERENCES `media` (`id`),
  ADD CONSTRAINT `FK_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
