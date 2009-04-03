# most popular defs
# awk -F '\t' '{print $2 " " $1 | "sort -nr"}' defs-* | head -n 50

import UrbanDictionary
UrbanDictionary.lemma_pretty('fagtard', UrbanDictionary.statistics_for_lemma('fagtard'))