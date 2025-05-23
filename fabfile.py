'''
>>> pipenv shell
>>> fab deploy
'''

# 命令行执行任务
from fabric import task, Connection

# 自动对交互式命令行的提示做出响应
from invoke import Responder
from _credentials import github_username, github_password


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )
    
    return [username_responder, password_responder]

@task()
def deploy(c):
    
    #ssh 连接设置
    conn = Connection(
        
        host='182.254.229.129', # 替换成你的服务器 IP 地址
        user='root',   # 替换成你的用户名
        connect_kwargs={
            
            "key_filename": "C:/Users/asus/.ssh/id_rsa",  # Windows 路径注意反斜杠或用正斜杠
            # 如果私钥有密码，可以加上 "passphrase": "你的密钥密码"
        }
    )
    
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'django-myblog'

    project_root_path = '~/apps/Django-ZMR-Blog/'
    django_project_subdir = 'MyBlog'

    '''
        每次 ssh 客户端实例执行新的命令是无状态的，即每次都会在服务器根目录执行新的命令，
        而不是在上一次执行的命令所在目录，所以要在同一个目录下连续执行多条命令，需要使用 with 上下文管理器。
    '''

    # 先停止应用
    with conn.cd(supervisor_conf_path):
        
        cmd = 'supervisorctl stop {}'.format(supervisor_program_name)
        conn.run(cmd)

    # 进入项目根目录，从 Git 拉取最新代码
    with conn.cd(project_root_path):
        
        # cmd = 'git pull'
        # responders = _get_github_auth_responders()
        # conn.run(cmd, watchers=responders)
        
        # 使用 SSH，不需要认证器
        cmd = 'git pull'
        conn.run(cmd)

    # 安装依赖，迁移数据库，收集静态文件
    with conn.cd(project_root_path):
        
        conn.run('pipenv install --deploy --ignore-pipfile')
        conn.run(f'pipenv run python {django_project_subdir}/manage.py migrate')
        conn.run(f'pipenv run python {django_project_subdir}/manage.py collectstatic --noinput')

    # 重新启动应用
    with conn.cd(supervisor_conf_path):
        
        cmd = 'supervisorctl start {}'.format(supervisor_program_name)
        conn.run(cmd)