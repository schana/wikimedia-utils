import pandas as pd


'''
First, get the relevant data from dumps/mysql

Sitelinks:
mysql --host analytics-store.eqiad.wmnet wikidatawiki -e "select concat('Q', ips_item_id) as id, ips_site_id as site, replace(ips_site_page, ' ', '_') as title from wb_items_per_site join page on page_title = concat('Q', ips_item_id) where page_namespace = 0 and ips_site_id like '%wiki';" > sitelinks.tsv

Pagecounts:
wget https://dumps.wikimedia.org/other/pagecounts-ez/merged/pagecounts-2017-04-views-ge-5-totals.bz2
bunzip2 pagecounts-2017-04-views-ge-5-totals.bz2
echo "site title pageviews" > pagecounts.ssv
grep -e '^[a-z]*\.z ' --color=no pagecounts-2017-04-views-ge-5-totals | sed 's/\.z /wiki /' >> pagecounts.ssv
'''


pagecounts = pd.read_csv('pagecounts.ssv', sep=' ')
sitelinks = pd.read_csv('sitelinks.tsv', sep='\t')
merged = pd.merge(sitelinks, pagecounts, on=['site', 'title'])
merged.to_csv('sitelinks-pagecounts.csv')

