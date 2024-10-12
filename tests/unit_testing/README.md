## Unit Tests

Use this folder to place your unit tests.

#### Naming Convention

The naming convention for unit tests is as follows:

`test_<entity>_<part>.py`

The `test_` part is **mandatory**, as it is needed by `pytest` to identify the test files.

Each test function **must** also start with `test_`.

#### Running Tests

To run the tests, execute the following command:

```bash
pytest tests/unit_testing
```

or to run all tests:

```bash
pytest
```
