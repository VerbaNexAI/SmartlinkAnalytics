                DECLARE @nombreVista NVARCHAR(128) = 'Vistas';
                DECLARE @sql NVARCHAR(MAX);

                IF EXISTS (SELECT 1 FROM sys.views WHERE name = @nombreVista)
                BEGIN
                    SET @sql = 'SELECT * FROM [' + @nombreVista + ']';
                    EXEC sp_executesql @sql;
                END
                ELSE
                BEGIN
                    EXEC sp_executesql N'
                    CREATE VIEW dbo.Vistas AS
                    SELECT dbo.Clientes.Nombre, dbo.Clientes.ClienteID, dbo.Pedidos.PedidoID, dbo.Pedidos.Fecha, dbo.Pedidos.Monto
                    FROM dbo.Clientes
                    INNER JOIN dbo.Pedidos ON dbo.Clientes.ClienteID = dbo.Pedidos.ClienteID';
                    
                    SET @sql = 'SELECT * FROM [' + @nombreVista + ']';
                    EXEC sp_executesql @sql;
                END