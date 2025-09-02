-- Setup database for Indian market data - adapted from original project
-- This uses the same table structure as the original project for compatibility

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS investment_data;
USE investment_data;

-- Create yahoo_a_stock_eod_price table (same as original project)
CREATE TABLE IF NOT EXISTS `yahoo_a_stock_eod_price` (
  `tradedate` date NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `open` decimal(10,2),
  `high` decimal(10,2),
  `low` decimal(10,2),
  `close` decimal(10,2),
  `volume` bigint,
  `adjclose` decimal(10,2),
  `amount` decimal(15,2),
  PRIMARY KEY (`tradedate`, `symbol`),
  INDEX `idx_symbol` (`symbol`),
  INDEX `idx_tradedate` (`tradedate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;

-- Create yahoo_index_eod_price table (adapted from original project)
CREATE TABLE IF NOT EXISTS `yahoo_index_eod_price` (
  `trade_date` date NOT NULL,
  `index_code` varchar(20) NOT NULL,
  `index_name` varchar(50),
  `open` decimal(10,2),
  `high` decimal(10,2),
  `low` decimal(10,2),
  `close` decimal(10,2),
  `volume` bigint,
  `adjclose` decimal(10,2),
  PRIMARY KEY (`trade_date`, `index_code`),
  INDEX `idx_index_code` (`index_code`),
  INDEX `idx_trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;

-- Create yahoo_stock_list table (adapted from original project)
CREATE TABLE IF NOT EXISTS `yahoo_stock_list` (
  `symbol` varchar(20) NOT NULL PRIMARY KEY,
  `ts_code` varchar(20),
  `name` varchar(100),
  `market` varchar(10),
  `list_date` date,
  `delist_date` date,
  INDEX `idx_market` (`market`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;

-- Create yahoo_index_list table (adapted from original project)
CREATE TABLE IF NOT EXISTS `yahoo_index_list` (
  `index_code` varchar(20) NOT NULL PRIMARY KEY,
  `index_name` varchar(50),
  `market` varchar(10),
  `list_date` date,
  `description` varchar(200),
  INDEX `idx_market` (`market`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;

-- Create yahoo_india_link_table for data validation (adapted from original project)
CREATE TABLE IF NOT EXISTS `yahoo_india_link_table` (
  `symbol` varchar(100) NOT NULL,
  `link_date` date NOT NULL,
  `adj_ratio` double,
  PRIMARY KEY (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;

-- Create final_a_stock_eod_price table (same as original project for compatibility)
CREATE TABLE IF NOT EXISTS `final_a_stock_eod_price` (
  `tradedate` date NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `open` decimal(10,2),
  `high` decimal(10,2),
  `low` decimal(10,2),
  `close` decimal(10,2),
  `volume` bigint,
  `adjclose` decimal(10,2),
  `amount` decimal(15,2),
  PRIMARY KEY (`tradedate`, `symbol`),
  INDEX `idx_symbol` (`symbol`),
  INDEX `idx_tradedate` (`tradedate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;

-- Create trading calendar table (adapted for Indian markets)
CREATE TABLE IF NOT EXISTS `indian_trading_calendar` (
  `trade_date` date NOT NULL PRIMARY KEY,
  `is_trading_day` boolean DEFAULT TRUE,
  `market_holiday` varchar(100),
  INDEX `idx_trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;

-- Insert Indian market holidays
INSERT IGNORE INTO indian_trading_calendar (trade_date, is_trading_day, market_holiday) VALUES
('2024-01-01', FALSE, 'New Year'),
('2024-01-26', FALSE, 'Republic Day'),
('2024-03-08', FALSE, 'Holi'),
('2024-03-29', FALSE, 'Good Friday'),
('2024-04-11', FALSE, 'Eid'),
('2024-04-17', FALSE, 'Ram Navami'),
('2024-05-01', FALSE, 'Labour Day'),
('2024-08-15', FALSE, 'Independence Day'),
('2024-08-26', FALSE, 'Janmashtami'),
('2024-10-02', FALSE, 'Gandhi Jayanti'),
('2024-10-12', FALSE, 'Dussehra'),
('2024-11-01', FALSE, 'Diwali'),
('2024-11-15', FALSE, 'Guru Nanak Jayanti'),
('2025-01-26', FALSE, 'Republic Day'),
('2025-03-14', FALSE, 'Holi'),
('2025-04-18', FALSE, 'Good Friday'),
('2025-03-30', FALSE, 'Eid'),
('2025-04-06', FALSE, 'Ram Navami'),
('2025-05-01', FALSE, 'Labour Day'),
('2025-08-15', FALSE, 'Independence Day'),
('2025-08-15', FALSE, 'Janmashtami'),
('2025-10-02', FALSE, 'Gandhi Jayanti'),
('2025-10-02', FALSE, 'Dussehra'),
('2025-10-20', FALSE, 'Diwali'),
('2025-11-04', FALSE, 'Guru Nanak Jayanti');
