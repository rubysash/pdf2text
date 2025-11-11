# pdf2text
Guts bloated pdf so it can be made into AI food

## Purpose
Reduce pdf (like a book) drastically.     For example 18MB becomes 100k.     

## Use Case
Claude Skills currently has an 8MB limit.  I want to train it with specific texts.    I can fit many compressed/gutted versions and get the same context almost by using this tool to strip out the text.


## Installation

```
git clone https://github.com/rubysash/pdf2text.git
python -m venv pdf2text
cd pdf2text
scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

