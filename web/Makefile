all: nil

clean:
	$(RM) *.log *.pyc

drop:
	mysql -u root -p prout <drop_db.sql> drop_db.log

create:
	mysql -u root -p prout <create_db.sql> create_db.log

nil:
	echo "By default, do nothing"

