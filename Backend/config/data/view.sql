DECLARE @nombreVista NVARCHAR(128) = 'New_View-Inconsistency';
DECLARE @sql NVARCHAR(MAX);

IF EXISTS (SELECT 1 FROM sys.views WHERE name = @nombreVista)
BEGIN
    SET @sql = 'SELECT * FROM [' + @nombreVista + ']';
    EXEC sp_executesql @sql;
END
ELSE
BEGIN
    SET @sql = '
    CREATE VIEW dbo.View_Inconsistency_items AS
SELECT SPID_PRUEBA_SDBpid.T_Relationship.SP_Item2ID, SPID_PRUEBA_SDBpid.T_Relationship.GraphicOID, SPID_PRUEBA_SDBpid.T_Relationship.Item1Location, SPID_PRUEBA_SDBpid.T_Relationship.Item2Location, SPID_PRUEBA_SDBpid.T_Relationship.IsBinary, SPID_PRUEBA_SDBpid.T_Relationship.SP_Item1ID, SPID_PRUEBA_SDBpid.T_Inconsistency.SP_ID AS SP_InconsistencyID, SPID_PRUEBA_SDBpid.T_Inconsistency.Description, 
         SPID_PRUEBA_SDBpid.T_Inconsistency.Name, SPID_PRUEBA_SDBpid.T_Inconsistency.InconsistencyType, SPID_PRUEBA_SDBpid.T_Inconsistency.IsApproved, SPID_PRUEBA_SDBpid.T_Inconsistency.InconsistencyStatus, SPID_PRUEBA_SDBpid.T_Inconsistency.Severity, SPID_PRUEBA_SDBpid.T_Inconsistency.PropNameItem1, SPID_PRUEBA_SDBpid.T_Inconsistency.PropNameItem2, SPID_PRUEBA_SDBpid.T_Inconsistency.SP_RelationshipID, 
         SPID_PRUEBA_SDBpid.T_Representation.SP_ID AS SP_RepresentationID, SPID_PRUEBA_SDBpid.T_Representation.RepresentationType, SPID_PRUEBA_SDBpid.T_Representation.GraphicOID AS GraphicOID_Representation, SPID_PRUEBA_SDBpid.T_Representation.InStockpile, SPID_PRUEBA_SDBpid.T_Representation.FileName, SPID_PRUEBA_SDBpid.T_Representation.Style, SPID_PRUEBA_SDBpid.T_Representation.SP_ModelItemID, 
         SPID_PRUEBA_SDBpid.T_Representation.RADLayer, SPID_PRUEBA_SDBpid.T_Representation.ExportLayer, SPID_PRUEBA_SDBpid.T_Representation.ItemStatus, SPID_PRUEBA_SDBpid.T_Representation.RepresentationClass, SPID_PRUEBA_SDBpid.T_Representation.SP_FileLastModifiedTime, SPID_PRUEBA_SDBpid.T_Representation.SP_ModelItemTimestamp, SPID_PRUEBA_SDBpid.T_Representation.SP_DrawingID, 
         SPID_PRUEBA_SDBpid.T_Relationship.UpdateCount, SPID_PRUEBA_SDBpid.T_Drawing.Path, SPID_PRUEBA_SDBpid.T_Drawing.Name AS Drawing_Name
FROM  SPID_PRUEBA_SDBpid.T_Relationship INNER JOIN
         SPID_PRUEBA_SDBpid.T_Representation ON SPID_PRUEBA_SDBpid.T_Relationship.SP_Item2ID = SPID_PRUEBA_SDBpid.T_Representation.SP_ID INNER JOIN
         SPID_PRUEBA_SDBpid.T_Inconsistency ON SPID_PRUEBA_SDBpid.T_Relationship.SP_ID = SPID_PRUEBA_SDBpid.T_Inconsistency.SP_RelationshipID INNER JOIN
         SPID_PRUEBA_SDBpid.T_Drawing ON SPID_PRUEBA_SDBpid.T_Relationship.SP_DrawingID = SPID_PRUEBA_SDBpid.T_Drawing.SP_ID';

    EXEC sp_executesql @sql;
    
    SET @sql = 'SELECT * FROM [' + @nombreVista + ']';
    EXEC sp_executesql @sql;
END;
