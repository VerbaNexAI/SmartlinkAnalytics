                SELECT [PROYECTO], [ID], [FECHA-CREACION], [ESTADO]
                FROM [ODS].[dbo].['NOMBRES-PROYECTOS-2D$']
                WHERE [PROYECTO] NOT LIKE '%master%'
                AND [PROYECTO] NOT LIKE '%tempdb%'
                AND [PROYECTO] NOT LIKE '%model%'
                AND [PROYECTO] NOT LIKE '%msdb%'
                AND [PROYECTO] NOT LIKE '%CAS05%'
                AND [PROYECTO] LIKE 'SPID%SDB'
                AND [ESTADO] = 'inactivo';