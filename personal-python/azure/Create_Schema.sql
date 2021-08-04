IF OBJECT_ID('[dbo].[PlayerRank]', 'U') IS NOT NULL
DROP TABLE [dbo].[PlayerRank]
GO

CREATE TABLE dbo.PlayerRank (
    PlayerRankId    INT PRIMARY KEY IDENTITY(1,1),
    ETL_DTM         DATETIME2       NULL,
    Platform        varchar(10)     NULL,
    Player_Name     varchar(100)    NULL,
    Playlist        varchar(50)     NULL,
    Rank            varchar(50)     NULL,
    Division        varchar(50)     NULL,
    MMR             INT             NULL
);
GO
--SELECT * FROM player_rank