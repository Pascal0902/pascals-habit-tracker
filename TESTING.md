# Test Suite for Pascal's Habit Tracker

This repository now includes comprehensive tests for all core modules of the Pascal's Habit Tracker application.

## Test Coverage

The test suite covers the following modules:

### Core Modules Tested
- **habit_tracking**: Core habit and user management functionality
- **data_storage**: JSON-based persistence layer
- **habit_analysis**: Analytics and streak calculation functions
- **cli_menu**: Command-line interface utilities

### Test Structure

```
tests/
├── __init__.py
├── test_integration.py          # Integration tests across modules
├── habit_tracking/
│   ├── __init__.py
│   ├── test_habits.py          # Tests for Habit and UserHabit classes
│   └── test_users.py           # Tests for User class
├── data_storage/
│   ├── __init__.py
│   ├── test_interface.py       # Tests for StorageInterface abstract class
│   └── test_json_storage.py    # Tests for JsonStorageInterface implementation
├── habit_analysis/
│   ├── __init__.py
│   └── test_analytics.py       # Tests for analytics functions
└── cli_menu/
    ├── __init__.py
    └── test_cli_utils.py        # Tests for CLI utility functions
```

## Running Tests

### Prerequisites
```bash
pip install pytest pytest-cov
```

### Run All Tests
```bash
pytest
```

### Run Tests with Coverage Report
```bash
pytest --cov=src --cov-report=term-missing
```

### Run Specific Test Modules
```bash
# Run only habit tracking tests
pytest tests/habit_tracking/

# Run only data storage tests
pytest tests/data_storage/

# Run only habit analysis tests
pytest tests/habit_analysis/

# Run only CLI tests
pytest tests/cli_menu/

# Run integration tests
pytest tests/test_integration.py
```

### Run with Verbose Output
```bash
pytest -v
```

## Test Configuration

The test suite is configured via `pytest.ini`:
- Coverage minimum threshold: 50%
- HTML coverage reports generated in `htmlcov/`
- Filters out deprecation warnings

## Test Features

### Comprehensive Coverage
- **Unit Tests**: Individual class and function testing
- **Integration Tests**: Cross-module functionality verification
- **Edge Case Testing**: Boundary conditions and error scenarios
- **Mock Testing**: Time-dependent functionality with controlled datetime

### Key Test Areas

#### Habit Tracking Module
- Habit creation with various periods (daily, weekly, monthly, quarterly, annually)
- Period calculation algorithms for all habit types
- Completion tracking and validation
- User habit management (add, remove, track)
- JSON serialization and deserialization

#### Data Storage Module
- Abstract interface compliance
- JSON file persistence
- CRUD operations for users, habits, and user habits
- Error handling for non-existent files and invalid data
- Cross-instance data persistence

#### Habit Analysis Module
- Streak calculation algorithms
- Current vs. all-time streak tracking
- Multi-user analytics
- Period-specific habit filtering
- Edge cases with no completion data

#### CLI Menu Module
- Multi-page option selection menus
- Navigation between pages
- Input validation and error handling
- User interaction flow testing

#### Integration Tests
- End-to-end workflow testing
- Cross-module data consistency
- Persistence across storage instances
- Multi-user isolation verification

## Test Statistics

- **Total Tests**: 114 tests
- **Test Files**: 7 test files
- **Coverage**: ~53% of source code
- **Modules Covered**: 4 core modules

## Test Data Management

Tests use:
- Temporary files for storage testing
- Mock datetime objects for time-dependent tests
- Isolated test environments to prevent interference
- Automatic cleanup of test artifacts

## Running in CI/CD

The test suite is designed to run in continuous integration environments:
- No external dependencies beyond pytest
- Self-contained test data
- Deterministic test results
- Fast execution (< 1 second for full suite)

## Contributing to Tests

When adding new features:
1. Add corresponding unit tests
2. Update integration tests if cross-module functionality is affected
3. Ensure coverage remains above 50%
4. Test edge cases and error conditions
5. Use descriptive test names and docstrings

## Test Quality Features

- **Descriptive Test Names**: Clear indication of what each test validates
- **Comprehensive Docstrings**: Explanation of test purpose and expectations
- **Setup/Teardown**: Proper test isolation and cleanup
- **Mock Usage**: Time-dependent tests use proper mocking
- **Edge Case Coverage**: Tests boundary conditions and error scenarios
- **Cross-Platform**: Tests work on different operating systems

## Coverage Report

To generate an HTML coverage report:
```bash
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in your browser
```

This provides detailed line-by-line coverage information for all source files.