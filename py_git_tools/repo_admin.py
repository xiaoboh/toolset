#!/usr/bin/env python
# coding=utf-8

# manage repo:
#   create repo
#   del repo
#   list repo
#   show repo

import commands
import os
import sys
import urllib

__version__ = '0.2'


# globle config 
g_cfg_repo_root_path = '/git'
g_cfg_admin_public_key = os.path.expanduser('~/.ssh/id_rsa.pub')
#g_cfg_pubkey_url = 'ftp://anonymous@192.168.1.31/pubkey/'
g_cfg_pubkey_url = "smb://192.168.1.208/Shared Data/pubkey/"
g_cfg_pubkey_dir = '/git/.pubkey'

class RepoManage:
    """
    manage repo
    """
    #{{{
    def __init__(self):
        return

    def create_repo(self, repo_name, repo_desc ):
        """
        create a new repo on current server
        """
        #{{{
        # add a new user
        status,output = commands.getstatusoutput('useradd -m %s'%(repo_name ) )
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))

        os.chdir( '/home/%s'%(repo_name) )
        os.mkdir( './.ssh' )
        file_auth_keys = open( './.ssh/authorized_keys', 'w')
        file_auth_keys.close()
        os.chmod( './.ssh', 0700)
        os.chmod( './.ssh/authorized_keys', 0644)
        status,output = commands.getstatusoutput(
            'chown -R %s:%s ./.ssh'%(repo_name,repo_name) )
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))

        # create git repo
        os.chdir( g_cfg_repo_root_path )
        dir_name = repo_name + ".git"
        os.mkdir( dir_name )
        os.chdir( dir_name )
        status,output = commands.getstatusoutput( 'git init --bare')
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))
        status,output = commands.getstatusoutput( 
            'chown -R %s:%s .'%(repo_name,repo_name))
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))
        status,output = commands.getstatusoutput( 'chmod -R 700 .')
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))

        # add admin to repo user list
        self.add_user_key( repo_name, 'admin'
                          , open(g_cfg_admin_public_key).read())

        # finish the init commit to git repo
        os.chdir( '/tmp')
        if not os.access( './repo_admin', os.F_OK):
            os.mkdir( './repo_admin')
        os.chdir( './repo_admin')
        repo_path = '%s@localhost:%s/%s.git'%(
            repo_name,g_cfg_repo_root_path,repo_name)
        status,output = commands.getstatusoutput( 
            'git clone %s %s'%(repo_path,repo_name) )
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))
        os.chdir( repo_name)
        file_readme = open( './README', 'w')
        file_readme.write(repo_desc)
        file_readme.close()
        status,output = commands.getstatusoutput( 'git add ./README' )
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))

        status,output = commands.getstatusoutput( 'git commit -m "init repo"' )
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))

        status,output = commands.getstatusoutput( 'git push %s master'%(repo_path) )
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))

        os.chdir( '..')

        status,output = commands.getstatusoutput( 'rm -rf ./%s'%(repo_name) )
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))
        #}}}


    def delete_repo(self, repo_name):
        """
        delete a repo
        """
        #{{{
        # delete repo dir
        os.chdir( g_cfg_repo_root_path )
        status,output = commands.getstatusoutput( 'rm -rf %s.git'%(repo_name))
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))

        # delete user
        status,output = commands.getstatusoutput( 'userdel %s'%(repo_name))
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))

        # delete user home dir
        status,output = commands.getstatusoutput( 'rm -rf /home/%s'%(repo_name))
        if status is not 0:
            raise RuntimeError('sh(%d):%s'%(status,output))
        #}}}

    def get_all_repos(self):
        """
        get all repos 
        """
        #{{{
        repos = []
        for f in os.listdir(g_cfg_repo_root_path):
            if not os.path.isfile( f ):
                continue
            (repo,ext) = os.splitext(f)
            if ext is not '.git':
                continue
            repos.append(repo)

        return repos;
        #}}}



    def flush_all_user_key(self, repo_name):
        """
        update all user key to authorized_keys
        """
        #{{{
        dest_dir = '/home/%s/.ssh'%(repo_name)

        file_auth_key = open( os.path.join(dest_dir,'authorized_keys'), 'w')

        os.chdir( dest_dir)
        for f in os.listdir(dest_dir):
            if not os.path.isfile( f ):
                continue
            if os.path.splitext(f)[1] != '.pub':
                continue

            file_user_key = open( os.path.join(dest_dir,f), 'r')
            file_auth_key.write( file_user_key.read() )
            file_user_key.close()

        file_auth_key.close()
        #}}}

    def get_repo_all_users(self, repo_name):
        """
        get a repo`s all users
        """
        #{{{
        dest_dir = '/home/%s/.ssh'%(repo_name)

        os.chdir( dest_dir)
        users = []
        for f in os.listdir(dest_dir):
            if not os.path.isfile( f ):
                continue
            (user,ext) = os.path.splitext(f)
            if ext != '.pub':
                continue
            users.append(user)

        return users;
        #}}}

    def add_user_key(self, repo_name, user, pub_key):
        """
        add a user key to a repo
        """
        #{{{
        dest_dir = '/home/%s/.ssh'%(repo_name)
        user_key = '%s/%s.pub'%(dest_dir,user)
        auth_key = '%s/authorized_keys'%(dest_dir)

        if self.is_hava_user(repo_name, user):
            raise RuntimeError('repo user "%s" is exists'%(user))

        file_user_key = open( user_key, 'w')
        file_user_key.write(pub_key)
        file_user_key.close()

        file_auth_key = open( auth_key, 'a')
        file_auth_key.write(pub_key)
        file_auth_key.close()
        #}}}


    def del_user_key(self, repo_name, user):
        """
        del a user key from a repo
        """
        #{{{
        dest_dir = '/home/%s/.ssh'%(repo_name)
        user_key = '%s/%s.pub'%(dest_dir,user)

        if not self.is_hava_user(repo_name, user):
            raise RuntimeError('repo user "%s" is not exists'%(user))

        status,output = commands.getstatusoutput( 'rm -f %s'%(user_key))
        if status is not 0:
            raise RuntimeError('sh:'+str(status)+output)

        self.flush_all_user_key( repo_name)
        #}}}


    def mod_user_key(self, repo_name, user, pub_key):
        """
        update user repo perm
        """
        #{{{
        dest_dir = '/home/%s/.ssh'%(repo_name)
        user_key = '%s/%s.pub'%(dest_dir,user)
        auth_key = '%s/authorized_keys'%(dest_dir)

        if not self.is_hava_user(repo_name, user):
            raise RuntimeError('repo user "%s" is not exists'%(user))

        file_user_key = open( user_key, 'w')
        file_user_key.write(pub_key)
        file_user_key.close()

        self.flush_all_user_key( repo_name)
        #}}}


    def is_hava_user(self, repo_name, user):
        """
        check the user is in this repo
        """
        dest_dir = '/home/%s/.ssh'%(repo_name)
        user_key = '%s/%s.pub'%(dest_dir,user)

        return os.access( user_key, os.F_OK)

    #}}}

#main
#{{{

import argparse

def get_user_pubkey( user ):
    """
    get a user's pubkey from g_cfg_pubkey_url
    """
    local_key = os.path.join( g_cfg_pubkey_url, user+'.pub' )
    if os.path.isfile(local_key):
        return open(local_key).read()
    elif 'smb' == g_cfg_pubkey_url[:3]:
        return commands.getoutput(
            'smbget -a -q -O "%s%s.pub"'%(g_cfg_pubkey_url,user) )
    else:
        return urllib.urlopen( g_cfg_pubkey_url+ user+'.pub').read()


def main():
    parser = argparse.ArgumentParser(description='git repo manage toolkit')
    #{{{
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument('repo', metavar='RepoName', nargs='*'
                        , help='the git repo name, that you will manage')
    parser.add_argument('--init', action='store_true'
                        , help='init env')
    parser.add_argument('--create', action='store_true'
                        , help='create a new repo')
    parser.add_argument('--delete', action='store_true'
                        , help='delete a exists repo')
    parser.add_argument('--repo-desc', metavar='REPO Desc'
                        ,default='Git Repo'
                        , help='the repo desc')
    parser.add_argument('--list', action='store_true'
                        , help='list all repo')

    parser.add_argument('--add-user', metavar='USER'
                        , help='add a user to repo')
    parser.add_argument('--del-user', metavar='USER'
                        , help='del a user from repo')
    parser.add_argument('--update-user', metavar='USER'
                        , help='update a user key from repo')
    parser.add_argument('--list-user', action='store_true'
                        , help='list all users in repo')
    parser.add_argument('--search-user', metavar='USER'
                        , help='search all repo, is USER in this repo, show it.')

    args = parser.parse_args()
    print args
    #}}}


    rm = RepoManage()
    #{{{
    if args.init:
        os.mkdir(g_cfg_repo_root_path)
        os.mkdir(g_cfg_pubkey_dir)
        print 'Success: INIT ENV'

    elif args.create:
        for repo in args.repo:
            rm.create_repo( repo, args.repo_desc )
            print 'Success: create repo(%s)!'%(repo)

    elif args.delete:
        for repo in args.repo:
            rm.delete_repo( repo )
            print 'Success: delete repo(%s)!'%(repo)

    elif args.list:
        for f in os.listdir(g_cfg_repo_root_path):
            if os.path.splitext(f)[1] != '.git':
                continue
            print 'REPO: %s'%(f)

    elif args.add_user:
        pubkey = get_user_pubkey( args.add_user)
        if not pubkey:
            print 'Failure: cannot get user pub key'
            return

        for repo in args.repo:
            if rm.is_hava_user( repo, args.add_user):
                rm.mod_user_key( repo, args.add_user, pubkey)
                print 'Success: update user(%s) to repo(%s)!'%(args.add_user,repo)
            else:
                rm.add_user_key(repo, args.add_user, pubkey)
                print 'Success: add user(%s) to repo(%s)!'%(args.add_user,repo)

    elif args.del_user:
        for repo in args.repo:
            rm.del_user_key(repo, args.del_user)
            print 'Success: delete user(%s) from repo(%s)!'%(args.add_user,repo)

    elif args.update_user:
        pubkey = get_user_pubkey( args.update_user)
        if not pubkey:
            print 'Failure: cannot get user pub key'
            return

        for f in os.listdir(g_cfg_repo_root_path):
            (repo,ext) = os.path.splitext(f)
            if ext != '.git':
                continue
            try:
                rm.mod_user_key(repo, args.update_user, pubkey)
                print 'Success: update user(%s) to repo(%s)!'%(args.update_user,repo)
            except:
                continue

    elif args.list_user:
        for repo in args.repo:
            print 'repo(%s) user list:'%(repo)
            print rm.get_repo_all_users(repo)

    elif args.search_user:
        for f in os.listdir(g_cfg_repo_root_path):
            (repo,ext) = os.path.splitext(f)
            if ext != '.git':
                continue
            if rm.is_hava_user( repo, args.search_user):
                print 'user(%s) in Repo(%s)'%(args.search_user,repo)

    #}}}

if __name__ == '__main__':
    main()

#}}}
