""" FTP 인터페이스
"""

import os, sys
import ftplib

from deprecated import deprecated

from .file import FileConnector, FileExplorer


# TODO : FTP PathLike로 원격지 주소 규정


class FTPConnector(FileConnector, FileExplorer):
    """ FTP 원격 서버 연결 및 탐색 클래스 입니다.
    """

    def __init__(self, **kwargs):
        self.ftp = None
        self.connect(**kwargs)
        
    def connect(self, **kwargs) -> bool:
        self.address = kwargs['address']
        self.port = int(kwargs['port'])
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.encoding = kwargs['encoding'] if 'encoding' in kwargs else 'UTF-8'

        self.ftp = ftplib.FTP()
        self.ftp.encoding = self.encoding
        self.ftp.connect(self.address, self.port)
        self.ftp.login(self.user, self.password)
        

    def close(self) -> bool:
        self.ftp.close()

    def mkdir(self, remote_path: str) -> bool:
        try:
            parent_path = os.path.dirname(remote_path)
            if not self.exists(parent_path):
                self.mkdir(parent_path)
            self.ftp.mkd(remote_path)
        except ftplib.error_perm as e:
            if not e.args[0].startswith('550'):
                result = False
            else:
                result = True
        else:
            result = True
        return result

    @deprecated(version='0.0', reason='temporary function')
    def _path_replace_(path: str) -> str:
        return path.replace('/', '\\')

    def _local_mkdir_(self, local_path: str) -> bool:
        try:
            if not os.path.exists(local_path):
                parent_path = os.path.dirname(local_path)
                if not os.path.exists(parent_path):
                    self._local_mkdir_(parent_path)
                os.mkdir(local_path)
        except:
            result = False
        else:
            result = True
        return result
            
    # TODO : 파일 업로드 결과 반환
    def _upload_file_(self, local_path: str, remote_file: str):
        with open(local_path, 'rb') as f:
            self.ftp.storbinary(f'STOR {remote_file}', f)

    # TODO : 파일 다운로드 결과 반환
    def _download_file_(self, remote_file: str, local_path: str):
        with open(local_path, 'wb') as f:
            self.ftp.retrbinary(f'RETR {remote_file}', f.write)

    def _upload_dir_(self, local_path: str, remote_path: str, mkdir: bool = True, rapper: bool = True, recall: bool = False):
        # TODO : 제거
        local_path = FTPConnector._path_replace_(local_path)
        remote_path = FTPConnector._path_replace_(remote_path)

        upload_cnt = 0
        if not recall:
            if mkdir:
                local_dir = os.path.basename(local_path)
                remote_path = os.path.join(remote_path, local_dir) if rapper else remote_path
                self.mkdir(remote_path)    
            self.explore(remote_path)
        
        for target in os.listdir(local_path):
            target_path = os.path.join(local_path, target)
            remote_target_path = os.path.join(remote_path, target)

            if os.path.isdir(target_path):
                self.mkdir(remote_target_path)
                self.explore(remote_target_path)
                self._upload_dir_(target_path, remote_target_path, recall=True)
                self.explore('..')
                upload_cnt += 1
            else:
                self._upload_file_(target_path, remote_target_path)
                upload_cnt += 1
        return upload_cnt

    def _download_dir_(self, remote_path: str, local_path: str, mkdir: bool = True, rapper: bool = True, recall: bool = False):
        download_cnt = 0
        if not recall:
            if mkdir:
                local_dir = os.path.basename(remote_path)
                local_path = os.path.join(local_path, local_dir) if rapper else local_path
                self._local_mkdir_(local_path)    
            self.explore(remote_path)
        
        for target in self.listdir(remote_path):
            target_path = '/'.join([remote_path, target])
            local_target_path = os.path.join(local_path, target)

            if self.isdir(target_path):
                self._local_mkdir_(local_target_path)
                self.explore(target_path)
                self._download_dir_(target_path, local_target_path, recall=True)
                self.explore('..')
                download_cnt += 1
            else:
                self._download_file_(target, local_target_path)
                download_cnt += 1
        return download_cnt  

    def upload_file(self, local_path: str, remote_path: str, mkdir: bool = True) -> bool:
        remote_dir, remote_file = os.path.split(remote_path)
        if not os.path.splitext(remote_file)[1]:
            remote_dir = remote_path
            remote_file = os.path.basename(local_path)
        if mkdir:
            self.mkdir(remote_dir)
        self.explore(remote_dir)
        self._upload_file_(local_path, remote_file)

    def download_file(self, remote_path: str, local_path: str, mkdir: bool = True) -> bool:
        local_dir, local_file = os.path.split(local_path)
        remote_dir, remote_file = os.path.split(remote_path)
        if not os.path.splitext(local_file)[1]:
            local_dir = local_path
            local_file = os.path.basename(remote_path)
        if mkdir:
            self._local_mkdir_(local_dir)
        self.explore(remote_dir)
        self._download_file_(remote_file, local_path)

    def upload_dir(self, local_path: str, remote_path: str, mkdir: bool = True, rapper: bool = True) -> int:
        return self._upload_dir_(local_path, remote_path, mkdir, rapper)

    def download_dir(self, remote_path: str, local_path: str, mkdir: bool = True, rapper: bool = True) -> int:
        return self._download_dir_(remote_path, local_path, mkdir, rapper)

    def current(self) -> str:
        return self.ftp.pwd()

    def explore(self, target: str):
        return self.ftp.cwd(target)

    def listdir(self, remote_path: str = '', rel_path = True) -> list:
        return [os.path.basename(p) for p in self.ftp.nlst(remote_path)] \
            if rel_path else self.ftp.nlst(remote_path)

    def exists(self, remote_path: str) -> bool:
        if remote_path in ['/', '', '\\']:
            result = True
        else:
            if remote_path.startswith('/'):
                parent_path = os.path.dirname(remote_path)
                if self.exists(parent_path):
                    result = remote_path in self.listdir(parent_path, rel_path=False)
                else:
                    result = False
            else:
                result = remote_path in self.listdir()
        return result

    def isdir(self, remote_path: str) -> bool:
        if self.exists(remote_path):
            current_dir = self.current()
            try:
                self.ftp.cwd(remote_path)
            except ftplib.error_perm as e:
                if not e.args[0].startswith('550'):
                    raise e
                else:
                    result = False
            else:
                result = True
            finally:
                self.ftp.cwd(current_dir)
        else:
            result = False
        return result

    def isfile(self, remote_path: str) -> bool:
        if self.exists(remote_path):
            result = not self.isdir(remote_path)
        else:
            result = False
        return result