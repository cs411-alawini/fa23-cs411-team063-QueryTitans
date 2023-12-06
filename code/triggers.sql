DELIMITER //

CREATE TRIGGER before_insert_update_match
BEFORE INSERT ON Matches
FOR EACH ROW
BEGIN
  IF NEW.Match_Date > NOW() THEN
    SET NEW.Match_Status = 'Scheduled';
  ELSEIF NEW.Match_Date <= NOW() AND ADDTIME(NEW.Match_Date, '0:30:00') > NOW() THEN
    SET NEW.Match_Status = 'In Progress';
  ELSE
    SET NEW.Match_Status = 'Completed';
  END IF;
END;
//

CREATE TRIGGER before_update_match
BEFORE UPDATE ON Matches
FOR EACH ROW
BEGIN
  IF NEW.Match_Date > NOW() THEN
    SET NEW.Match_Status = 'Scheduled';
  ELSEIF NEW.Match_Date <= NOW() AND ADDTIME(NEW.Match_Date, '0:30:00') > NOW() THEN
    SET NEW.Match_Status = 'In Progress';
  ELSE
    SET NEW.Match_Status = 'Completed';
  END IF;
END;
//

DELIMITER ;


DELIMITER //