# File to store prompts for few shot
few_shot_prompts_list = [
    {'Question': 'Which 5 regions have the most volatile avocado prices year-over-year?',
 'SQLQuery': """
    SELECT region,
           year,
           ROUND(AVG(AveragePrice), 2) AS avg_price,
           ROUND(STDDEV(AveragePrice), 2) AS price_stddev
    FROM avocadodata
    GROUP BY region, year
    ORDER BY price_stddev DESC
    LIMIT 5;
 """,
 'SQLResult': """[('Spokane', 2017, Decimal('1.60'), 0.61), ('Portland', 2017, Decimal('1.43'), 0.61), ('Seattle', 2017, Decimal('1.60'), 0.61), ('PhoenixTucson', 2016, Decimal('1.26'), 0.6), ('SanFrancisco', 2016, Decimal('1.88'), 0.57)]""",
 'Answer': """['Spokane', 'Portland', 'Seattle', 'PhoenixTucson', 'SanFrancisco']"""},


    {'Question': 'Which regions show increasing demand and decreasing average price year over year (possible oversupply)?',
 'SQLQuery': """
    WITH yearly_trends AS (
      SELECT region, year,
             SUM(Total_Volume) AS yearly_volume,
             AVG(AveragePrice) AS yearly_avg_price
      FROM avocadodata
      GROUP BY region, year
    ),
    price_volume_change AS (
      SELECT t1.region,
             t1.year AS year_start,
             t2.year AS year_end,
             t2.yearly_volume - t1.yearly_volume AS volume_change,
             t2.yearly_avg_price - t1.yearly_avg_price AS price_change
      FROM yearly_trends t1
      JOIN yearly_trends t2 ON t1.region = t2.region AND t1.year = t2.year - 1
    )
    SELECT *
    FROM price_volume_change
    WHERE volume_change > 0 AND price_change < 0
    ORDER BY ABS(volume_change * price_change) DESC
    LIMIT 5;
 """,
 'SQLResult': """[('Southeast', 2015, 2016, Decimal('38026268.59'), Decimal('-0.127789')), ('West', 2015, 2016, Decimal('39907015.38'), Decimal('-0.056923')), ('SouthCentral', 2015, 2016, Decimal('13644105.60'), Decimal('-0.085096')), ('Portland', 2015, 2016, Decimal('9368056.53'), Decimal('-0.115192')), ('LosAngeles', 2015, 2016, Decimal('14921609.84'), Decimal('-0.068750'))]""",
 'Answer': """['Southeast', 'West', 'SouthCentral', 'Portland', 'LosAngeles']"""},

    
    {'Question': 'What are the 5 most extreme avocado price outliers compared to the regional average?',
 'SQLQuery': """
    WITH region_stats AS (
      SELECT region,
             AVG(AveragePrice) AS mean_price,
             STDDEV(AveragePrice) AS stddev_price
      FROM avocadodata
      GROUP BY region
    )
    SELECT a.region, a.Date, a.AveragePrice,
           r.mean_price, r.stddev_price
    FROM avocadodata a
    JOIN region_stats r ON a.region = r.region
    WHERE ABS(a.AveragePrice - r.mean_price) > 2 * r.stddev_price
    ORDER BY ABS(a.AveragePrice - r.mean_price) DESC
    LIMIT 5;
 """,
 'SQLResult': """[('Tampa', datetime.date(2017, 4, 16), Decimal('3.17'), Decimal('1.408846'), 0.3405853384705), ('WestTexNewMexico', datetime.date(2016, 10, 16), Decimal('2.93'), Decimal('1.261701'), 0.4963644849685269), ('LasVegas', datetime.date(2016, 10, 2), Decimal('3.03'), Decimal('1.380917'), 0.47326642758671433), ('MiamiFtLauderdale', datetime.date(2017, 3, 12), Decimal('3.05'), Decimal('1.428491'), 0.33599596042836527), ('WestTexNewMexico', datetime.date(2016, 9, 25), Decimal('2.83'), Decimal('1.261701'), 0.4963644849685269)]""",
 'Answer': """['Tampa 2017-04-16', 'WestTexNewMexico 2016-10-16', 'LasVegas 2016-10-02', 'MiamiFtLauderdale 2017-03-12', 'WestTexNewMexico 2016-09-25']"""},




{'Question': 'Which 5 calendar months have the highest average avocado prices across all years?',
 'SQLQuery': """
    SELECT EXTRACT(MONTH FROM Date) AS month,
           ROUND(AVG(AveragePrice), 2) AS avg_price
    FROM avocadodata
    GROUP BY EXTRACT(MONTH FROM Date)
    ORDER BY avg_price DESC
    LIMIT 5;
 """,
 'SQLResult': """[(10, Decimal('1.58')), (9, Decimal('1.57')), (8, Decimal('1.51')), (11, Decimal('1.46')), (7, Decimal('1.46'))]""",
 'Answer': """['10', '9', '8', '11', '7']"""}


]