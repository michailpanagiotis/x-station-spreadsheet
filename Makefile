convert_to_syx:
	./convert.py syx $(FILE) --output /tmp/last_sent.syx

convert_to_xlsx:
	./convert.py xlsx /tmp/last_received.syx --output last_received.xlsx

send_to_remote:
	scp /tmp/last_sent.syx nuc_local:/tmp/last_sent.syx

receive_from_remote:
	scp nuc_local:/tmp/last_received.syx /tmp/last_received.syx

send_to_device:
	ssh nuc_local -t 'command; amidi -s /tmp/last_sent.syx -p hw:1,0,0'

receive_from_device: clean_received
	ssh nuc_local -t 'command; amidi -r /tmp/last_received.syx -p hw:1,0,0'

send: convert_to_syx send_to_remote send_to_device

test: send
	ssh nuc_local -t 'command; aseqdump -rp 20:0'

send_and_test: send test

clean_received:
	ssh nuc_local -t 'command; rm -f /tmp/last_received.syx'

receive: receive_from_device receive_from_remote clean_received convert_to_xlsx
