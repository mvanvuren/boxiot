INSERT INTO Trainings (CreationDate, Description) VALUES (CURRENT_TIMESTAMP, 'all combinations');

INSERT INTO TrainingCombinations (TrainingId, CombinationId, Sequence, Repetition)
	SELECT
		(SELECT Id FROM Trainings ORDER BY Id DESC LIMIT 1) AS TrainingId
	,	cbs.Id AS CombinationId
	,	cbs.Id AS Sequence
	,	(3 + abs(random() % 3)) AS Repetition		
	FROM
		Combinations cbs;