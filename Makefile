# DEVICE
send_to_device:
	ssh nuc_local -t 'command; amidi -s /tmp/last_sent.syx -p hw:1,0,0'

clean_received:
	ssh nuc_local -t 'command; rm -f /tmp/last_received.syx'

receive_from_device:
	ssh nuc_local -t 'command; rm -f /tmp/last_received.syx; ~/Projects/x-station-spreadsheet/read.py /tmp/last_received.syx'

# CONVERSIONS
convert_to_syx:
	./convert.py syx "$(FILE)" --output /tmp/last_sent.syx

convert_to_json:
	./convert.py json "$(FILE)" --output /tmp/last_sent.json

convert_to_xlsx:
	./convert.py xlsx /tmp/last_received.syx --output last_received.xlsx

# SSH
send_to_remote:
	scp /tmp/last_sent.syx nuc_local:/tmp/last_sent.syx

receive_from_remote:
	scp nuc_local:/tmp/last_received.syx /tmp/last_received.syx

# COMMANDS

send: convert_to_syx send_to_remote send_to_device

send_json: convert_to_json
	scp /tmp/last_sent.json nuc_local:.config/REAPER/Data/helgoboss/realearn/presets/controller/pmichail/x-station.json

test: send
	ssh nuc_local -t 'command; aseqdump -rp 20:0'

send_and_test: send test

receive: receive_from_device receive_from_remote clean_received convert_to_xlsx

receive_syx: receive_from_device receive_from_remote clean_received
	mv /tmp/last_received.syx last_received.syx
