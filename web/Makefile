all: drop create clean

clean:
	$(RM) *.log *.pyc

drop:
	mysql -u root -p -D '' <drop_db.sql> drop_db.log

create:
	mysql -u root -p -D ''  <create_db.sql> create_db.log

nil:
	echo "By default, do nothing"

cleandb:
	mysql -u root -p -D '' <clean_db.sql> clean_db.log
