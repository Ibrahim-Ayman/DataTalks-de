NYC Yellow Taxi – DLT Homework
==============================

This document contains answers and SQL queries for the NYC Yellow Taxi DLT homework.

## Question 1

**Question**: What is the start date and end date of the dataset?  
**Answer**: Start date **2009-06-01**, end date **2009-07-01**.

**Query used:**

```sql
SELECT
  MIN(trip_pickup_date_time::DATE) AS start_date,
  MAX(trip_dropoff_date_time::DATE) AS end_date
FROM "yellow_taxi_trips";
```

## Question 2

**Question**: What proportion of trips are paid with credit card?  
**Given counts**:  
- Total trips in sample: **10,000**  
- Trips paid with credit card: **2,666**

**Calculation:**

```text
proportion = (2666 / 10000) * 100 = 26.66%
```

So, **about 26.66%** of trips are paid with credit card.

**Example query to compute this directly in SQL:**

```sql
SELECT
  COUNT(*) AS total_trips,
  COUNT(*) FILTER (WHERE payment_type = 'Credit') AS credit_card_trips,
  100.0 * COUNT(*) FILTER (WHERE payment_type = 'Credit') / COUNT(*) AS credit_card_percentage
FROM "yellow_taxi_trips";
```

## Question 3

**Question**: What is the total amount of money generated in tips?  
**Answer**: **$6,063.41**

**Query used:**

```sql
SELECT
  SUM(tip_amt) AS total_tip_amount
FROM "yellow_taxi_trips";
```

