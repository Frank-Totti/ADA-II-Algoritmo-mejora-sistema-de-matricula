# How to Use the Input Parser

To use the input parser function from another file, import it as follows:

```python
from input_output.input import parse_input_file
```

Then, you can use the function like this:

```python
course_index_by_code, capacities, requests_by_student = parse_input_file(path)
```

- `path` should be the path to your input file.
- The function will return:
  - `course_index_by_code`: Dictionary mapping course codes to indices.
  - `capacities`: List of course capacities.
  - `requests_by_student`: Dictionary mapping student codes to their list of (course_idx, priority) requests.

