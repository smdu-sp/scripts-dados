SELECT [sistema]
      ,[processo]
      ,[protocolo]
      ,[dtInclusaoAssunto]
      ,[assunto]
      ,[situacaoAssunto]
      ,[statusDocumento]

FROM (
    SELECT [sistema]
          ,[processo]
          ,[protocolo]
          ,[dtInclusaoAssunto]
          ,[assunto]
          ,[situacaoAssunto]
          ,[statusDocumento]
          ,ROW_NUMBER() OVER (PARTITION BY [processo] ORDER BY [dtInclusaoAssunto] DESC) AS rn
    FROM [sa_licenciamento].[dbo].[prata_assunto]
    WHERE sistema = 'aprovaDigital'
) AS subquery

WHERE rn = 1