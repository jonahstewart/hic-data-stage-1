# HIC to CSV

This project extracts post data from the HIC website, cleans it and identifies variables of interests, and stores them in a CSV file. This is part 1 of a wider database reorganization project.

## Files

extract.py extract XML data downloaded from the HIC site (posts.xml), cleans it, and exports it to posts_data.csv

## Variables

The current variables are as follows.

Title: Title of HIC post

Dates: Dates as written on website

Month: Month extracted from body of posts where available

Year: Year from tag

Location: Location as written in body of HIC post

State: Extracted from tag

Categories: Categories from WP

Fatalities: Tracks if "Fatality" is present in Categories.

Perpetrator: Uses title data to determine if the perpetrator was a parent (e.g., "Child of X"), or someone outside the immediate family (e.g., "Child by Y"). This is an imperfect process, and should be double-checked by a human.
