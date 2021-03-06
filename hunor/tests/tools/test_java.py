from unittest import TestCase
from unittest.mock import MagicMock

import os
import subprocess

from hunor.tools.java import JDK, TIMEOUT as JAVA_TIMEOUT
from hunor.tools.java_factory import Java


class TestJDK(TestCase):

    def test_check_javac_no_java_home(self):
        del os.environ['JAVA_HOME']

        with self.assertRaises(SystemExit):
            JDK('')

    def test_wrong_java_home(self):
        WRONG_JAVA_HOME = 'wrong_java_home'

        os.environ['JAVA_HOME'] = WRONG_JAVA_HOME

        subprocess.check_call = MagicMock(side_effect=OSError)

        with self.assertRaises(SystemExit):
            JDK('')

        subprocess.check_call.assert_called_once_with(
            [os.path.join(WRONG_JAVA_HOME, 'bin', 'javac'), '-version'],
            stdout=subprocess.DEVNULL,
            timeout=10,
            cwd=None,
            stderr=subprocess.DEVNULL
        )

    def test_java_path(self):
        JAVA_HOME = 'java_home'

        subprocess.check_call = MagicMock()

        jdk = JDK(JAVA_HOME)

        subprocess.check_call.assert_called_once_with(
            [os.path.join(JAVA_HOME, 'bin', 'javac'), '-version'],
            stdout=subprocess.DEVNULL,
            timeout=10,
            cwd=None,
            stderr=subprocess.DEVNULL
        )

        self.assertEqual(os.path.join(JAVA_HOME, 'jre', 'bin', 'java'),
                         jdk.java)
        self.assertEqual(os.path.join(JAVA_HOME, 'bin', 'javac'), jdk.javac)

    def test_javac(self):
        JAVA_HOME = 'java_home'

        jdk = JDK(JAVA_HOME)

        subprocess.check_call = MagicMock()

        self.assertTrue(jdk.run_javac('file.java', 10, None))

        subprocess.check_call.assert_called_once_with(
            [os.path.join(JAVA_HOME, 'bin', 'javac'), 'file.java'],
            stdout=subprocess.DEVNULL,
            timeout=10,
            cwd=None,
            stderr=subprocess.DEVNULL
        )

    def test_javac_with_args(self):
        JAVA_HOME = 'java_home'

        jdk = JDK(JAVA_HOME)

        subprocess.check_call = MagicMock()

        self.assertTrue(jdk.run_javac('file.java', 10, None, '-a', 'b'))

        subprocess.check_call.assert_called_once_with(
            [os.path.join(JAVA_HOME, 'bin', 'javac'), '-a', 'b', 'file.java'],
            stdout=subprocess.DEVNULL,
            timeout=10,
            cwd=None,
            stderr=subprocess.DEVNULL
        )

    def test_javac_timeout(self):
        JAVA_HOME = 'java_home'

        jdk = JDK(JAVA_HOME)

        subprocess.check_call = MagicMock(
            side_effect=subprocess.TimeoutExpired('', 0))

        self.assertFalse(jdk.run_javac('file.java', 10, None))

    def test_javac_process_error(self):
        JAVA_HOME = 'java_home'

        jdk = JDK(JAVA_HOME)

        subprocess.check_call = MagicMock(
            side_effect=subprocess.CalledProcessError(-1, ''))

        self.assertFalse(jdk.run_javac('file.java', 10, None))


class TestJava(TestCase):

    def setUp(self):
        self.JAVA_HOME = 'java_home'

    def test_exec_process_error(self):
        subprocess.check_output = MagicMock(
            side_effect=subprocess.CalledProcessError(-1, ''))

        with self.assertRaises(subprocess.CalledProcessError):
            Java._exec('java', cwd=None, env=None, timeout=None)

        subprocess.check_output.assert_called_once_with(
            ['java'], cwd=None, env=None, timeout=None,
            stderr=subprocess.STDOUT)

    def test_exec_timeout_expired(self):
        subprocess.check_output = MagicMock(
            side_effect=subprocess.TimeoutExpired('', 0))

        with self.assertRaises(subprocess.TimeoutExpired):
            Java._exec('java', cwd=None, env=None, timeout=None)

        subprocess.check_output.assert_called_once_with(
            ['java'], cwd=None, env=None, timeout=None,
            stderr=subprocess.STDOUT)

    def test_exec_file_not_found_error(self):
        subprocess.check_output = MagicMock(
            side_effect=FileNotFoundError())

        with self.assertRaises(FileNotFoundError):
            Java._exec('java', cwd=None, env=None, timeout=None)

        subprocess.check_output.assert_called_once_with(
            ['java'], cwd=None, env=None, timeout=None,
            stderr=subprocess.STDOUT)

    def test_java_property(self):
        java = Java(self.JAVA_HOME)
        java._check = MagicMock()

        self.assertEqual(os.path.join(self.JAVA_HOME, 'jre', 'bin', 'java'),
                         java.java)

    def test_exec_java(self):
        subprocess.check_output = MagicMock(return_value=None)
        java = Java(self.JAVA_HOME)

        subprocess.check_output = MagicMock(return_value='OK')

        self.assertEqual('OK', java.exec_java('a', None, 1, 'b', 'c'))
        subprocess.check_output.assert_called_once_with(
            [os.path.join(self.JAVA_HOME, 'jre', 'bin', 'java'), 'b', 'c'],
            cwd='a', env=None, timeout=1, stderr=subprocess.STDOUT)

    def test_run(self):
        subprocess.check_output = MagicMock(return_value=None)
        java = Java(self.JAVA_HOME)

        subprocess.check_output = MagicMock(return_value='OK')

        self.assertEqual('OK', java.run('a', 'b', 'c'))
        subprocess.check_output.assert_called_once_with(
            [java.java, 'a', 'b', 'c'], cwd=None, env=java.get_env(),
            timeout=JAVA_TIMEOUT, stderr=subprocess.STDOUT
        )

    def test_version_java(self):
        subprocess.check_output = MagicMock(return_value=None)
        java = Java(self.JAVA_HOME)

        subprocess.check_output = MagicMock(return_value='java 1.8.0_202')

        self.assertEqual('java 1.8.0_202', java._version_java())
        subprocess.check_output.assert_called_once_with(
            [java.java, '-version'], cwd=None, env=java.get_env(),
            timeout=JAVA_TIMEOUT, stderr=subprocess.STDOUT
        )

    def test_get_env(self):
        subprocess.check_output = MagicMock(return_value=None)
        java = Java(self.JAVA_HOME)

        env = java.get_env()

        self.assertEqual(java.java_home, env['JAVA_HOME'])
        self.assertTrue(os.environ['PATH'] in env['PATH'])
        self.assertTrue(os.path.join(java.java_home, 'bin') in env['PATH'])

    def test_get_env_with_variables(self):
        subprocess.check_output = MagicMock(return_value=None)
        java = Java(self.JAVA_HOME)

        env = java.get_env({'A_B_C_D_583': 'OK'})

        self.assertEqual(java.java_home, env['JAVA_HOME'])
        self.assertTrue(os.environ['PATH'] in env['PATH'])
        self.assertTrue(os.path.join(java.java_home, 'bin') in env['PATH'])
        self.assertEqual('OK', env['A_B_C_D_583'])

    def test_check_java_home_none(self):
        self._del_java_home_env()

        with self.assertRaises(SystemExit):
            Java()

    def test_check_java_home_arg(self):
        subprocess.check_output = MagicMock(return_value=None)
        self._del_java_home_env()

        java = Java(self.JAVA_HOME)

        self.assertTrue(java.java.startswith(self.JAVA_HOME))
        self.assertTrue(java.javac.startswith(self.JAVA_HOME))

        subprocess.check_output.assert_any_call(
            [java.java, '-version'], cwd=None, env=java.get_env(),
            timeout=JAVA_TIMEOUT, stderr=subprocess.STDOUT
        )

        subprocess.check_output.assert_any_call(
            [java.javac, '-version'], cwd=None, env=java.get_env(),
            timeout=JAVA_TIMEOUT, stderr=subprocess.STDOUT
        )

    def test_set_home_in_env(self):
        subprocess.check_output = MagicMock(return_value=None)
        os.environ['JAVA_HOME'] = self.JAVA_HOME

        java = Java()

        self.assertTrue(java.java.startswith(self.JAVA_HOME))
        self.assertTrue(java.javac.startswith(self.JAVA_HOME))

        subprocess.check_output.assert_any_call(
            [java.java, '-version'], cwd=None, env=java.get_env(),
            timeout=JAVA_TIMEOUT, stderr=subprocess.STDOUT
        )

        subprocess.check_output.assert_any_call(
            [java.javac, '-version'], cwd=None, env=java.get_env(),
            timeout=JAVA_TIMEOUT, stderr=subprocess.STDOUT
        )

    def test_check_wrong_java_home(self):
        subprocess.check_output = MagicMock(side_effect=FileNotFoundError())

        with self.assertRaises(SystemExit):
            Java('wrong_java_home')

    def test_javac_property(self):
        subprocess.check_output = MagicMock(return_value=None)
        java = Java(self.JAVA_HOME)

        self.assertEqual(os.path.join(self.JAVA_HOME, 'bin', 'javac'),
                         java.javac)

    def test_run_javac(self):
        subprocess.check_output = MagicMock(return_value=None)
        java = Java(self.JAVA_HOME)

        subprocess.check_output = MagicMock(return_value='OK')

        self.assertEqual('OK', java.run_javac('file.java', 'b', 'c'))
        subprocess.check_output.assert_called_once_with(
            [java.javac, 'file.java', 'b', 'c'], cwd=None, env=java.get_env(),
            timeout=JAVA_TIMEOUT, stderr=subprocess.STDOUT
        )

    def test_exec_javac(self):
        subprocess.check_output = MagicMock(return_value=None)
        java = Java(self.JAVA_HOME)

        subprocess.check_output = MagicMock(return_value='OK')

        self.assertEqual('OK', java.exec_javac('file.java', 'src_dir', None,
                                               1, 'b'))
        subprocess.check_output.assert_called_once_with(
            [os.path.join(self.JAVA_HOME, 'bin', 'javac'), 'file.java', 'b'],
            cwd='src_dir', env=None, timeout=1, stderr=subprocess.STDOUT)

    def test_version_javac(self):
        subprocess.check_output = MagicMock(return_value=None)
        java = Java(self.JAVA_HOME)

        subprocess.check_output = MagicMock(return_value='javac 1.8.0_202')

        self.assertEqual('javac 1.8.0_202', java._version_javac())
        subprocess.check_output.assert_called_once_with(
            [java.javac, '-version'], cwd=None, env=java.get_env(),
            timeout=JAVA_TIMEOUT, stderr=subprocess.STDOUT
        )

    def _del_java_home_env(self):
        if 'JAVA_HOME' in os.environ:
            del os.environ['JAVA_HOME']