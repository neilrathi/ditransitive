# ditransitive

## directory

* `models` contains WebPPL models for RSA speakers
* `priors` contains code for generating priors (as well as actual priors)
* `analysis.R` merges `priors` and `models` to generate and analyze data
* `plots` contains plots generated by `analysis.R`

## requirements

* python 3
* huggingfacee transformers
* gpu pytorch
* tidyr