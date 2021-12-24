CREATE TABLE IF NOT EXISTS "ActionTypes" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_ActionTypes" PRIMARY KEY AUTOINCREMENT,
    "Name" VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "CombinationTypes" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_CombinationTypes" PRIMARY KEY AUTOINCREMENT,
    "Name" VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "Actions" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_Actions" PRIMARY KEY AUTOINCREMENT,
    "Symbol" VARCHAR(10) NOT NULL UNIQUE,
    "Text" VARCHAR(50) NOT NULL UNIQUE,
    "ActionTypeId" INTEGER NOT NULL,
    CONSTRAINT "FK_Actions_ActionTypes_ActionTypeId" FOREIGN KEY ("ActionTypeId") REFERENCES "ActionTypes" ("Id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "Combinations" (
	"Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "CombinationTypeId"	INTEGER NOT NULL,    
	"Pattern"	VARCHAR(50) NOT NULL UNIQUE,
	"Text"	VARCHAR(200) UNIQUE,
	"ActionCount"	INTEGER NOT NULL,
    CONSTRAINT "FK_Combinations_CombinationTypes_CombinationTypeId" FOREIGN KEY ("CombinationTypeId") REFERENCES "CombinationTypes" ("Id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "CombinationActions" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_CombinationActions" PRIMARY KEY AUTOINCREMENT,
    "CombinationId" INTEGER NOT NULL,
    "ActionId" INTEGER NOT NULL,
    "Sequence" INTEGER NOT NULL,
    "SubSequence" INTEGER NOT NULL,
    CONSTRAINT "FK_CombinationActions_Combinations_CombinationId" FOREIGN KEY ("CombinationId") REFERENCES "Combinations" ("Id") ON DELETE CASCADE,
    CONSTRAINT "FK_CombinationActions_Actions_ActionId" FOREIGN KEY ("ActionId") REFERENCES "Actions" ("Id") ON DELETE CASCADE
);

CREATE INDEX "IX_Actions_ActionTypeId" ON "Actions" ("ActionTypeId");
CREATE INDEX "IX_CombinationActions_ActionId" ON "CombinationActions" ("ActionId");
CREATE INDEX "IX_CombinationActions_CombinationId" ON "CombinationActions" ("CombinationId");

CREATE UNIQUE INDEX "UIX_CombinationActions_CombinationId_ActionId_Sequence_SubSequence" ON "CombinationActions" (
	"CombinationId"	ASC,
	"ActionId"	ASC,
	"Sequence"	ASC,
	"SubSequence"	ASC
);


CREATE TABLE IF NOT EXISTS "Trainings" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_Trainings" PRIMARY KEY AUTOINCREMENT,
    "CreationDate" TEXT NOT NULL,
    "Description" VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS "TrainingCombinations" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_TrainingCombinations" PRIMARY KEY AUTOINCREMENT,
    "TrainingId" INTEGER NOT NULL,
    "CombinationId" INTEGER NOT NULL,
    "Sequence" INTEGER NOT NULL,
    "Repetition" INTEGER NOT NULL,
    CONSTRAINT "FK_TrainingCombinations_Trainings_TrainingId" FOREIGN KEY ("TrainingId") REFERENCES "Trainings" ("Id") ON DELETE CASCADE,
    CONSTRAINT "FK_TrainingCombinations_Combinations_CombinationId" FOREIGN KEY ("CombinationId") REFERENCES "Combinations" ("Id") ON DELETE CASCADE
);

CREATE INDEX "IX_TrainingCombinations_TrainingId" ON "TrainingCombinations" ("TrainingId");
CREATE INDEX "IX_TrainingCombinations_CombinationId" ON "TrainingCombinations" ("CombinationId");

CREATE UNIQUE INDEX "UIX_TrainingCombinations_TrainingId_CombinationId_Sequence_Repetition" ON "TrainingCombinations" (
	"TrainingId" ASC,
	"CombinationId"	ASC,
	"Sequence"	ASC,
    "Repetition"	ASC
);
