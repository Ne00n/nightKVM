SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `jobs` (
  `ID` varchar(16) NOT NULL,
  `Task` varchar(10) NOT NULL,
  `Node` varchar(20) NOT NULL,
  `Package` varchar(20) DEFAULT NULL,
  `Status` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `machines` (
  `Name` varchar(20) NOT NULL,
  `Node` varchar(20) NOT NULL,
  `Status` int(11) NOT NULL DEFAULT -1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `nodes` (
  `Name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `packages` (
  `Name` varchar(20) NOT NULL,
  `CPU` int(11) NOT NULL,
  `Memory` int(11) NOT NULL,
  `Disk` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE `jobs`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `jobsNodes` (`Node`),
  ADD KEY `jobsPackages` (`Package`);

ALTER TABLE `machines`
  ADD PRIMARY KEY (`Name`),
  ADD KEY `machinesNodes` (`Node`);

ALTER TABLE `nodes`
  ADD PRIMARY KEY (`Name`);

ALTER TABLE `packages`
  ADD PRIMARY KEY (`Name`);


ALTER TABLE `jobs`
  ADD CONSTRAINT `jobsNodes` FOREIGN KEY (`Node`) REFERENCES `nodes` (`Name`) ON UPDATE CASCADE,
  ADD CONSTRAINT `jobsPackages` FOREIGN KEY (`Package`) REFERENCES `packages` (`Name`) ON UPDATE CASCADE;

ALTER TABLE `machines`
  ADD CONSTRAINT `machinesNodes` FOREIGN KEY (`Node`) REFERENCES `nodes` (`Name`) ON UPDATE CASCADE;
COMMIT;
