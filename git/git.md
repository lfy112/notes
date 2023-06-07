# git学习

`git init`初始化git仓库

`git add <file name>`将文件放到暂存区

`git commit -m 'description'`提交修改和对应的描述

`git status`可以查看当前哪些文件没有提交，哪些文件没有追踪到

`git diff`可以查看文件修改的内容（相较于暂存区）

`git log`查看提交记录，加上`--pretty=oneline`参数可以更简洁

`git reset`回退版本`git reset --hard HEAD^`回退到上一个版本，`git reset --hard xxxx`切换到指定的版本，xxxx表示`git log`看到的sha1值，`git reflog`可以回到未来

## 工作区与暂存区

工作区是能看见的文件和目录，暂存区是等待提交的文件

step 1: `git add`放到暂存区；step 2: `git commit`提交修改

> 注意，修改后一定要先add到暂存区才能，不add的修改不会被提交

`git diff HEAD --file name`可以查看工作区和版本库里面最新版本的区别（不加HEAD就只能看见和暂存区的区别）

## 恢复操作

如果还没有进行add操作：`git checkout -- file name`（--后面有空格）撤销工作区的该文件，如果add过，从暂存区恢复，否则从版本库恢复，回到最近一次`git commit`或`git add`时的状态

如果已经add之后：`git reset HEAD <file>`可以把暂存区的修改撤销，重新放回工作区

## 删除文件

在本地删除文件后，`git status`会知道删除了这个文件，使用`git rm file name`和`git commit`删除git中的文件

如果删错了文件，可以使用`git checkout -- file name`从暂存区或者版本库进行恢复

## 分支

创建分支：`git checkout -b name`创建并切换到一个叫name的分支

使用`git branch`查看当前分支

使用`git checkout name`或者`git switch name`切换分支

使用`git merge name`合并分支

使用`git branch -d name`删除分支

如果merge时候发生了冲突，需要手动修改冲突文件，重新add、commit，可以使用`git log --graph`查看

禁用fast forward模式，在merge时生成一个新的commit，使用`git merge --no-ff`
