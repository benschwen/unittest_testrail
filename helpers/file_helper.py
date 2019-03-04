from pathlib import Path

class FileHelper:
    @staticmethod
    def resolveAgnosticPath(relativeDirPath, fileName):
        dir = Path(relativeDirPath)
        return dir / fileName