# Script tools for Rune Factory 2,3,4
Extract / import scripts with rune factory 2,3,4

If you need help about extract / import texts, please email to me.
## Extract
`extract.py [file] [output] [table_file]`

You need to manually change `encoding table files` in python script.

## Import
`import.py [file] [output] [table_file]`

You need to manually change `encoding table files` in python script.

Also, set your `NULLBYTES` for builds. For example, on RF2 and some RF3 script files are use 1-byte `NULLBYTES(00)` after text ends, but RF3 main script use 2-bytes `NULLBYTES(0000)` after text ends. you should change your `NULLBYTES` before use.

```diff
-- NULLBYTES = 0000
++ NULLBYTES = 00
```

## Table File?
For localization, we use specific table file. RF uses utf-8 encodings, so you need to use UTF-8 encoding table file. Such as: `UTF8_JPN.tbl`


## Other Scripts
* `Text_fit_checker.py` : Help checking your text fits with screen.
* `Text_Checker.py` : Help checking the control texts (Newline and texts between @) are written properly.