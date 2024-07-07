
            -- SELECT [PROYECTO], [ID], [FECHA-CREACION], [ESTADO]
            -- FROM [ODS].[dbo].['NOMBRES-PROYECTOS-2D$']
            -- WHERE [ESTADO] = 'activo' 
            -- AND [PROYECTO] LIKE 'SPID%SDB';


SELECT name 
FROM sys.databases
WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb');
