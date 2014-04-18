import ConfigParser
import sys
import time
import os
import thread

if len(sys.argv) != 2:
    print 'Usage: '+sys.argv[0]+' [config_file_path]'
    sys.exit(0)

config_path = sys.argv[1] if sys.argv[1] else 'clear.ini'
config = ConfigParser.ConfigParser()

def AuthConfigFile():
    try:
        config.read(config_path)
        if config.has_section('global'):
            return True
        else:
            return False
    except:
        print 'read config file error'
        return False

def GetExpiredFiles(path, expired):
    expired_files = list()
    files = os.listdir(path)
    now = time.time()
    for f in files:
        delete_time = f.split('-')[-1]
        if now - int(delete_time) >= expired:
            expired_files.append(f)
    return expired_files

def clear():
    expired = config.get('global', 'expired_time') \
        if config.has_option('expired_time') and config.get('global', 'expired_time') \
        else 24*3600
    interval = config.get('global', 'clear_interval_time') \
        if config.has_option('clear_interval_time') and config.get('global', 'clear_interval_time') \
        else 1*3600
    trash = config.get('global', 'trash_path') \
        if config.has_option('trash_path') and config.get('global', 'trash_path') \
        else '~/.trash_box'

    while(True):
        failed_files = list()
        expired_files = GetExpiredFiles(trash, expired)
        trash = trash+'/' if trash[-1] != '/' else trash
        for f in expired_files:
            try:
                os.system('rm -rf '+trash+expired_files)
            except Exception, e:
                print trash+f, e
        time.sleep(interval)

if __name__ == '__main__':
    if(AuthConfigFile()):
        thread.start_new_thread(clear)
    else:
        print 'config file error'
