SELECT 
    YEAR(Maturity) AS Année,
    MONTH(Maturity) AS Mois,
    AVG(prix_hfc) AS Hfc,
    COUNT(prix_hfc) AS nb_heures
FROM (
    SELECT 
        Maturity,
        CAST(REPLACE(_heure,'p','') AS INT) - 1 AS heure,
        prix_hfc
    FROM (
        SELECT *
        FROM [dbo].[V_NEW_PRICESHLY]
        WHERE [Price Set] = 'FWD_ASK'
          AND Market = 'EPC'
          AND [Price Date] = :price_date
    ) AS pivo
    UNPIVOT (
        prix_hfc FOR _heure IN (
            [p01],[p02],[p03],[p04],[p05],[p06],
            [p07],[p08],[p09],[p10],[p11],[p12],
            [p13],[p14],[p15],[p16],[p17],[p18],
            [p19],[p20],[p21],[p22],[p23],[p24],[p25]
        )
    ) AS pi
) AS _hfc
GROUP BY YEAR(Maturity), MONTH(Maturity)
ORDER BY Année, Mois, Hfc;