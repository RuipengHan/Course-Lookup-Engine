-- use production;
-- select * from Comments where course = 1721;

drop trigger CommentTrig;

DELIMITER //

CREATE TRIGGER CommentTrig
	BEFORE INSERT ON Comments
	FOR EACH ROW
    
BEGIN
	SET @TotalCommentNum = (SELECT COUNT(commenter) FROM Comments WHERE course = new.course);
	IF @TotalCommentNum >= 5 THEN
		SET new.comment = concat("new comment: ", new.comment);
	END IF;
    
END //

DELIMITER ;

-- INSERT INTO Comments VALUES (3000,103,1721,"test0",'2010-12-31 01:15:00',1941,134,NULL);
-- INSERT INTO Comments VALUES (3001,103,1721,"test1",'2010-12-31 01:15:00',1941,134,NULL);
-- INSERT INTO Comments VALUES (3002,103,1721,"test2",'2010-12-31 01:15:00',1941,134,NULL);
-- INSERT INTO Comments VALUES (3003,103,1721,"test3",'2010-12-31 01:15:00',1941,134,NULL);
-- INSERT INTO Comments VALUES (3004,103,1721,"test4",'2010-12-31 01:15:00',1941,134,NULL);