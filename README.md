
备份 JENKINS_HOME 到 Git：
1. 在 JENKINS_HOME_BAK_PATH 执行 git pull 命令
2. 调用 ant 命令 copy JENKINS_HOME_PATH 到 JENKINS_HOME_BAK_PATH
3. 遍历 JENKINS_HOME_BAK_PATH，如果其中的文件或目录不在 JENKINS_HOME 中，对其执行删除操作
4. 将 JENKINS_HOME_BAK_PATH 提交到 Git

建议：
> 将任务放到crontab中
> -  01 02 * * * . /etc/profile;/usr/bin/python /data/backup-jenkins-to-git/auto_backup.py>/var/log/backup-jenkins-to-git.log 2>&1
> -  注：/etc/profile中配置了ANT的环境变量
