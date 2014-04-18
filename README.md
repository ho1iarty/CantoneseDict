CantoneseDict
=============

A tool for creating a Cantonese dictionary(jyutping).
### Usage
1. Add Characters
	`python zi_dict.py`

2. Add Words
    `python ci_dict.py`

### Dependencies
* [pyquery][1]
* [progressbar][2]

### Data Structure
```SQL
TABLE DICT_ZI(ZI TEXT, YIN TEXT)
TABLE DICT_CI(FAN TEXT, JIAN TEXT, YIN TEXT, YI TEXT)
```

### Input (Dictionary Source)
* **[JyutEnDict.u8][3]**. jyutping to English dictionary.
* **[gbk_zi][4]**. Chinese Internal Code Specification.
* **[Cantonese Pronunciation List of the Characters for Computers.][5]**


### Output
**jyut_zh.dict**. SQLite db file.


  [1]: https://pypi.python.org/pypi/pyquery
  [2]: http://code.google.com/p/python-progressbar/
  [3]: http://sourceforge.net/projects/e-guidedog/files/related%20third%20party%20software/0.3/JyutEnDict.zip/download
  [4]: http://ff.163.com/newflyff/gbk-list/
  [5]: http://www.iso10646hk.net/jp/
