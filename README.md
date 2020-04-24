# PosterChat

## Testing

We use Django's built-in unittesting framework to run QA. For example, to run tests on the core app:

```
(pc) seranthirugnanam@MBP001 PosterChat % python manage.py test core.tests.UserModelTests
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....
----------------------------------------------------------------------
Ran 5 tests in 6.107s

OK
Destroying test database for alias 'default'...
```
