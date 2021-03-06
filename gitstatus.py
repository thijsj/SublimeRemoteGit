from sublime_plugin import TextCommand, WindowCommand
from sublime import Region

from .classes.gitstatus import GitStatus
from .classes.commands import GIT_STATUS, GitCommand
from .utils import remoteCommand, logCommand
from .sublime_utils import currentLineNo, gotoLine, replaceView
from .constants import ST_VIEW_NAME

class RemoteGitSt(TextCommand):
    def run(self, edit):
        logCommand(self.view, self.__class__.__name__)
        result = remoteCommand(self.view, GitCommand(GIT_STATUS))
        replaceView(self.view, edit, result)

        gitStatus = GitStatus.fromMessage(self.view.substr(Region(0, self.view.size())))
        toLine = getattr(self.view, "laststatuslineno", gitStatus.firstlineno())
        if toLine:
            gotoLine(self.view, gitStatus.closestLineNo(toLine))

class RemoteGitStatusChangeLine(TextCommand):
    def run(self, edit, up=False):
        if self.view.name() != ST_VIEW_NAME:
            return
        gitStatus = GitStatus.fromMessage(self.view.substr(Region(0, self.view.size())))
        gotoLine(self.view, gitStatus.nextlineno(currentLineNo(self.view), up))
        self.view.laststatuslineno = currentLineNo(self.view)

class RemoteGitStatusHelp(WindowCommand):
    def run(self):
        items = [
            'a (git add or git rm if deleted)',
            'A (git add all)',
            'r (git reset HEAD)',
            'c (git checkout)',
            'm (git commit)',
            'M (git add all, then commit)',
            'p (git push)',
            'd (git diff)',
            'l (git log)'
        ]
        self.window.show_quick_panel(items, lambda x: None)
