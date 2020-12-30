"""
    Flirc remote sender
"""
import sys
import subprocess

VOL_UP = '0,8980,4429,580,532,557,528,557,532,553,1628,576,527,558,527,558,505,580,1646,531,1672,554,1645,558,1642,558,505,580,1619,584,1619,579,1646,557,527,558,527,558,1645,558,1615,584,531,553,532,553,531,558,1620,579,532,557,1641,558,532,553,532,532,1645,580,1619,585,1619,584,501,584,1641,584'
VOL_DOWN = '0,9032,4376,633,448,640,449,636,448,636,1566,636,448,615,470,640,448,636,1561,641,1562,640,1562,640,1574,628,444,640,1561,641,1561,637,1562,641,488,597,448,641,1562,637,1562,641,448,637,1562,641,444,640,449,636,448,641,1563,640,444,641,444,641,1562,640,444,641,1562,641,1558,640,1563,641'
FLIRC_UTIL_PATH = r'C:\Program Files (x86)\Flirc\flirc_util.exe'
FLIRC_IK = '23000'  # interkey delay
FLIRC_REPEAT = 2
FLIRC_CMD = '%s sendir --ik=%s --repeat=%s --pattern=' % (FLIRC_UTIL_PATH, FLIRC_IK, FLIRC_REPEAT)


def main():
    """ MAIN """
    helptext = "Invalid command - use up or down"
    if len(sys.argv) < 2:
        print(helptext)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'up':
        send_command(VOL_UP)
    elif cmd == 'down':
        send_command(VOL_DOWN)
    else:
        print(helptext)
        sys.exit(1)


def send_command(cmd):
    """ Send the IR command """
    os_cmd = FLIRC_CMD + cmd
    print('os_cmd: %s' % os_cmd)
    subprocess.run(os_cmd.split(' '), check=True)


if __name__ == "__main__":
    main()
