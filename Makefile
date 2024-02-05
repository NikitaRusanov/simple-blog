DC="docker-compose"
DC_FILE="docker-compose.yml"
TEST_FILE="docker-compose-test.yml"


run:
	${DC} -f ${DC_FILE} up -d ${ARGS}

stop:
	${DC} -f ${DC_FILE} down

logs:
	${DC} -f ${DC_FILE} logs -f

run-tests:
	${DC} -f ${TEST_FILE} up --attach test-runner && ${DC} -f ${TEST_FILE} down