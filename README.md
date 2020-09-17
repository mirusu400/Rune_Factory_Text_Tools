# Script tools for Rune Factory 2,3,4
Extract / import scripts with rune factory 2,3,4

If you need help about extract / import texts, please email to me.
## Extract
`RFTxtExtract.py [file] [output]`

You need to manually change `encoding table files` in python script.
```diff
--tablefile="수정UTF_일어_대사추출.tbl"
++tablefile="YOUR_TABLE_FILE"
```
## Import
`RFTxtImport.py [file] [output]`

You need to manually change `encoding table files` in python script.
```diff
--tablefile="수정UTF_일어_대사추출.tbl"
++tablefile="YOUR_TABLE_FILE"
```

## Table File?
For localization, we use specific table file. RF uses utf-8 encodings, so you need to use UTF-8 encoding table file. Such as: `UTF8_JPN.tbl`


## Other Scripts
* `Text_fit_checker.py` : Help checking your text fits with screen.
* `Text_Checker.py` : Help checking the control texts (Newline and texts between @) are written properly.