# Job And Talent Developers Connector

## Installation

### local
1. Install poetry package and dependency manager:  
`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`
2. Clone repository:  
`git clone git@github.com:copalco/jat.git`  
3. enter the cloned repository directory:
`cd <directory name>`
4. poetry install

## Tests

### Ci-build (unit tests, type check, style check)
`make ci-build`
### Integration tests
`make integration-tests`
### Acceptance tests
`make integration-tests`
