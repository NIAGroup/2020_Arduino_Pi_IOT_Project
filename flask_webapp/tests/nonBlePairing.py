import pexpect, time, sys

addr = "00:14:03:06:12:84"
passkey = "1234"

def pairDevice(addr, passkey)
    analyzer = pexpect.spawn(command='bluetoothctl',encoding='utf-8')
    analyzer.expect("# ")
    print(analyzer.before)

    for cmd in ['scan on','scan off',f"pair {addr}", passkey, 'exit']:
        print(f"Trying {cmd}...")
        analyzer.sendline(cmd)
        print(analyzer.before)
        stop_time = time.time() + 10
        while time.time() < stop_time:
            time.sleep(1)
        analyzer.expect('# ')
