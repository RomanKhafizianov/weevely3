from core.vectors import Os, Vector
from core.module import Module
from core import messages
import random


class Info(Module):

    """Collect system information.

    Usage:
      system_info
      system_info [--info=info]

    """

    def initialize(self):

        self._register_infos(
            {
                'name': 'System information',
                'description': __doc__,
                'author': [
                    'Emilio Pinna'
                ],
                'license': 'GPLv3'
            }
        )

        self._register_arguments(
            options={
                'info': 'all'
            })

        self._register_vectors(
            [
            Vector("print(@$_SERVER['DOCUMENT_ROOT']);", 'document_root'),
            Vector("$u=@posix_getpwuid(@posix_geteuid());if($u){$u=$u['name'];} else{$u=getenv('username');} print($u);", 'whoami'),
            Vector("print(@gethostname());", 'hostname'),
            Vector("@print(getcwd());", 'cwd'),
            Vector("$v=@ini_get('open_basedir'); if($v) print($v);", 'open_basedir'),
            Vector("(@ini_get('safe_mode') && print(1)) || print(0);", 'safe_mode'),
            Vector("print(@$_SERVER['SCRIPT_NAME']);", 'script'),
            Vector("print(@php_uname());", 'uname'),
            Vector("print(PHP_OS);", 'os'),
            Vector("print(@$_SERVER['REMOTE_ADDR']);", 'client_ip'),
            Vector('print(@ini_get("max_execution_time"));', 'max_execution_time'),
            Vector('print(@$_SERVER["PHP_SELF"]);', 'php_self'),
            Vector('@print(DIRECTORY_SEPARATOR);', 'dir_sep'),
            Vector("$v=''; if(function_exists( 'phpversion' )) { $v=phpversion(); } elseif(defined('PHP_VERSION')) { $v=PHP_VERSION; } elseif(defined('PHP_VERSION_ID')) { $v=PHP_VERSION_ID; } print($v);", 'php_version')
            ]
        )

    def run(self, args):

        results = {}
        
        for vector in self.vectors:
            
            if args['info'] in ('all', vector.name):

                results[vector.name] = vector.run()

                # Store "static" results used by other modules
                if vector.name in ('whoami', 'hostname', 'dir_sep'):
                    self._store_result(vector.name, results[vector.name])

        return results
