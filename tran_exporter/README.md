# Transaction Extract Automation

Please note, 10pow6 is **not affiliated in any way with Earth 2.**

Extracts your transactions excel. Script run as of 25 December 2020.  Site changes will end up breaking this.

Haven't been able to fully test this yet as the site has been down, but in theory should work based off unit tests.

**IMPORTANT** Never run any code / etc. from the internet if you don't know what it does. There are a lot of bad folks out there, and they could be malicious!

## General Setup Info

### Clone the directory
```
git clone https://github.com/10pow6/e2_tools.git
```

### Setup your venv
```
python -m venv venv
```

### Grab the appropriate chrome driver
https://chromedriver.chromium.org/
(Tested with ChromeDriver 87.0.4280.88)

### Run it!
```
tran_automation.py
```