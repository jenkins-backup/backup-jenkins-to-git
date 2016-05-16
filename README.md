备份Jenkins的配置到Git

> 将任务放到crontab中
> -  01 02 * * * . /etc/profile;/usr/bin/python /data/backup-jenkins-to-git/auto_backup.py>/var/log/backup-jenkins-to-git.log 2>&1
> -  注：/etc/profile中配置了ANT的环境变量