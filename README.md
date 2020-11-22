# Qualification interface for TORQUE
This is the qualification interface for the EMNLP'20 paper -- TORQUE. The purpose of "qualification" is to test if a crowd worker understands one's annotation guidelines accurately via a set of multiple-choice questions.
```
@inproceedings{NWHPGR20,
  author={Qiang Ning and Hao Wu and Rujun Han and Nanyun Peng and Matt Gardner and Dan Roth},
  title={ {TORQUE}: A Reading Comprehension Dataset of Temporal Ordering Questions},
  booktitle={Proc. of EMNLP},
  year={2020}
}
```

When we collected TORQUE, we used a backend server which compared workers' submissions against our gold answers to each of the exam questions. For your reference, the code we ran on the backend server was `./main.py`. However, we deleted our gold answers from this repository, so you may find some non-existing directories `main.py` is referring to. **We want to highlight that our recent work, [Crowdaq](http://www.crowdaq.com/), can provide you with the qualification functionality much more easily.** Please check out Crowdaq if you need to set up qualification for your data collection project.

If you are in need of the test questions, please contact the authors directly.

## Project setup
Please install `npm` accordingly: https://nodejs.org/en/download/
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

Then you should be able to see messages like:
```
  App running at:
  - Local:   http://localhost:8080/ 
  - Network: http://xxx.xxx.xxx.xxx:8080/
```

### Compiles and minifies for production
```
npm run build
```

Then your distribution files should be in `./dist/` now.

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
