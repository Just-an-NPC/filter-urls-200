# filter-urls-200
This is just a simple tool that is used to filter URLs and only displays URLs with a response code of 200

# Installation
git clone https://github.com/Just-an-NPC/filter-urls-200

# Usage
-o = output

--max_workers = This option allows you to specify the number of threads to use for parallel processing. By default, this value is 10. The higher the number of threads, the faster the URL processing if your system supports it.

example command :     
python3 filter_urls.py (file urls).txt -o filtered_urls.txt --max_workers 20
