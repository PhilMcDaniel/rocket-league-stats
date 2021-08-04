IF OBJECT_ID('[dbo].[PlayerRank]', 'U') IS NOT NULL
DROP TABLE [dbo].[PlayerRank]
GO

CREATE TABLE dbo.PlayerRank (
    PlayerRankId    INT PRIMARY KEY IDENTITY(1,1),
    ETL_DTM         DATETIME2       NULL,
    Platform        varchar(10)     NULL,
    Player_Name     varchar(100)    NULL,
    Playlist        varchar(50)     NULL,
    Rank            varchar(100)    NULL,
    Division        varchar(50)     NULL,
    MMR             INT             NULL,
    IsLatest        char(1)         NULL
);
GO
--SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.PlayerRank')

INSERT INTO [dbo].[PlayerRank] ([ETL_DTM],[Platform],[Player_Name],[Playlist],[Rank],[Division],[MMR],[IsLatest])
VALUES (GETDATE(),'test','test','test','test','test',-1,'Y')
--SELECT * FROM dbo.PlayerRank