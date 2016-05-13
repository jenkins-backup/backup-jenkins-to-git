# -*- coding: utf-8 -*-
import os
import logging
'''
    备份JENKINS_HOME到Git：
    1、在JENKINS_HOME_BAK_PATH执行git pull命令
    2、调用ant命令copy JENKINS_HOME_PATH to JENKINS_HOME_BAK_PATH
    3、遍历JENKINS_HOME_BAK_PATH，如果其中的文件或目录不在JENKINS_HOME中，对其执行删除操作
    4、将JENKINS_HOME_BAK_PATH提交到Git
'''

# JENKINS_CONFIG_FILE，存放JENKINS_HOME_BAK_PATH、JENKINS_HOME_PATH等常量
JENKINS_CONFIG_FILE = "jenkins_config.properties"
# BACKUP_BUILD_FILE
BACKUP_BUILD_FILE = "backup.xml"


def backup_jenkins():
    # 从jenkins_config.properties中读取JENKINS_HOME_PATH、JENKINS_HOME_BAK_PATH
    global JENKINS_HOME_BAK_PATH
    global JENKINS_HOME_PATH
    with open(JENKINS_CONFIG_FILE, "r") as f:
        for line in f.readlines():
            tmp = line.split("=", 1)
            if "JENKINS_HOME_PATH" == tmp[0].strip():
                JENKINS_HOME_PATH = tmp[1].strip()
            elif "JENKINS_HOME_BAK_PATH" == tmp[0].strip():
                JENKINS_HOME_BAK_PATH = tmp[1].strip()
            else:
                pass
    os.chdir(JENKINS_HOME_BAK_PATH)
    print "current dir:" + os.getcwd()
    # 1、在JENKINS_HOME_BAK_PATH执行git pull命令
    os.system("git pull")
    # 2、调用ant命令copy JENKINS_HOME_PATH to JENKINS_HOME_BAK_PATH
    os.system("ant -f " + BACKUP_BUILD_FILE)

    # 3、遍历JENKINS_HOME_BAK_PATH，如果其中的文件或目录不在JENKINS_HOME中，对其执行删除操作
    for dirpath, dirs, files in os.walk(JENKINS_HOME_BAK_PATH):
        # 3.1、遍历JENKINS_HOME_BAK_PATH，如果其中的文件不在JENKINS_HOME中，对其执行删除操作
        for f in files:
            # JENKINS_HOME_BAK_PATH下的文件
            bakfile = os.path.join(dirpath, f)
            # 与JENKINS_HOME_BAK_PATH下的文件相对应的JENKINS_HOME_PATH下的文件
            orginfile = os.path.join(dirpath.replace(JENKINS_HOME_BAK_PATH, JENKINS_HOME_PATH), f)

            if ".git" in bakfile:
                # 忽略.git目录及其下的目录或文件
                pass
            else:
                if not os.path.exists(orginfile):
                    # 对不在JENKINS_HOME_PATH下的文件执行删除操作
                    logging.debug(orginfile + " is not exists.")
                    os.system("git rm %s" % bakfile)
        # 3.2、遍历JENKINS_HOME_BAK_PATH，如果其中的目录不在JENKINS_HOME中，对其执行删除操作
        for bak_dir in dirs:
            # JENKINS_HOME_BAK_PATH下的目录
            bakdir = os.path.join(dirpath, bak_dir)
            # 与JENKINS_HOME_BAK_PATH下的目录相对应的JENKINS_HOME_PATH下的目录
            orgindir = os.path.join(dirpath.replace(JENKINS_HOME_BAK_PATH, JENKINS_HOME_PATH), bak_dir)

            if ".git" in bakdir:
                # 忽略.git目录及其下的目录或文件
                pass
            else:
                if not os.path.exists(orgindir):
                    # 对不在JENKINS_HOME_PATH下的目录执行删除操作
                    logging.debug(orgindir + " is not exists.")
                    os.system("git rm -r %s" % bakdir)

    # 4、将JENKINS_HOME_BAK_PATH提交到GIT
    log_message = "sync jenkins config"
    os.system("git add .")
    os.system('git commit -m "%s"' % log_message)
    os.system("git push origin master")

if __name__ == "__main__":
    backup_jenkins()
