import pandas as pd
import sys

merged = pd.read_csv(sys.argv[1], names=('id', sys.argv[1]))

for wiki in sys.argv[2:]:
    print wiki
    next_wiki = pd.read_csv(wiki, names=('id', wiki))
    merged = pd.merge(merged, next_wiki, on='id', how='outer')

print 'merging'
merged.to_csv('all_predictions.csv', index=False)

