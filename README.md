[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)

# [An Approximate Dynamic Programming Approach to Dynamic Stochastic Matching](https://doi.org/10.1287/ijoc.2021.0203)

This archive is distributed in association with the [INFORMS Journal on Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

The purpose of this repository is to share the source code used in the paper ["An Approximate Dynamic Programming Approach to Dynamic Stochastic Matching"](https://doi.org/10.1287/ijoc.2021.0203) by F. You and T. Vossen.

The code contains implementation of main model of the paper, benchmark approaches for comparision, numerical instance generation and experimentation.

## Dependencies
To replicate numerical experiments from the paper, or use the code to solve new dynamic stochastic matching instances, python packages `numpy`, `networkx`, as well as the `Gurobi` solver and the `gurobipy` package are required.

### Cite
To cite the contents of this repository, please cite both the paper and this repo, using their respective DOIs.

https://doi.org/10.1287/ijoc.2021.0203

https://doi.org/10.1287/ijoc.2021.0203.cd

Below is the BibTex for citing this version of the data.

```bib
@article{adp_matching_code,
    title = {An Approximate Dynamic Programming Approach to Dynamic Stochastic Matching},
    author = {F. You and T. Vossen},
    year = {2023},
    journal = {{INFORMS Journal on Computing}},
    doi={10.1287/ijoc.2021.0203.cd},
    note={available for download at https://github.com/INFORMSJoC/2021.0203}
}
```

## Replicate Experiments
Synthetic instance generation and numerical simulation code is provided:

to recreate ridesharing results, run `python src/ridesharing.py`

to recreate matchmaking results, run `python src/matchmaking.py`

to recreate kidney exchange results, run `python src/kidney.py`

## License
This software is released under the MIT license, which we report in file `LICENSE`.