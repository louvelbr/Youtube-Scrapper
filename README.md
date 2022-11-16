# Youtube-Scrapper
Scrapping Youtube with BeautifulSoup  

Install requirements :
``pip install requirements.txt``  

Tests : 
``python -m pytest tests``  
Or just ``pytest`` if you take test_scapper.py out of tests/

Tests Coverage :
``pytest --cov=. tests/`` (not working)
If you take test_scapper.py out of tests/ and put it at the root then 81% coverage with the command : ``pytest --cov=.``

Run : 
``python scrapper.py --input input.json --output output.json``  

