# Git Extract

提取远程 git 泄露或本地 git 的工具

### 目的

现有的 git 恢复工具都依赖于 git 命令，没有将各版本的文件恢复，存在需要手动提取恢复 objects 的情况，对于部分文件的考虑存在欠缺，如 logs/HEAD, refs/stash, info/packs

### 特点

支持远程 .git 泄露的提取，也支持对本地 .git 路径下文件的提取；不使用 git 命令，完全使用 python 完成对 git 文件的解析；提取历史各版本的文件，并使用 filename.sha1[:6] 格式命名文件，以做区分

- 恢复项现包括：

    - index 缓存
    - HEAD 现分支的恢复
    - logs/HEAD 日志
    - refs/stash 工作进度保存
    - refs/heads/master master 恢复
    - info/packs packs 文件提取恢复
    - refs/wip/index/refs/heads/master magit wip 模式 (PlaidCTF 2020)
    - refs/wip/wtree/refs/heads/master

- 可能重复但仍做恢复的项：

    - packed-refs
    - refs/remotes/origin/HEAD
    - ORIG_HEAD
    - FETCH_HEAD

- 其他信息项：

    - config
    - description
    - info/exclude
    - COMMIT_EDITMSG

- 注意：

    不是所有的恢复项都一定存在

### 依赖

只使用 python 原生库

### 使用

```
$ python git_extract.py http://example.com/.git/ 一个存在 .git 泄露的网站
$ python git_extract.py example/.git/ 一个本地的 .git 路径
```

### 更新

- 2018-10-3：

    增加对 windows 字体颜色输出的支持，并同步默认背景色，linux 中背景色也修改为与默认同步

- 2019-7-27：

    修复文件缺失、文件格式错误等造成的报错退出  
    修正 urllib2 默认使用系统代理，造成下载缓慢的情况 

- 2020-6-4：
    
    禁止跟随跳转，增加新恢复项 magit wip 模式

- 2020-11-14：
    
    完善文件解析输出详情

### 待做

- 解析其他版本的 git 文件格式，目前支持 version 2
- pack 文件的 ofs_delta, ref_delta 类型文件的重建

### 参考
- [pack 文件格式](https://git-scm.com/docs/pack-format) 
- [index 文件格式](https://git-scm.com/docs/index-format) 
