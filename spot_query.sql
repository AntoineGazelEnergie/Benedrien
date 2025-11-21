SET LANGUAGE French;

SELECT 
    DATEADD(hour, CAST(REPLACE(heure, 'p', '') AS int) - 1, CAST(Maturity AS datetime)) AS Datetime,
    prix AS Spot
FROM (
    SELECT [Price Set], [Market], [Component], [Price Date], [Time], [Maturity],
           [p01],[p02],[p03],[p04],[p05],[p06],[p07],[p08],[p09],[p10],[p11],[p12],
           [p13],[p14],[p15],[p16],[p17],[p18],[p19],[p20],[p21],[p22],[p23],[p24],
           [Currency],[Unit]
    FROM [dbo].[V_NEW_PRICESHLY]
    WHERE market = 'EPEX'
      AND [price set] = 'spot_mid'
      AND Component = 'PWFHO'
      AND Maturity BETWEEN :start_date AND :end_date
) AS qq
UNPIVOT (
    prix FOR heure IN ([p01],[p02],[p03],[p04],[p05],[p06],[p07],[p08],[p09],[p10],[p11],[p12],
                       [p13],[p14],[p15],[p16],[p17],[p18],[p19],[p20],[p21],[p22],[p23],[p24])
) AS unpvt;
