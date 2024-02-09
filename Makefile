DC=docker-compose
DC_FILE=docker-compose.yml
ENV_FILE=.env
TEST_DC_FILE=docker-compose-test.yml
TEST_ENV_FILE=.test.env


run:
	${DC} --env-file=${ENV_FILE} -f ${DC_FILE} up -d ${ARGS}

stop:
	${DC} -f ${DC_FILE} down -v

logs:
	${DC} -f ${DC_FILE} logs -f

run-tests:
	${DC} --env-file=${TEST_ENV_FILE} -f ${TEST_DC_FILE} up --attach test-runner && ${DC} -f ${TEST_DC_FILE} down -v