-- Create database for Indian market data
CREATE DATABASE IF NOT EXISTS indian_market_data;
USE indian_market_data;

-- Create stock prices table
CREATE TABLE IF NOT EXISTS indian_stock_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tradedate DATE NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    market ENUM('NSE', 'BSE') NOT NULL,
    open DECIMAL(10,2),
    high DECIMAL(10,2),
    low DECIMAL(10,2),
    close DECIMAL(10,2),
    volume BIGINT,
    adjclose DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_symbol_date (symbol, tradedate),
    INDEX idx_tradedate (tradedate),
    INDEX idx_market (market)
);

-- Create stock list table
CREATE TABLE IF NOT EXISTS indian_stock_list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL UNIQUE,
    stock_code VARCHAR(20) NOT NULL,
    market ENUM('NSE', 'BSE') NOT NULL,
    name VARCHAR(100),
    sector VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_market (market),
    INDEX idx_stock_code (stock_code)
);

-- Create index weights table (for Nifty, Sensex, etc.)
CREATE TABLE IF NOT EXISTS indian_index_weights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    index_code VARCHAR(20) NOT NULL,
    index_name VARCHAR(50) NOT NULL,
    stock_code VARCHAR(20) NOT NULL,
    weight DECIMAL(8,4),
    trade_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_index_date (index_code, trade_date),
    INDEX idx_stock_code (stock_code)
);

-- Create trading calendar table
CREATE TABLE IF NOT EXISTS indian_trading_calendar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trade_date DATE NOT NULL UNIQUE,
    is_trading_day BOOLEAN DEFAULT TRUE,
    market_holiday VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_trade_date (trade_date)
);

-- Insert some sample trading calendar data
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
('2024-11-15', FALSE, 'Guru Nanak Jayanti');
