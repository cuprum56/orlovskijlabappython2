import os
import logging
import datetime
import shutil

class Shell:
    def __init__(self):
        self.nowDir = os.getcwd()
        self.startLogging()


    def startLogging(self):
        logging.basicConfig(
            filename='shel.log',
            level=logging.INFO,
            format='[%(asctime)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
            
        )


    def logComand(self, command, isError=False, errorText=''):
        logTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logText = f'[{logTime} {command}]'

        if isError:
            logText+= f'\n[{logTime}] ERROR: {errorText}'

        with open('C:/prog/mai/labs/python/shell/shel.log', mode='a', encoding='utf-8') as f:
            f.write(logText + '\n')


    def ls(self, path=None, lFlag=False):
        try:
            targetPath = path if path else self.nowDir
            targetPath = self.getAbsolutePath(targetPath)

            if not os.path.exists(targetPath):
                errorText = 'No such file or directory'
                print(f'{errorText} {path}')
                self.logComand(f"ls {path if path else ''} {'-l' if lFlag else ''}",
                True, errorText)
                return
            
            items = os.listdir(targetPath)
            if lFlag:
                print('-' * 100)
                print(f'{'Name':<30} {'Size':<10} {'Modified':<20} Permissions')
                print('-' * 100)
                
                for item in items:
                    itemPath = os.path.join(targetPath, item)
                    itemStat = os.stat(itemPath)
                    itemSize = itemStat.st_size
                    itemModified = datetime.datetime.fromtimestamp(itemStat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    itemPermission = oct(itemStat.st_mode)[-3:]
                    itemType = 'd' if os.path.isdir(itemPath) else '-'
                    print(f"{item:<30} {itemSize:<10} {itemModified:<20} {itemType}{itemPermission}")
            
            else:
                for item in items:
                    print(item)

            self.logComand(f'ls{f' {path}' if path else ''} {'-l' if lFlag else ''}')

        except Exception as e:
            errorText = str(e)
            print('ls: ', errorText)
            self.logComand(f'ls{f' {path}' if path else ''} {'-l' if lFlag else ''}', True, errorText)


    def cd(self, path):
        try:
            if path == '..':
                newPath = os.path.dirname(self.nowDir)
            elif path == '~':
                newPath = os.path.expanduser('~')
            else:
                newPath = self.getAbsolutePath(path)

            if not os.path.exists(newPath):
                errorText = 'No such directory'
                print(f"{errorText}: {path}")
                self.logComand(f'cd {path}', True, errorText)
                return
        
            if not os.path.isdir(newPath):
                errorText = 'Path is not a directory'
                print(f'{errorText}: {path}')
                self.logComand(f'cd {path}', True, errorText)
                return
        
            self.nowDir = newPath
            os.chdir(newPath)
            self.logComand(f'cd {path}')
        
        except Exception as e:
            errorText = str(e)
            print(f"cd: {errorText}")
            self.logComand(f"cd {path}", True, errorText)

    
    def cat(self, path):
        try:
            absPath = self.getAbsolutePath(path)

            if not os.path.exists(absPath):
                errorText = 'No such file'
                print(f'{errorText}: {path}')
                self.logComand(f'cat {path}', True, errorText)
                return

            if os.path.isdir(absPath):
                errorText = 'Is a directory'
                print(f'{errorText}: {path}')
                self.logComand(f'cat {path}', True, errorText)
                return
            
            with open(absPath, mode='r', encoding='utf-8') as f:
                fileContent = f.read()
                print(fileContent)

            self.logComand(f'cat {path}')

        except Exception as e:
            errorText = str(e)
            print(f'cat: ', {errorText})
            self.logComand(f'cat {path}', True, errorText)

    
    def cp(self, source, target, rFlag=False):
        try:
            srcAbsPath = self.getAbsolutePath(source)
            trgAbsPath = self.getAbsolutePath(target)
            if not os.path.exists(srcAbsPath):
                errorText = 'Source does not exist'
                print(f'{errorText}:  {source}')
                self.logComand(f'cp {source} {target}{' -r' if rFlag else ''}', True, errorText)
                return
            
            if os.path.isdir(srcAbsPath) and rFlag:
                shutil.copytree(srcAbsPath, trgAbsPath)
            else:
                shutil.copy2(srcAbsPath, trgAbsPath)
            
            self.logComand(f'cp {source} {target}{' -r' if rFlag else ''}')

        except Exception as e:
            errorText = str(e)
            print(f'cp: {errorText}')
            self.logComand(f'cp {source} {target}{' -r' if rFlag else ''}', True, errorText)

    
    def mv(self, source, target):
        try:
            srcAbsPath = self.getAbsolutePath(source)
            trgAbsPath = self.getAbsolutePath(target)
            if not os.path.exists(srcAbsPath):
                errorText = 'Source does not exist'
                print(f'{errorText}:  {source}')
                self.logComand(f'mv {source} {target}', True, errorText)
                return

            shutil.move(srcAbsPath, trgAbsPath)
            self.logComand(f'mv {source} {target}')
        
        except Exception as e:
            errorText = str(e)
            print(f'mv: {errorText}')
            self.logComand(f'mv {source} {target}', True, errorText)

        
    def rm(self, path, rFlag=False):
        try:
            absPath = self.getAbsolutePath(path)

            if absPath in ['/', '\\'] or absPath == os.path.dirname(self.nowDir):
                errorText = 'Cant remove parent or root directory'
                print(errorText)
                self.logComand(f'rm {path}{' -r' if rFlag else ''}', True, errorText)
                return
            
            if not os.path.exists(absPath):
                errorText = 'No such file or directory'
                print(f'{errorText}: {path}')
                self.logComand(f'rm {path}{' -r' if rFlag else ''}', True, errorText)
                return
            
            if os.path.isdir(absPath):
                if not rFlag:
                    errorText = 'Cant remove directory without -r flag'
                    print(f'{errorText}: {path}')
                    self.logComand(f'rm {path}{' -r' if rFlag else ''}', True, errorText)
                    return
                
                confrim = input(f'Remove directory {path}? (y/n)')
                if confrim.lower() != 'y':
                    return
                
                shutil.rmtree(absPath)

            else:
                os.remove(absPath)
            self.logComand(f'rm {path}{' -r' if rFlag else ''}')
        
        except Exception as e:
            errorText = str(e)
            print(f'rm: {errorText}')
            self.logComand(f'rm {path}{' -r' if rFlag else ''}', True, errorText)


    def getAbsolutePath(self, path):
        if os.path.isabs(path):
            return path
        return os.path.join(self.nowDir, path)
    
    def run(self):
        print('Type "exit" to leave')
        while True:
            try:
                command = input(f'\n{self.nowDir}> ').strip()
                if not command:
                    continue

                if command.lower() == 'exit':
                 break

                parts = command.split()
                func = parts[0]
                args = parts[1:]

                if func == 'ls':
                    lFlag = '-l' in args
                    argsPath = [arg for arg in args if arg != '-l']
                    path = argsPath[0] if argsPath else None
                    self.ls(path, lFlag)

                elif func == 'cd':
                    if not args:
                        print('add directory to args')
                        continue
                    self.cd(args[0])

                elif func == 'cat':
                    if not args:
                        print('add file to args')
                        continue
                    self.cat(args[0])

                elif func == 'cp':
                    fileArgs = [arg for arg in args if arg != '-r']
                    if len(fileArgs) < 2:
                        print('add 2 arguments to comand: source and target directory')
                        continue
                    rFlag = '-r' in args
                    self.cp(fileArgs[0], fileArgs[1], rFlag)
            
                elif func == 'mv':
                    if len(args) < 2:
                        print('add 2 arguments to comand: source and target directory')
                        continue
                    self.mv(args[0], args[1])

                elif func == 'rm':
                    targetArgs = [arg for arg in args if arg != '-r']
                    if not targetArgs:
                        print('add file or directory to args')
                        continue
                    rFlag = '-r' in args
                    self.rm(targetArgs[0], rFlag)
                
                else:
                    print('Unknow command: ', func)
            except Exception as e:
                errorText = str(e)
                print('Error on run: ', e)

if __name__ == '__main__':
    shell = Shell()
    shell.run()
