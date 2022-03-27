IF NOT EXISTS (
        SELECT *
        FROM sys.databases
        WHERE name = 'MiijinDB'
        )
BEGIN
    CREATE DATABASE [MiijinDB]
END
GO

USE MiijinDB

GO

IF NOT EXISTS ( SELECT  *
                FROM    sys.schemas
                WHERE   name = N'MiijinDB' )
    EXEC('CREATE SCHEMA [MiijinDB]');
GO

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='employeeLunchRecords' and xtype='U')
    CREATE TABLE [MiijinDB].[employeeLunchRecords]
    (
        [employeeLunchID] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [employeeID] INT NOT NULL,
        [timeIDScanned] DATETIME NOT NULL
    )
GO

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='studentLunchRecords' and xtype='U')
    CREATE TABLE [MiijinDB].[studentLunchRecords]
    (
        [studentLunchID] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [studentID] INT NOT NULL,
        [timeIDScanned] DATETIME NOT NULL
    )
GO

INSERT INTO [MiijinDB].[employeeLunchRecords] (employeeID, timeIDScanned) VALUES (1, CURRENT_TIMESTAMP)
INSERT INTO [MiijinDB].[studentLunchRecords] (studentID, timeIDScanned) VALUES (1, CURRENT_TIMESTAMP)