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
1. put own github personal access token and twitter api token to tokens.env file in the root project directory
2. docker-compose up -d web
3. go to browser and http://127.0.0.1:8080/connected/realtime/{REPLACE WITH handle}/{REPLACE WITH handle}
4. go to browser and http://127.0.0.1:8080/connected/register/{REPLACE WITH handle}/{REPLACE WITH handle}
5. you can see stored data in "data" directory in the root of repository events are stored in csv file

### localy
1. Export environment variables: *JAT_GITHUB_API_TOKEN* *JAT_TWITTER_API_TOKEN* to allow access to the services
## Tests

### Ci-build (unit tests, type check, style check)
`make ci-build`
### Integration tests
`make integration-tests`
### Acceptance tests
`make integration-tests`

## Solutions
1. As I saw that register endpoint contains history of developers connection, I immediatelly decided
that I should use event sourced model for Connection. This granted me history for "free".
2. I decided to use DDD approach so that my project would be understandable not only for developers, but
for business people too. I hope it is.
3. I used Starlette framework for the first time. I was reluctant to do so earlier cause it does not allow
to compose routes using class instances. Only functions or classes as types are allowed. I overcame that by using
simple clojure pattern.

## Problems
1. Realtime endpoint is as realtime as it's dependencies, so in case of twitter and github there is
a latency, but also rate limiting. That's why if I made that project for production I'd choose to
retrieve the users as a background task. As soon I'd get results id notify client somehow that we know it.
2. Since I stopped pursuing working acceptance test (what I do for the real production code) I had no simple way
to assure me that I'm going in the right direction. Big mistake. In order to gain time I lost it for debugging and manual
testing using browser. I kept telling to myself it's almost finished, just one steep hill to go. And again, and again.
I guess we all sometimes fall prey to sunken cost fallacy.
3. I set a very strict typing policy which slowed me down. It made the task harder sometimes.
4. Since I had only little time to do this. I felt pressure which pushed me to be faster, and as a result it was slower than if
I kept steady pace. Also it caused me to finish the project not as tidy as I'd like.

## Shortcuts
1. I resigned from setting up github actions pipeline as it would take a lot of time, and I created local ci build make command
to run tests and checks locally.
2. I left some duplication that could be removed e.g UserRetrievers.
3. Some code is tested indirectly which makes pinpointing issues more difficult
4. to improve the performance of **register** endpoint i'd implement readmodel and keep it in memory, but I'd do it later. 

## Next steps I'd take
1. Divide and implement acceptance tests
2. Handle threshold reaching errors from Twitter and Github
3. Handle error when checking one developer to himself
4. Simplify business logic in application layer of ConnectedQueryHandler
5. Return 422 for too long and too short handles error
6. Add centralized CI pipeline using github actions
7. Make tokens secret (tokens are read only and restricted for minimum access)
8. Create a mock server for acceptance tests and future performance tests
9. Setup observablity to be able to notice problems with application