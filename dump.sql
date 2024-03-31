SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `jobs` (
  `ID` varchar(16) NOT NULL,
  `Node` varchar(20) NOT NULL,
  `User` varchar(20) NOT NULL,
  `Package` varchar(20) DEFAULT NULL,
  `Task` varchar(10) NOT NULL,
  `Status` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `machines` (
  `Name` varchar(20) NOT NULL,
  `Node` varchar(20) NOT NULL,
  `User` varchar(20) DEFAULT NULL,
  `Status` int(11) NOT NULL DEFAULT -1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `nodes` (
  `Name` varchar(20) NOT NULL,
  `Token` varchar(33) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `packages` (
  `Name` varchar(20) NOT NULL,
  `CPU` int(11) NOT NULL,
  `Memory` int(11) NOT NULL,
  `Disk` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `users` (
  `Username` varchar(20) NOT NULL,
  `Password` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


ALTER TABLE `jobs`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `jobsNodes` (`Node`),
  ADD KEY `jobsPackages` (`Package`),
  ADD KEY `jobsUsers` (`User`);

ALTER TABLE `machines`
  ADD PRIMARY KEY (`Name`),
  ADD KEY `machinesNodes` (`Node`),
  ADD KEY `machinesUsers` (`User`);

ALTER TABLE `nodes`
  ADD PRIMARY KEY (`Name`);

ALTER TABLE `packages`
  ADD PRIMARY KEY (`Name`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`Username`);


ALTER TABLE `jobs`
  ADD CONSTRAINT `jobsNodes` FOREIGN KEY (`Node`) REFERENCES `nodes` (`Name`) ON UPDATE CASCADE,
  ADD CONSTRAINT `jobsPackages` FOREIGN KEY (`Package`) REFERENCES `packages` (`Name`) ON UPDATE CASCADE,
  ADD CONSTRAINT `jobsUsers` FOREIGN KEY (`User`) REFERENCES `users` (`Username`) ON UPDATE CASCADE;

ALTER TABLE `machines`
  ADD CONSTRAINT `machinesNodes` FOREIGN KEY (`Node`) REFERENCES `nodes` (`Name`) ON UPDATE CASCADE,
  ADD CONSTRAINT `machinesUsers` FOREIGN KEY (`User`) REFERENCES `users` (`Username`) ON UPDATE CASCADE;
COMMIT;
