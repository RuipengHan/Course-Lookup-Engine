DELIMITER //
create PROCEDURE GetaverageRating2(in courseid int)
	BEGIN
        declare done int default 0;
		declare sum_quality int default 0;
		declare sum_prof int default 0;
		declare sum_work int default 0; 
		Declare sum_rubric int default 0;
		declare sum_diff int default 0;
        declare sum_gpa int default 0;
        declare counter int default 0;
        declare subject_ varchar(40);
        declare course_number_ int;
        declare id_ int;
        declare overall_quality_ int;
        declare professor_ int;
        declare workload_ int;
        declare rubric_ int;
		declare difficulty_ int;
        declare grade_Rceived_ int;
		Declare customer_cursor CURSOR FOR select c.subject, c.course_number,c.id,r.overall_quality,r.professor,r.workload,r.rubric,r.difficulty,(CASE grade_Rceived WHEN 'A' Then 4
                   WHEN 'B' Then 3
                   WHEN 'C' Then 2
                   WHEN 'D' Then 1
                   WHEN 'F' Then 0 end)
		from Ratings r join Courses c on (c.id = r.course)
		where c.id = courseid;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
		
        DROP TABLE IF EXISTS finaltable;
        CREATE TABLE finaltable(
			subject varchar(40),
            course_number int,
            id int,
            avg_quality float,
            avg_prof float,
            avg_work float,
            avg_rubric float,
            avg_diff float,
            avg_gpa float
        );
        open customer_cursor;
        repeat
			fetch customer_cursor into subject_, course_number_,id_,overall_quality_,professor_,workload_,rubric_,difficulty_,grade_Rceived_;
				SET sum_quality = sum_quality + overall_quality_;
                SET sum_prof = sum_prof + professor_;
                SET sum_work = sum_work + workload_;
                SET sum_rubric = sum_rubric + rubric_;
                SET sum_diff = sum_diff + difficulty_;
                SET sum_gpa = sum_gpa + grade_Rceived_;
                set counter = counter + 1;
		until done 
        end repeat;
        close customer_cursor;
		insert into finaltable
        values(subject_, course_number_, id_,sum_quality/counter,sum_prof/counter,sum_work/counter,sum_rubric/counter,sum_diff/counter,sum_gpa/counter);
        select * from finaltable;
        end;//
DELIMITER ;