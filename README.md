# Command Line List Comprehension
A command line tool realizing declarative style list comprehensions as opposed to most shells' imperative loops.

## Usage

#### Simple Map/Filter
Print numbers 6-10
```
:{ echo x : x - seq 1 10 ? [ x -gt 5 ] }:
```

#### Multiple inputs
Combinates all input lines (i.e. {1..5}+{1..5})
```
:{ echo x+y : x - seq 1 5 , y - seq 1 5 }:
```

## Requirements
 - Python 3

## Installation
```
git clone https://github.com/meipp/Command-Line-List-Comprehension
alias :{="path/to/Command-Line-List-Comprehension/list-comprehension.py"
```

## TODO
 - stdin as input
 - files as input without use of cat
 - nested list comprehensions
