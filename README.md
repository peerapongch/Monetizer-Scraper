# money
scraping information from monetizer dashboard
+ and whatever comes after

includes the basic functionality of data extraction from monetizer
your username and password is hard coded to the script so you do not need to input them 

Instruction for running: 
1. Install python 3.x on your machine (any version of python 3 will do), Google Chrome, and ChromeDriver (this bit might be tricky, just google around where to put your chrome driver; its different for mac and windows)
2. Install the necessary packages by copying and pasting the following into terminal 
	pip install -r requirements.txt
and press enter (these are more packages than necessary but hey the more the merrier) 
3. Go to terminal and type 
	python makemoney_v2.py
4. it will prompt you to input the amount of time you want the script to run for (note that the unit is in minutes) 
5. the script will run and the csv file will be saved in the same directory as the script and named extract_liveleads.csv

Note: to change the file name or any other parameters, just edit in the script. they are listed as the first few variables 

Make it rain