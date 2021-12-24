-- starter
INSERT INTO Trainings (CreationDate, Description) VALUES (CURRENT_TIMESTAMP, 'starter combinations');

INSERT INTO TrainingCombinations (TrainingId, CombinationId, Sequence, Repetition)
	SELECT
		(SELECT Id FROM Trainings ORDER BY Id DESC LIMIT 1) AS TrainingId
	,	cbs.Id AS CombinationId
	,	cbs.Id AS Sequence
	,	(3 + abs(random() % 3)) AS Repetition		
	FROM
		Combinations cbs
	INNER JOIN
		CombinationTypes cts
	ON
		cbs.CombinationTypeId = cts.Id
	WHERE
		cts.Name IN ('starter');

-- basic
INSERT INTO Trainings (CreationDate, Description) VALUES (CURRENT_TIMESTAMP, 'basic combinations');

INSERT INTO TrainingCombinations (TrainingId, CombinationId, Sequence, Repetition)
	SELECT
		(SELECT Id FROM Trainings ORDER BY Id DESC LIMIT 1) AS TrainingId
	,	cbs.Id AS CombinationId
	,	cbs.Id AS Sequence
	,	(3 + abs(random() % 3)) AS Repetition		
	FROM
		Combinations cbs
	INNER JOIN
		CombinationTypes cts
	ON
		cbs.CombinationTypeId = cts.Id
	WHERE
		cts.Name IN ('basic');        

--evasive
INSERT INTO Trainings (CreationDate, Description) VALUES (CURRENT_TIMESTAMP, 'evasive combinations');

INSERT INTO TrainingCombinations (TrainingId, CombinationId, Sequence, Repetition)
	SELECT
		(SELECT Id FROM Trainings ORDER BY Id DESC LIMIT 1) AS TrainingId
	,	cbs.Id AS CombinationId
	,	cbs.Id AS Sequence
	,	(3 + abs(random() % 3)) AS Repetition		
	FROM
		Combinations cbs
	INNER JOIN
		CombinationTypes cts
	ON
		cbs.CombinationTypeId = cts.Id
	WHERE
		cts.Name IN ('evasive');

-- ender
INSERT INTO Trainings (CreationDate, Description) VALUES (CURRENT_TIMESTAMP, 'ender combinations');

INSERT INTO TrainingCombinations (TrainingId, CombinationId, Sequence, Repetition)
	SELECT
		(SELECT Id FROM Trainings ORDER BY Id DESC LIMIT 1) AS TrainingId
	,	cbs.Id AS CombinationId
	,	cbs.Id AS Sequence
	,	(3 + abs(random() % 3)) AS Repetition		
	FROM
		Combinations cbs
	INNER JOIN
		CombinationTypes cts
	ON
		cbs.CombinationTypeId = cts.Id
	WHERE
		cts.Name IN ('ender');

-- in-fighting
INSERT INTO Trainings (CreationDate, Description) VALUES (CURRENT_TIMESTAMP, 'in-fighting combinations');

INSERT INTO TrainingCombinations (TrainingId, CombinationId, Sequence, Repetition)
	SELECT
		(SELECT Id FROM Trainings ORDER BY Id DESC LIMIT 1) AS TrainingId
	,	cbs.Id AS CombinationId
	,	cbs.Id AS Sequence
	,	(3 + abs(random() % 3)) AS Repetition		
	FROM
		Combinations cbs
	INNER JOIN
		CombinationTypes cts
	ON
		cbs.CombinationTypeId = cts.Id
	WHERE
		cts.Name IN ('in-fighting');

-- advanced
INSERT INTO Trainings (CreationDate, Description) VALUES (CURRENT_TIMESTAMP, 'advanced combinations');

INSERT INTO TrainingCombinations (TrainingId, CombinationId, Sequence, Repetition)
	SELECT
		(SELECT Id FROM Trainings ORDER BY Id DESC LIMIT 1) AS TrainingId
	,	cbs.Id AS CombinationId
	,	cbs.Id AS Sequence
	,	(3 + abs(random() % 3)) AS Repetition		
	FROM
		Combinations cbs
	INNER JOIN
		CombinationTypes cts
	ON
		cbs.CombinationTypeId = cts.Id
	WHERE
		cts.Name IN ('advanced');
