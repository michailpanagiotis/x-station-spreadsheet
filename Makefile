send:
	scp last_sent.xlsx nuc_local:/tmp/last_sent.xlsx; ssh nuc_local -t 'command; /home/pmichail/Projects/x-station-spreadsheet/sendxlsx.py /tmp/last_sent.xlsx'
