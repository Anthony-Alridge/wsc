# WinoGrande 

Version 1.1.beta (Nov 21th, 2019)

- - - 

## Data

    ./data/
    ├── train_[xs,s,m,l,xl].jsonl          # training set with differnt sizes
    ├── train_[xs,s,m,l,xl]-labels.lst     # answer labels for training sets
    ├── dev.jsonl                          # development set
    ├── dev-labels.lst                     # answer labels for development set
    └── test.jsonl                         # test set
    
You can use `train_*.jsonl` for training models and `dev` for validation.
Please note that labels are not included in `test.jsonl`. 


## Evaluation

Coming soon.

    
## Reference
If you use this dataset, please cite the following paper:

	@article{sakaguchi2019winogrande,
	    title={WinoGrande: An Adversarial Winograd Schema Challenge at Scale},
	    author={Sakaguchi, Keisuke and Bras, Ronan Le and Bhagavatula, Chandra and Choi, Yejin},
	    journal={arXiv preprint arXiv:1907.10641},
	    year={2019}
	}


## License 

Winogrande dataset is licensed under CC BY 2.0.


## Questions?

You may ask us questions at our [google group](https://groups.google.com/a/allenai.org/forum/#!forum/winogrande).


## Contact 

Email: keisukes[at]allenai.org
