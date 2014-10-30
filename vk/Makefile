all: setup

.PHONY: setup test clean help run stop

setup:
	virtualenv pybox
	pybox/bin/pip install -Ur requirements.txt
	mkdir -p tmp/
	mkdir -p db/

run:
	mongod --config smtac.conf &

stop:
	mongo --port 6060 --eval "db.getSiblingDB('admin').shutdownServer()"

clean:
	rm -rf pybox/
	rm -rf tmp/
