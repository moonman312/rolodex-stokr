# rolodex-stokr
I'm one of the worst people at keeping up with others as much as I wish I would. 

I want to build some kind of super simple personal tool or something super simple that has a list of people I want to stay in touch with and then I can set how often I want to stay in touch with each of them and then it reminds me everyday with the list of people in order of how overdue it is until I confirm I have interacted with them and their timer is restarted.

This is a personal project for my own utility, but if you have the same struggle, feel free to clone it


## Set Up
crontab -e
to run the script at 9am every morning:
```0 9 * * * /usr/bin/python3 /path/to/your/script.py```


Edit EXAMPLE_contact_data.txt with the following format and change the name of the file to contact_data.txt
[
  {"name": "John Doe", "frequency": 7, "last_interaction": "2024-02-10", "next_interaction": "2024-02-17"},
  {"name": "Jane Smith", "frequency": 14, "last_interaction": "2024-02-08", "next_interaction": "2024-02-22"},
  {"name": "Bob Johnson", "frequency": 30, "last_interaction": "2024-02-05", "next_interaction": "2024-03-06"}
]


You can send emails with the subject "Interaction Update" and the following content (meaning you have):
```
John Doe
yes
2024-02-18  # Optional: Set a specific date for the next interaction
```

or (meaning you haven't yet)
```Jane Smith
no
```
