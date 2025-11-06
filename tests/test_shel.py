import pytest
import os
import tempfile
import shutil
from main import Shell

class TestShell:
    @pytest.fixture
    def shell(self):
        return Shell()
    
    @pytest.fixture
    def test_dir(self):
        original_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file = os.path.join(tmp_dir, 'test1.txt')
            test_dir_path = os.path.join(tmp_dir, 'test_dir')
            
            with open(test_file, 'w') as f:
                f.write("test content")
            
            os.makedirs(test_dir_path)
            with open(os.path.join(test_dir_path, 'inner.txt'), 'w') as f:
                f.write("inner content")
            
            yield tmp_dir
            
            os.chdir(original_dir)

    def test_shell_init(self, shell):
        assert shell.nowDir == os.getcwd()

    def test_getAbsolutePath(self, shell):
        shell.nowDir = 'C:\\tmp'
        assert shell.getAbsolutePath('test') == 'C:\\tmp\\test'
        assert shell.getAbsolutePath('C:\\absolute\\path') == 'C:\\absolute\\path'

    def test_ls_basic(self, shell, test_dir):
        shell.nowDir = test_dir
        shell.ls()

    def test_ls_detailed(self, shell, test_dir):
        shell.nowDir = test_dir
        shell.ls(lFlag=True)

    def test_ls_with_path(self, shell, test_dir):
        shell.ls(path=test_dir)

    def test_ls_nonexistent(self, shell):
        shell.ls(path='C:\\nonexistent')

    def test_cd_absolute(self, shell, test_dir):
        original_dir = shell.nowDir
        shell.cd(test_dir)
        assert shell.nowDir == test_dir
        shell.cd(original_dir)

    def test_cd_relative(self, shell, test_dir):
        original_dir = shell.nowDir
        shell.nowDir = test_dir
        shell.cd('test_dir')
        assert shell.nowDir == os.path.join(test_dir, 'test_dir')
        shell.cd(original_dir)

    def test_cd_parent(self, shell, test_dir):
        original_dir = shell.nowDir
        subdir = os.path.join(test_dir, 'test_dir')
        shell.nowDir = subdir
        shell.cd('..')
        assert shell.nowDir == test_dir
        shell.cd(original_dir)

    def test_cd_nonexistent(self, shell):
        original_dir = shell.nowDir
        shell.cd('nonexistent_dir')
        assert shell.nowDir == original_dir

    def test_cat_file(self, shell, test_dir):
        shell.nowDir = test_dir
        shell.cat('test1.txt')

    def test_cat_directory(self, shell, test_dir):
        shell.nowDir = test_dir
        shell.cat('test_dir')

    def test_cat_nonexistent(self, shell):
        shell.cat('nonexistent.txt')

    def test_cp_file(self, shell, test_dir):
        shell.nowDir = test_dir
        shell.cp('test1.txt', 'test1_copy.txt')
        assert os.path.exists(os.path.join(test_dir, 'test1_copy.txt'))

    def test_cp_directory_without_r(self, shell, test_dir):
        shell.nowDir = test_dir
        shell.cp('test_dir', 'test_dir_copy')

    def test_cp_directory_with_r(self, shell, test_dir):
        shell.nowDir = test_dir
        shell.cp('test_dir', 'test_dir_copy', rFlag=True)
        assert os.path.exists(os.path.join(test_dir, 'test_dir_copy'))

    def test_mv_file(self, shell, test_dir):
        shell.nowDir = test_dir
        shell.mv('test1.txt', 'test1_moved.txt')
        assert not os.path.exists(os.path.join(test_dir, 'test1.txt'))
        assert os.path.exists(os.path.join(test_dir, 'test1_moved.txt'))

    def test_mv_directory(self, shell, test_dir):
        shell.nowDir = test_dir
        shell.mv('test_dir', 'test_dir_moved')
        assert not os.path.exists(os.path.join(test_dir, 'test_dir'))
        assert os.path.exists(os.path.join(test_dir, 'test_dir_moved'))

    def test_rm_file(self, shell, test_dir):
        shell.nowDir = test_dir
        shell.rm('test1.txt')
        assert not os.path.exists(os.path.join(test_dir, 'test1.txt'))

    def test_rm_directory_without_r(self, shell, test_dir):
        shell.nowDir = test_dir
        shell.rm('test_dir')

    def test_rm_directory_with_r(self, shell, test_dir, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        shell.nowDir = test_dir
        shell.rm('test_dir', rFlag=True)
        assert not os.path.exists(os.path.join(test_dir, 'test_dir'))

    def test_rm_protected(self, shell):
        shell.rm('C:\\', rFlag=True)

    def test_log_file_created(self, shell):
        log_path = 'C:/prog/mai/labs/python/shell/shel.log'
        assert os.path.exists(log_path)