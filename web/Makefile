all: drop create 

clean:
	$(RM) *.log *.pyc

create:
	mysql -u root -p prout <create_db.sql> create_db.log

drop:
	mysql -u root -p prout <drop_db.sql> drop_db.log
