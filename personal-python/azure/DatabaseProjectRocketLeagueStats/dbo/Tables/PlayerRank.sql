CREATE TABLE [dbo].[PlayerRank] (
    [PlayerRankId] INT           IDENTITY (1, 1) NOT NULL,
    [ETL_DTM]      DATETIME2 (7) NULL,
    [Platform]     VARCHAR (10)  NULL,
    [PlatformPlayer_Id] VARCHAR(100) NULL,
    [Player_Name]  VARCHAR (100) NULL,
    [Playlist]     VARCHAR (50)  NULL,
    [Rank]         VARCHAR (100) NULL,
    [Division]     VARCHAR (50)  NULL,
    [MMR]          INT           NULL,
    [IsLatest]     CHAR (1)      NULL,
    [Batch_Id]     UNIQUEIDENTIFIER NULL,
    [MatchesPlayed] INT         NULL,
    PRIMARY KEY CLUSTERED ([PlayerRankId] ASC)
)
WITH (DATA_COMPRESSION = ROW);


GO

