# One_Piece_Scan

## Presentation of the Project

The objective of this project is to gather information regarding the release of manga chapters (scans) for One Piece and summarize this important information on an HTML page. The information we aim to collect includes a summary of the latest chapter, the release date of the next scan while determining if there is a break, and, in the case of a break, an explanation for it (Eiichiro Oda, the author of One Piece, often takes breaks due to health issues stemming from his lifestyle, intensive work rhythm, and age, which frequently lead to publication interruptions ranging from one week to a month).

1) To achieve this, we will use youtube_transcript_api to retrieve subtitles from the latest videos of the "Mont Corvo" channel, which provides reviews and analyses of recent chapters. Once the subtitles from these review videos are retrieved, we will exploit the LLM Llama *(Llama – 3.3-70B)* to automatically summarize the latest chapter and publish relevant theories.

2) To verify the release date of the next chapter and gather information regarding any delays, we will also scrape the Dextero website to obtain the most up-to-date information available at the time of the program’s execution.

3) We use a sqlite database to store information from youtube and scrapping. 

4) We have a script that checks whether the latest chapter has been released or not.

5) We also have a CSV file containing the scheduled release dates of scans and break periods for an entire year.

Since One Piece chapters are legally published on Sundays, and analysis videos are released on the same day, we will verify whether a chapter is scheduled for release that week by consulting the CSV file **(4)**. If the CSV indicates a break week, our HTML page will display that it is a break week, along with the next scheduled release date. If a chapter is scheduled for release, we will then verify if the scan has been published that week **(3)**. If so, the YouTube subtitles script will execute (summary-analysis and theory generation) **(1)**. Otherwise, the script will retrieve justification details from Dextero **(2)**.


## Our tree structure :
```
```

## Development Environment:
Requierments:
Python 3.10+

Clone this repository on your local machine :
```
git clone https://github.com/wlemalin/one_piece_scan
```

**Navigate to the project directory and install the dependencies :**
```
cd one_piece_scan
pip install -r requirements.txt
```


## Execution of the scripts

To initialize database use 
```
flask --app flaskr run --debug 
```

To run the application use 
```
flask --app flaskr init-db 
```

To update database execute add_db.py

You can try your own examples in add_db.py, after initializing database.
html need changes, take inspiration from flask tutorial.

