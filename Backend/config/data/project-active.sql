
            SELECT [PROYECTO], [ID], [FECHA-CREACION], [ESTADO]
            FROM [ODS].[dbo].['NOMBRES-PROYECTOS-2D$']
            WHERE [ESTADO] = 'activo' 
            AND [PROYECTO] LIKE 'SPID%SDB';