USE DATABASE FITCONNECT_ANALYTICS;
USE SCHEMA ANALYTICS;

CREATE OR REPLACE TABLE AI_WEEKLY_INSIGHTS (
    INSIGHT_ID STRING,
    GENERATED_AT TIMESTAMP_NTZ,
    PERIOD_START DATE,
    PERIOD_END DATE,
    MODEL_NAME STRING,
    INSIGHT_JSON VARIANT
);

INSERT INTO AI_WEEKLY_INSIGHTS (
    INSIGHT_ID,
    GENERATED_AT,
    PERIOD_START,
    PERIOD_END,
    MODEL_NAME,
    INSIGHT_JSON
)
WITH RESPONSE AS (
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'claude-4-sonnet',
        CONCAT(
            'Return ONLY valid JSON. ',
            'Do not include markdown, explanations, or code fences. ',
            'The response must start with { and end with }. ',
            'Use exactly these keys: summary, anomalies, recommendations, next_actions. ',
            'summary must be a string. ',
            'anomalies, recommendations, and next_actions must be arrays of strings. ',
            'Analyze these FitConnect SaaS metrics: ',
            OBJECT_CONSTRUCT(*)::STRING
        )
    ) AS RAW_RESPONSE
    FROM MART_KPI_OVERVIEW
)
SELECT
    UUID_STRING() AS INSIGHT_ID,
    CURRENT_TIMESTAMP() AS GENERATED_AT,
    DATEADD(day, -7, CURRENT_DATE) AS PERIOD_START,
    CURRENT_DATE AS PERIOD_END,
    'claude-4-sonnet' AS MODEL_NAME,
    TRY_PARSE_JSON(REGEXP_SUBSTR(RAW_RESPONSE, '\\{.*\\}', 1, 1, 's')) AS INSIGHT_JSON
FROM RESPONSE;
