CREATE TABLE [dbo].[Batch] (
    [Batch_Id]     UNIQUEIDENTIFIER NOT NULL,
    [BatchDate]    DATE             NULL,
    [ETL_DTM]      DATETIME2 (7) NULL,
    [BatchDurationSeconds] DECIMAL (13,4)  NULL,
    PRIMARY KEY CLUSTERED (Batch_Id ASC)
)
WITH (DATA_COMPRESSION = ROW);


GO