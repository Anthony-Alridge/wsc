# Injecting commonsense reasoning into the Winograd Schema Challenge

This repository contains work submitted for the 'Injecting commonsense reasoning into the Winograd Schema Challenge' MEng project.
The repository contains code aimed at generating ASP programs capable of solving Winograd Schema problems.

## Instructions
This project requires clingo and ILASP to run. These are provided in the lib directory.
The required python packages can be installed with pip via the requirements.txt file.


The entry point to the program is main.py. Instructions for running the program and args are given below. The easiest way to run
the program is via the ./run_main script, which already provides suitable arguments.


usage: main.py [-h] [--train_path TRAIN_PATH] [--test_path TEST_PATH]
               [--ne NE] [-d] [--model_name MODEL_NAME] [--mode MODE]

Solve WSC problems.

optional arguments:


  -h, --help            show this help message and exit


  --train_path TRAIN_PATH
                        The path to the input file for training
  
  --test_path TEST_PATH
                        The path to the input file for evaluation data.
  
  --ne NE               A hyper-parameter determining the max number of
                        examples to use as background knowledge per input.
  
  -d                    Sets program into debug mode, meaning progress will be
                        saved to files.
  
  --model_name MODEL_NAME
                        The model to use, one of {ConceptNetTranslation,
                        ILASPTranslation}
  
  --mode MODE           The learning mode, one of {batch, iterative}. Only
                        applies to ILASPTranslation

## Files and directories
### Data
See the data directory for training data (train_xl) and the benchmark dataset (wsc273).
### Conceptnet
See the conceptnet directory for the conceptnet local database, and code for downloading data from conceptnet.
### main.py
Entry point to the system.

Other files:
- semantic_extraction.py: Convert text into semantic properties. These can be converted into ASP.
- asp_converter.py: Convert parsed predicates into a commonsense program using conceptnet or ilasp.
- clingo_runner.py: Run the answer set solver.
- wsc_solver.py: Linking everything together to solve Winograd Schemas
- sentence_finder.py: For ILASP. Gathers similar sentences to input test instance.
- main.py: Entry point and evaluation
