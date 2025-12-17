# raxtax_extension

## Overview
This repository contains a prototype implementation of an extension to
the raxtax workflow for taxonomic classification of DNA sequences. The
primary purpose of this repository is to support research and
development of the extended raxtax approach.

In addition to the prototype implementation, the repository also
contains an experimental and benchmarking pipeline used to evaluate the
method with respect to classification accuracy, robustness, runtime,
and memory behavior. These benchmarks were developed in the context of
a research project and are included to document and reproduce the
experimental results.

## Intended Scope and Usage
This repository is primarily intended as a research prototype rather
than a polished end-user tool. The benchmark and test pipelines are
included for experimental reproducibility and analysis, and may require
careful configuration and reading of the corresponding README files
before execution.

While the core components of the raxtax extension can be reused, the
benchmark orchestration code is tailored to specific experimental
setups and is not intended to serve as a general-purpose benchmarking
framework.

## Installation

### Requirements
- Conda (Miniconda)

### Setup
Clone the repository and navigate to the project root directory:

```
git clone https://github.com/Namdoooo/raxtax_extension.git
cd raxtax
```

Create a conda environment using the provided environment.yml file:

```
conda env create -f environment.yml
```

Activate the environment:

```
conda activate "./.conda_venv"
```

## Repository Structure
The repository is organized into the following main components:

- `raxtax_extension_prototype/`  
  Contains the source code of the raxtax extension prototype, including
  the core classification logic and supporting utilities.

- `simtools/`  
  Provides tools for dataset simulation, benchmark execution, and
  experiment orchestration. This directory contains code used to
  generate input data and to control experimental workflows.

- `analysis/`  
  Contains scripts used for post-processing, aggregation, and analysis
  of benchmark results, including the generation of plots and summary
  statistics.

- `benchmarks_hits/`  
  Contains benchmark-specific scripts, configurations, and archived
  result data. Each benchmark subdirectory includes its own README
  describing the experimental design, execution steps, and outputs.

- `pygargammel/`  
  Contains an external third-party tool and is
  not developed as part of the raxtax extension prototype.



## Benchmarks
All benchmarks are located in the benchmarks_hits/ directory.
Each benchmark directory is self-contained and includes:

- a detailed README
- execution scripts
- analysis scripts

The project is designed with reproducibility in mind.
Benchmarks explicitly document:

- parameter settings
- random seed usage
- commit hashes used for execution

Where required, additional manual steps (e.g. configuration file
generation or dataset pairing) are documented in the corresponding
README files.



## Notes
AI-based tools were used as assistance during development, primarily for
generating print and log messages, implementing visualization-related
functions and supporting code commenting and documentation.