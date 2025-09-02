-- Validation queries for Indian market data - adapted from original project

-- Create link table for Indian data (similar to original project)
CREATE TABLE IF NOT EXISTS `yahoo_india_link_table` (
  `symbol` varchar(100) NOT NULL,
  `link_date` date NOT NULL,
  `adj_ratio` double,
  PRIMARY KEY (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;

-- Populate link table for Indian stocks
INSERT IGNORE INTO yahoo_india_link_table (symbol, link_date)
SELECT symbol, MAX(tradedate) as link_date 
FROM yahoo_a_stock_eod_price
WHERE VOLUME > 0 AND symbol IN (
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR',
    'ICICIBANK', 'KOTAKBANK', 'LT', 'SBIN', 'BHARTIARTL',
    'ITC', 'ASIANPAINT', 'AXISBANK', 'MARUTI', 'NESTLEIND',
    'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'WIPRO', 'POWERGRID'
)
GROUP BY symbol;

-- Change symbol to upper case (matching original project)
UPDATE yahoo_india_link_table SET symbol = UPPER(symbol);
UPDATE yahoo_a_stock_eod_price SET symbol = UPPER(symbol);

-- Set initial adj_ratio to 1 for Indian stocks (since we're starting fresh)
UPDATE yahoo_india_link_table SET adj_ratio = 1.0 WHERE adj_ratio IS NULL;

-- Validation: Check data completeness
SELECT 
    symbol,
    COUNT(*) as record_count,
    MIN(tradedate) as first_date,
    MAX(tradedate) as last_date
FROM yahoo_a_stock_eod_price 
WHERE symbol IN (
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR',
    'ICICIBANK', 'KOTAKBANK', 'LT', 'SBIN', 'BHARTIARTL',
    'ITC', 'ASIANPAINT', 'AXISBANK', 'MARUTI', 'NESTLEIND',
    'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'WIPRO', 'POWERGRID'
)
GROUP BY symbol
ORDER BY symbol;

-- Validation: Check for missing data
SELECT 
    symbol,
    COUNT(*) as missing_days
FROM (
    SELECT DISTINCT tradedate 
    FROM yahoo_a_stock_eod_price 
    WHERE tradedate >= '2024-01-01'
) all_dates
CROSS JOIN (
    SELECT DISTINCT symbol 
    FROM yahoo_a_stock_eod_price 
    WHERE symbol IN (
        'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR',
        'ICICIBANK', 'KOTAKBANK', 'LT', 'SBIN', 'BHARTIARTL',
        'ITC', 'ASIANPAINT', 'AXISBANK', 'MARUTI', 'NESTLEIND',
        'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'WIPRO', 'POWERGRID'
    )
) all_stocks
LEFT JOIN yahoo_a_stock_eod_price yp ON all_dates.tradedate = yp.tradedate AND all_stocks.symbol = yp.symbol
WHERE yp.tradedate IS NULL
GROUP BY symbol
ORDER BY missing_days DESC;

-- Validation: Check for data quality issues
SELECT 
    symbol,
    tradedate,
    CASE 
        WHEN high < low THEN 'High < Low'
        WHEN high < open THEN 'High < Open'
        WHEN high < close THEN 'High < Close'
        WHEN low > open THEN 'Low > Open'
        WHEN low > close THEN 'Low > Close'
        WHEN volume < 0 THEN 'Negative Volume'
        WHEN close <= 0 THEN 'Zero/Negative Close'
        ELSE 'OK'
    END as issue
FROM yahoo_a_stock_eod_price
WHERE symbol IN (
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR',
    'ICICIBANK', 'KOTAKBANK', 'LT', 'SBIN', 'BHARTIARTL',
    'ITC', 'ASIANPAINT', 'AXISBANK', 'MARUTI', 'NESTLEIND',
    'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'WIPRO', 'POWERGRID'
)
AND (
    high < low OR high < open OR high < close OR
    low > open OR low > close OR volume < 0 OR close <= 0
)
ORDER BY symbol, tradedate;

-- Validation: Check index data completeness
SELECT 
    index_code,
    COUNT(*) as record_count,
    MIN(trade_date) as first_date,
    MAX(trade_date) as last_date
FROM yahoo_index_eod_price 
GROUP BY index_code
ORDER BY index_code;
