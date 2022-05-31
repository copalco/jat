# Job And Talent Developers Connector

## Installation

### docker-compose
1. install docker and docker-compose
2. Clone repository:  
   `git clone git@github.com:copalco/jat.git`
3. cd <directory you cloned the repo to>

### local
1. Install poetry package and dependency manager:  
`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`
2. Clone repository:  
`git clone git@github.com:copalco/jat.git`  
3. enter the cloned repository directory:
`cd <directory name>`
4. poetry install

## Running server instance

### docker-compose
1. docker-compose up -d web
2. go to browser and http://127.0.0.1:8080/connected/realtime/{REPLACE WITH handle}/{REPLACE WITH handle}
3. see result

## Tests

### Ci-build (unit tests, type check, style check)
`make ci-build`
### Integration tests
`make integration-tests`
### Acceptance tests
`make integration-tests`

## Problems
1. Realtime endpoint is as realtime as it's dependencies, so in case of twitter and github there is
a latency, but also rate limiting. That's why if I made that project for production I'd choose to
retrieve the users as a background task. As soon I'd get results id notify client somehow that we know it.

## Next steps I'd take
1. Make tokens secret (tokens are read only and restricted for minimum access)
2. Divide and implement acceptance tests
3. Handle error when checking one developer to himself
4. Simplify business logic in application layer of ConnectedQueryHandler
5. Return 422 for too long and too short handles error
6. Add centralized CI pipeline using github actions