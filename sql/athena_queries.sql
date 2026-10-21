-- Example Athena queries over the table created by the Glue crawler.
-- Replace stock_market_db.stock_ticks with the database and table your crawler created.

-- Latest ticks
SELECT "index", "date", open, high, low, close, volume
FROM stock_market_db.stock_ticks
ORDER BY "date" DESC
LIMIT 20;

-- Average closing price (USD) per index
SELECT "index", ROUND(AVG(closeusd), 2) AS avg_close_usd, COUNT(*) AS ticks
FROM stock_market_db.stock_ticks
GROUP BY "index"
ORDER BY avg_close_usd DESC;

-- Daily trading range per index
SELECT "index", "date", ROUND(high - low, 2) AS daily_range
FROM stock_market_db.stock_ticks
ORDER BY daily_range DESC
LIMIT 10;
