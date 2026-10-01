-- ============================================================
-- FINRA Industry Regulatory Analytics
-- Query 1: Overall Dataset Summary
-- ============================================================

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT year) AS years_covered,
    MIN(year) AS first_year,
    MAX(year) AS last_year,
    COUNT(DISTINCT report_date) AS snapshot_dates,
    COUNT(DISTINCT registration_type) AS registration_categories,
    SUM(number_of_firms) AS total_firm_observations
FROM finra_industry_snapshot;


-- ============================================================
-- Query 2: Historical Trend in FINRA-Registered Firms
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        number_of_firms,
        report_date
    FROM public.finra_industry_snapshot
    WHERE registration_type =
        'All FINRA-Registered Broker-Dealer Firms at Year End'
      AND (
            report_date = '2022-12-31'
            OR (
                report_date = '2021-12-31'
                AND year IN (2011, 2021)
            )
          )
)

SELECT
    year,
    number_of_firms,
    report_date
FROM selected_snapshot
ORDER BY year;


-- ============================================================
-- Query 3: Year-over-Year Change
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE registration_type =
        'All FINRA-Registered Broker-Dealer Firms at Year End'
      AND (
            report_date = '2022-12-31'
            OR (
                report_date = '2021-12-31'
                AND year IN (2011, 2021)
            )
          )
),

trend AS (
    SELECT
        year,
        number_of_firms,
        LAG(number_of_firms) OVER (
            ORDER BY year
        ) AS previous_year_firms
    FROM selected_snapshot
)

SELECT
    year,
    number_of_firms,
    previous_year_firms,
    number_of_firms - previous_year_firms AS yoy_change,
    ROUND(
        (
            (number_of_firms - previous_year_firms)
            * 100.0
            / NULLIF(previous_year_firms, 0)
        )::numeric,
        2
    ) AS yoy_change_pct
FROM trend
ORDER BY year;


-- ============================================================
-- Query 4: Overall Change and Largest Annual Decline
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE registration_type =
        'All FINRA-Registered Broker-Dealer Firms at Year End'
      AND (
            report_date = '2022-12-31'
            OR (
                report_date = '2021-12-31'
                AND year IN (2011, 2021)
            )
          )
),

trend AS (
    SELECT
        year,
        number_of_firms,
        LAG(number_of_firms) OVER (
            ORDER BY year
        ) AS previous_year_firms
    FROM selected_snapshot
),

yoy AS (
    SELECT
        year,
        number_of_firms,
        previous_year_firms,
        number_of_firms - previous_year_firms AS yoy_change,
        ROUND(
            (
                (number_of_firms - previous_year_firms)
                * 100.0
                / NULLIF(previous_year_firms, 0)
            )::numeric,
            2
        ) AS yoy_change_pct
    FROM trend
)

SELECT
    MIN(year) AS first_year,
    MAX(year) AS last_year,

    MAX(
        number_of_firms
    ) FILTER (
        WHERE year = (SELECT MIN(year) FROM yoy)
    ) AS firms_first_year,

    MAX(
        number_of_firms
    ) FILTER (
        WHERE year = (SELECT MAX(year) FROM yoy)
    ) AS firms_last_year,

    MAX(
        number_of_firms
    ) FILTER (
        WHERE year = (SELECT MIN(year) FROM yoy)
    )
    -
    MAX(
        number_of_firms
    ) FILTER (
        WHERE year = (SELECT MAX(year) FROM yoy)
    ) AS total_decline,

    ROUND(
        (
            (
                MAX(number_of_firms) FILTER (
                    WHERE year = (SELECT MAX(year) FROM yoy)
                )
                -
                MAX(number_of_firms) FILTER (
                    WHERE year = (SELECT MIN(year) FROM yoy)
                )
            )
            * 100.0
            /
            MAX(number_of_firms) FILTER (
                WHERE year = (SELECT MIN(year) FROM yoy)
            )
        )::numeric,
        2
    ) AS total_change_pct,

    MIN(yoy_change) AS largest_yoy_decline,

    MIN(yoy_change_pct) AS largest_yoy_decline_pct

FROM yoy;

-- ============================================================
-- Query 5: Registration Category Comparison
-- 2011 vs 2021
-- ============================================================

WITH category_data AS (
    SELECT
        registration_type,
        year,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

category_comparison AS (
    SELECT
        registration_type,

        MAX(number_of_firms)
            FILTER (WHERE year = 2011)
            AS firms_2011,

        MAX(number_of_firms)
            FILTER (WHERE year = 2021)
            AS firms_2021

    FROM category_data
    GROUP BY registration_type
)

SELECT
    registration_type,
    firms_2011,
    firms_2021,

    firms_2021 - firms_2011 AS absolute_change,

    ROUND(
        (
            (firms_2021 - firms_2011)
            * 100.0
            / NULLIF(firms_2011, 0)
        )::numeric,
        2
    ) AS percentage_change

FROM category_comparison
ORDER BY registration_type;

-- ============================================================
-- Query 6: Registration Category Trend Over Time
-- 2011-2021
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
)

SELECT
    year,
    registration_type,
    number_of_firms
FROM selected_snapshot
ORDER BY
    year,
    registration_type;
	
	
	-- ============================================================
-- Query 7: Year-over-Year Change by Registration Category
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

category_trend AS (
    SELECT
        year,
        registration_type,
        number_of_firms,

        LAG(number_of_firms) OVER (
            PARTITION BY registration_type
            ORDER BY year
        ) AS previous_year_firms

    FROM selected_snapshot
)

SELECT
    year,
    registration_type,
    number_of_firms,
    previous_year_firms,

    number_of_firms - previous_year_firms
        AS absolute_change,

    ROUND(
        (
            (number_of_firms - previous_year_firms)
            * 100.0
            / NULLIF(previous_year_firms, 0)
        )::numeric,
        2
    ) AS percentage_change

FROM category_trend
ORDER BY
    year,
    registration_type;
	
	
	-- ============================================================
-- Query 8: Largest Annual Changes by Registration Category
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

category_trend AS (
    SELECT
        year,
        registration_type,
        number_of_firms,

        LAG(number_of_firms) OVER (
            PARTITION BY registration_type
            ORDER BY year
        ) AS previous_year_firms

    FROM selected_snapshot
),

yoy_changes AS (
    SELECT
        year,
        registration_type,
        number_of_firms,
        previous_year_firms,

        number_of_firms - previous_year_firms
            AS absolute_change,

        ROUND(
            (
                (number_of_firms - previous_year_firms)
                * 100.0
                / NULLIF(previous_year_firms, 0)
            )::numeric,
            2
        ) AS percentage_change

    FROM category_trend
    WHERE previous_year_firms IS NOT NULL
)

SELECT
    year,
    registration_type,
    number_of_firms,
    previous_year_firms,
    absolute_change,
    percentage_change
FROM yoy_changes
ORDER BY ABS(absolute_change) DESC
LIMIT 10;


-- ============================================================
-- Query 9: Broker-Dealer vs Investment Adviser Trend
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
)

SELECT
    year,

    MAX(
        number_of_firms
    ) FILTER (
        WHERE registration_type =
            'All FINRA-Registered Broker-Dealer Firms at Year End'
    ) AS broker_dealer_firms,

    MAX(
        number_of_firms
    ) FILTER (
        WHERE registration_type =
            'Investment Adviser Firms-Only at Year End'
    ) AS investment_adviser_only_firms

FROM selected_snapshot

GROUP BY year
ORDER BY year;


-- ============================================================
-- Query 10: Gap Between Broker-Dealer and Investment Adviser
-- Categories
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

category_pivot AS (
    SELECT
        year,

        MAX(number_of_firms) FILTER (
            WHERE registration_type =
                'All FINRA-Registered Broker-Dealer Firms at Year End'
        ) AS broker_dealer_firms,

        MAX(number_of_firms) FILTER (
            WHERE registration_type =
                'Investment Adviser Firms-Only at Year End'
        ) AS investment_adviser_only_firms

    FROM selected_snapshot
    GROUP BY year
)

SELECT
    year,
    broker_dealer_firms,
    investment_adviser_only_firms,

    investment_adviser_only_firms - broker_dealer_firms
        AS firm_count_gap

FROM category_pivot
ORDER BY year;

-- ============================================================
-- Query 11: CAGR — 2011 to 2021
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

category_endpoints AS (
    SELECT
        registration_type,

        MAX(number_of_firms)
            FILTER (WHERE year = 2011)
            AS firms_2011,

        MAX(number_of_firms)
            FILTER (WHERE year = 2021)
            AS firms_2021

    FROM selected_snapshot
    GROUP BY registration_type
)

SELECT
    registration_type,
    firms_2011,
    firms_2021,

    ROUND(
        (
            (
                POWER(
                    firms_2021::numeric / NULLIF(firms_2011, 0),
                    1.0 / 10
                ) - 1
            ) * 100
        ),
        2
    ) AS cagr_percentage

FROM category_endpoints
WHERE registration_type IN (
    'All FINRA-Registered Broker-Dealer Firms at Year End',
    'Investment Adviser Firms-Only at Year End'
)
ORDER BY registration_type;

-- ============================================================
-- Query 12: Registration Category Share by Year
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

year_totals AS (
    SELECT
        year,
        SUM(number_of_firms) AS total_reported_firms
    FROM selected_snapshot
    GROUP BY year
)

SELECT
    s.year,
    s.registration_type,
    s.number_of_firms,
    t.total_reported_firms,

    ROUND(
        (
            s.number_of_firms * 100.0
            / NULLIF(t.total_reported_firms, 0)
        )::numeric,
        2
    ) AS category_share_pct

FROM selected_snapshot s
JOIN year_totals t
    ON s.year = t.year

ORDER BY
    s.year,
    s.registration_type;
	
	-- ============================================================
-- Query 13: Registration Category Share Change
-- 2011 vs 2021
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

year_totals AS (
    SELECT
        year,
        SUM(number_of_firms) AS total_reported_firms
    FROM selected_snapshot
    GROUP BY year
),

category_shares AS (
    SELECT
        s.year,
        s.registration_type,
        ROUND(
            (
                s.number_of_firms * 100.0
                / NULLIF(t.total_reported_firms, 0)
            )::numeric,
            2
        ) AS category_share_pct
    FROM selected_snapshot s
    JOIN year_totals t
        ON s.year = t.year
),

share_comparison AS (
    SELECT
        registration_type,

        MAX(category_share_pct)
            FILTER (WHERE year = 2011)
            AS share_2011,

        MAX(category_share_pct)
            FILTER (WHERE year = 2021)
            AS share_2021

    FROM category_shares
    GROUP BY registration_type
)

SELECT
    registration_type,
    share_2011,
    share_2021,

    ROUND(
        (share_2021 - share_2011)::numeric,
        2
    ) AS share_change_percentage_points

FROM share_comparison

ORDER BY registration_type;

-- ============================================================
-- Query 14: Trend Consistency by Registration Category
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

yearly_change AS (
    SELECT
        year,
        registration_type,
        number_of_firms,

        number_of_firms
        - LAG(number_of_firms)
          OVER (
              PARTITION BY registration_type
              ORDER BY year
          ) AS absolute_change

    FROM selected_snapshot
)

SELECT
    registration_type,

    COUNT(*) FILTER (
        WHERE absolute_change > 0
    ) AS years_increased,

    COUNT(*) FILTER (
        WHERE absolute_change < 0
    ) AS years_decreased,

    COUNT(*) FILTER (
        WHERE absolute_change = 0
    ) AS years_unchanged,

    ROUND(
        AVG(absolute_change)
        FILTER (WHERE absolute_change IS NOT NULL)::numeric,
        2
    ) AS avg_annual_change

FROM yearly_change

GROUP BY registration_type

ORDER BY registration_type;

-- ============================================================
-- Query 15: Highest and Lowest Year by Registration Category
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

ranked_data AS (
    SELECT
        year,
        registration_type,
        number_of_firms,

        ROW_NUMBER() OVER (
            PARTITION BY registration_type
            ORDER BY number_of_firms DESC, year DESC
        ) AS highest_rank,

        ROW_NUMBER() OVER (
            PARTITION BY registration_type
            ORDER BY number_of_firms ASC, year ASC
        ) AS lowest_rank

    FROM selected_snapshot
)

SELECT
    registration_type,

    MAX(year) FILTER (
        WHERE highest_rank = 1
    ) AS highest_year,

    MAX(number_of_firms) FILTER (
        WHERE highest_rank = 1
    ) AS highest_firms,

    MAX(year) FILTER (
        WHERE lowest_rank = 1
    ) AS lowest_year,

    MAX(number_of_firms) FILTER (
        WHERE lowest_rank = 1
    ) AS lowest_firms

FROM ranked_data

GROUP BY registration_type

ORDER BY registration_type;

-- ============================================================
-- Query 16: Largest Annual Percentage Change by Category
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

yearly_change AS (
    SELECT
        year,
        registration_type,
        number_of_firms,

        LAG(number_of_firms) OVER (
            PARTITION BY registration_type
            ORDER BY year
        ) AS previous_year_firms

    FROM selected_snapshot
),

percentage_change AS (
    SELECT
        year,
        registration_type,
        number_of_firms,
        previous_year_firms,

        ROUND(
            (
                (number_of_firms - previous_year_firms)
                * 100.0
                / NULLIF(previous_year_firms, 0)
            )::numeric,
            2
        ) AS yoy_percentage_change

    FROM yearly_change
    WHERE previous_year_firms IS NOT NULL
),

ranked_changes AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY registration_type
            ORDER BY ABS(yoy_percentage_change) DESC, year DESC
        ) AS change_rank

    FROM percentage_change
)

SELECT
    registration_type,
    year,
    previous_year_firms,
    number_of_firms,
    yoy_percentage_change

FROM ranked_changes

WHERE change_rank = 1

ORDER BY registration_type;

-- ============================================================
-- Query 17: Volatility of Annual Percentage Changes
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

yearly_change AS (
    SELECT
        year,
        registration_type,
        number_of_firms,

        LAG(number_of_firms) OVER (
            PARTITION BY registration_type
            ORDER BY year
        ) AS previous_year_firms

    FROM selected_snapshot
),

percentage_change AS (
    SELECT
        year,
        registration_type,

        (
            (number_of_firms - previous_year_firms)
            * 100.0
            / NULLIF(previous_year_firms, 0)
        ) AS yoy_percentage_change

    FROM yearly_change
    WHERE previous_year_firms IS NOT NULL
)

SELECT
    registration_type,

    ROUND(
        AVG(yoy_percentage_change)::numeric,
        2
    ) AS avg_yoy_pct,

    ROUND(
        MIN(yoy_percentage_change)::numeric,
        2
    ) AS min_yoy_pct,

    ROUND(
        MAX(yoy_percentage_change)::numeric,
        2
    ) AS max_yoy_pct,

    ROUND(
        STDDEV_SAMP(yoy_percentage_change)::numeric,
        2
    ) AS yoy_stddev

FROM percentage_change

GROUP BY registration_type

ORDER BY registration_type;

-- ============================================================
-- Query 18: Correlation Between Registration Category Trends
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

category_pivot AS (
    SELECT
        year,

        MAX(number_of_firms) FILTER (
            WHERE registration_type =
                'All FINRA-Registered Broker-Dealer Firms at Year End'
        ) AS broker_dealer_firms,

        MAX(number_of_firms) FILTER (
            WHERE registration_type =
                'Investment Adviser Firms-Only at Year End'
        ) AS investment_adviser_firms,

        MAX(number_of_firms) FILTER (
            WHERE registration_type =
                'Securities Industry Registered Firms at Year End'
        ) AS securities_industry_firms

    FROM selected_snapshot

    GROUP BY year
)

SELECT
    ROUND(
        CORR(
            broker_dealer_firms,
            investment_adviser_firms
        )::numeric,
        4
    ) AS corr_broker_dealer_vs_investment_adviser,

    ROUND(
        CORR(
            broker_dealer_firms,
            securities_industry_firms
        )::numeric,
        4
    ) AS corr_broker_dealer_vs_securities_industry,

    ROUND(
        CORR(
            investment_adviser_firms,
            securities_industry_firms
        )::numeric,
        4
    ) AS corr_investment_adviser_vs_securities_industry

FROM category_pivot;

-- ============================================================
-- Query 19: 5-Year vs 10-Year Change
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

category_endpoints AS (
    SELECT
        registration_type,

        MAX(number_of_firms) FILTER (
            WHERE year = 2011
        ) AS firms_2011,

        MAX(number_of_firms) FILTER (
            WHERE year = 2016
        ) AS firms_2016,

        MAX(number_of_firms) FILTER (
            WHERE year = 2021
        ) AS firms_2021

    FROM selected_snapshot

    GROUP BY registration_type
)

SELECT
    registration_type,

    firms_2011,
    firms_2016,
    firms_2021,

    firms_2016 - firms_2011 AS change_2011_2016,

    ROUND(
        (
            (firms_2016 - firms_2011)
            * 100.0
            / NULLIF(firms_2011, 0)
        )::numeric,
        2
    ) AS change_pct_2011_2016,

    firms_2021 - firms_2016 AS change_2016_2021,

    ROUND(
        (
            (firms_2021 - firms_2016)
            * 100.0
            / NULLIF(firms_2016, 0)
        )::numeric,
        2
    ) AS change_pct_2016_2021,

    firms_2021 - firms_2011 AS change_2011_2021,

    ROUND(
        (
            (firms_2021 - firms_2011)
            * 100.0
            / NULLIF(firms_2011, 0)
        )::numeric,
        2
    ) AS change_pct_2011_2021

FROM category_endpoints

ORDER BY registration_type;

-- ============================================================
-- Query 20: Largest Overall Year-over-Year Movement
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

yearly_total AS (
    SELECT
        year,
        SUM(number_of_firms) AS total_reported_observations
    FROM selected_snapshot
    GROUP BY year
),

yearly_change AS (
    SELECT
        year,
        total_reported_observations,
        LAG(total_reported_observations) OVER (
            ORDER BY year
        ) AS previous_year_total
    FROM yearly_total
)

SELECT
    year,
    previous_year_total,
    total_reported_observations,

    total_reported_observations - previous_year_total
        AS absolute_change,

    ROUND(
        (
            (total_reported_observations - previous_year_total)
            * 100.0
            / NULLIF(previous_year_total, 0)
        )::numeric,
        2
    ) AS percentage_change

FROM yearly_change

WHERE previous_year_total IS NOT NULL

ORDER BY ABS(
    total_reported_observations - previous_year_total
) DESC;

-- ============================================================
-- Query 21: Category Contribution to 2011-2021 Change
-- ============================================================

WITH selected_snapshot AS (
    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2022-12-31'
      AND year BETWEEN 2012 AND 2020

    UNION ALL

    SELECT
        year,
        registration_type,
        number_of_firms
    FROM public.finra_industry_snapshot
    WHERE report_date = '2021-12-31'
      AND year IN (2011, 2021)
),

category_endpoints AS (
    SELECT
        registration_type,

        MAX(number_of_firms) FILTER (
            WHERE year = 2011
        ) AS firms_2011,

        MAX(number_of_firms) FILTER (
            WHERE year = 2021
        ) AS firms_2021

    FROM selected_snapshot

    GROUP BY registration_type
),

category_change AS (
    SELECT
        registration_type,
        firms_2011,
        firms_2021,
        firms_2021 - firms_2011 AS absolute_change
    FROM category_endpoints
),

overall_change AS (
    SELECT
        SUM(absolute_change) AS total_absolute_change
    FROM category_change
)

SELECT
    c.registration_type,
    c.firms_2011,
    c.firms_2021,
    c.absolute_change,

    ROUND(
        (
            c.absolute_change * 100.0
            / NULLIF(c.firms_2011, 0)
        )::numeric,
        2
    ) AS category_change_pct,

    ROUND(
        (
            c.absolute_change * 100.0
            / NULLIF(o.total_absolute_change, 0)
        )::numeric,
        2
    ) AS contribution_to_overall_change_pct

FROM category_change c
CROSS JOIN overall_change o

ORDER BY c.absolute_change DESC;