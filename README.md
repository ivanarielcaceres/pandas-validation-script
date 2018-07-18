# Rules based Script with Pandas

Python script that validates each record in a CSV file based on predefined rules for each field.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them
The requisites is defined in requirements.txt file

```
pip install -r requirements
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
python Sales_transactional_Data_Other.py
```

Or

```
python Sales_transactional_Data.py
```

So each script is returning result=[check, n_check, t_check, l_check, p_check], for each file processed where each 0 element of lists are statements like: “Your file does not have name/type/length/pattern errors.” or “Your file contain N name/type/length/pattern errors”, where N number of errors of specific type and other elements of the list are strings saying the place where error appear (Column and row name).


## Running the tests

TODO

### Break down into end to end tests

TODO


## Built With

* [Python](https://www.python.org/) - The programming language used
* [Pandas](https://pandas.pydata.org/) - Library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming
* [NumPy](http://www.numpy.org/) - Scientific computing with Python

## Versioning

For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Iván Cáceres** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
