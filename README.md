# Tornado Skeleton - example of an API scaffold using Tornado

## Description
Tornado Skeleton is a project that aims to set a coding convention and a project structure to follow when developing 
an API using the Python Tornado Framework.

This skeleton is heavily inspired by Gandalf (https://github.com/tradelab/gandalf), one would like to check it to see how it is used. 

## Project Structure
```
tornado_skeleton/
    bin/
        tornado_skeleton_app.py
    config/
        tornado_skeleton.dev.yaml
        tornado_skeleton.prod.yaml
        tornado_skeleton.yaml
    tornado_skeleton/
        api/
            handlers/
                __init__.py
                base_handler.py
                main_handler.py
                user_handler.py
            __init__.py
            response_errors.py
            tornado_skeleton_api.py
        helpers/
            error_code.py
        models/
            __init__.py
            user.py
    tests/
    .gitignore
    README.md
    requirements.txt
```

## Detail of the project
### bin
### config
### tornado_skeleton
### tests
