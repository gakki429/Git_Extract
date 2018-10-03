# Git Extract

提取远程git泄露或本地git的工具

|Author|gakki429|
|---|---
|Date|2018-9-9

### 目的
    现有的git恢复工具都依赖于git命令，没有将各版本的文件恢复
    存在需要手动提取恢复objects的情况，对于部分文件的考虑存在欠缺
    如logs/HEAD, refs/stash, info/packs

### 特点
    支持远程.git泄露的提取，也支持对本地.git路径下文件的提取
    不使用git命令，完全使用python完成对git文件的解析
    提取历史各版本的文件，并使用(sha1[:6] + filename)命名文件，以做区分

    恢复项现包括:
        index 缓存
        HEAD 现分支的恢复
        logs/HEAD 日志
        refs/stash 工作进度保存
        refs/heads/master master恢复
        info/packs packs文件提取恢复
    可能重复但仍做恢复的项:
        packed-refs
        refs/remotes/origin/HEAD
        ORIG_HEAD
        FETCH_HEAD
    其他信息项:
        info/exclude
        COMMIT_EDITMSG
    注:
        不是所有的恢复项都一定存在

### 依赖
    只使用python原生库

### 使用
    python git_extract.py http://example.com/.git/ 一个存在.git泄露的网站
    python git_extract.py example/.git/ 一个本地的.git路径

### 更新
    2018-10-3:
        增加对windows字体颜色输出的支持，并同步默认背景色
        linux中背景色也修改为与默认同步

### Todo
    解析其他版本的git文件格式，目前支持version 2
    pack文件的ofs_delta，ref_delta类型文件的重建

### 参考
* [pack文件格式](https://git-scm.com/docs/pack-format) 
* [index文件格式](https://git-scm.com/docs/index-format) 
