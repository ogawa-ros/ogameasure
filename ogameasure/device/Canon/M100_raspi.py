from __future__ import print_function
import logging
import os
import subprocess
import sys
import gphoto2 as gp
import time
import socket

#time1 = time.ctime()
#time2 = time.strptime(time1)
#time3 = time.strftime('%Y%m%d_%H.%M.%S', time2)
timestr = time.strftime('%Y%m%d_%H.%M.%S', time.strptime(time.ctime()))

#savedir_pre = '/home/1.85m/evaluation/optical_pointing/test/fig/'

HOST = '192.168.100.12'
PORT = 50000

#def capture(savedir, imagename):
#f = open('%s%s'%(savedir, imagename), 'w')
#f.write('test')
#f.close()

class m100(object):
    def capture(self,savepath):
        #savedir = './picture/'+timestr+'.JPG'
        savedir = savepath
        logging.basicConfig(format='%(levelname)s: %(name)s: %(massage)s', level=logging.WARNING)
        gp.check_result(gp.use_python_logging())
        camera = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_init(camera))
        print('Capturing image')
        file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))
        #print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        #target = os.path.join(savedir, imagename)
        #print('Copying image to', target)
        camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
        #gp.check_result(gp.gp_file_save(camera_file, target))
        #timestr = time.strftime('%Y%m%d_%H.%M.%S', time.strptime(time.ctime()))
        gp.check_result(gp.gp_file_save(camera_file, savedir))
        #gp.check_result(gp.gp_file_save(camera_file, './picture/'+timestr+'.jpg'))
        #subprocess.call(['xdg-open', target])
        gp.check_result(gp.gp_camera_exit(camera))
        return 'Shooting completed'
        #return 0

'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print('Server is listening for connections')

While True:
    conn, addr = s.accept()
    print('connected')
    capture()
    bytes = open('./picture/'+timestr+'.JPG', encoding='utf8', errors='ignore').read()
    print(len(bytes), 'bytes')
    bytes += '¥n'
    _file = open('./picture/'+timestr+'.JPG', 'wb')
    _file.write(bytes)
    _file.close()
    conn.send(bytes)
'''
