#!/bin/bash
mysql -u root -p prout < drop_db.sql > drop.log
mysql -u root -p prout < install_db.sql > install.log
