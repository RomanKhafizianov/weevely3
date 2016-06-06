from core.channels.channels import get_channel
from testsuite.config import script_folder, script_folder_url
from core.commons import randstr
from unittest import TestCase
from generate import generate, save_generated
import hashlib
import os
import shutil
import logging

class BaseDefaultChannel(TestCase):
    
    password = randstr(10)
    password_hash = hashlib.md5(password).hexdigest()
    filename = '%s_%s_%s.php'% (__name__, password_hash[:3], password_hash[3:6])
    url = os.path.join(script_folder_url, filename)
    path = os.path.join(script_folder, filename)
   
    @classmethod
    def setUpClass(cls):
        obfuscated = generate(cls.password)
        save_generated(obfuscated, cls.path)


    @classmethod
    def tearDownClass(cls):
        os.remove(cls.path)
       
    def setUp(self):
        self.channel = get_channel(self.url, self.password)
        
    
    def _multiple_requests(self, size, howmany):
        
        for i in range(howmany):
            payload = randstr(size)
            self.assertEqual(self.channel.send('echo("%s");' % payload), payload)