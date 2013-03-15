#!/usr/bin/env python
# hooks/update
#   verification the user permission for push op
    


import sys
import os
import commands

def task_manage( root_tree, branch ):
    """
    """
    #{{{
    status,output = commands.getstatusoutput(
        'git cat-file -p %s'%(root_tree) )
    if status is not 0:
        print 'Hook Warn:' + output
        return -1;

    status = -1
    output = 'not task_manage file'
    for f in output.split('\n'):
        items = f.split()
        if items[3] != 'task_manage':
            continue
        status,output = commands.getstatusoutput(
            'git cat-file -p %s'%(items[2]) )
        break

    if status is not 0:
        print 'Hook Warn:' + output
        return -1;

    tasks = []
    for item in output.split('\n'):
        if item[0] == '#':
            continue
        tasks.append(item.split(','))
        
    for task in tasks:
        if task[1] == 'open':
            # only master branch can create task
            if branch != 'master':
                continue
            output = commands.getstatusoutput( 
                'git branch %s'%(task[0]) )

        elif task[1] == 'close':
            # only task branch can close task
            if branch == 'master':
                continue
        else:
            print 'Hook Warn: task(%s) status error'%(task[0])

    #}}}


def check_perm( user, branch ):
    """
    check the user permission
    """
    #{{{
    import perm
    try:
        if user in perm.GIT_PERM[0]:
            return True 

        if user in perm.GIT_PERM[branch]:
            return True
        else:
            print 'Hook Error: insufficient permissions'
            return False
    except:
        print 'Hook Error: insufficient permissions'

    return False
    #}}}


def main():
    """
    """
    #{{{
    import pdb
    pdb.set_trace()

    ref = sys.argv[1]
    old_commit = sys.argv[2]
    new_commit = sys.argv[3]
    cur_path = os.getcwd()


    branch = os.path.split(ref)[1]
    user = ''
    root_tree = ''

    # get commit user email
    status,output = commands.getstatusoutput(
        'git cat-file -p %s'%(new_commit) )
    if status is not 0:
        print 'Hook Error:' + output
        return -1;

    committer = 
    for line in output.split('\n'):
        items = line.split()
        if not items:
            continue
        if items[0] == 'tree':
            root_tree = items[1]
        elif items[0] == 'committer':
            user = items[1]

    if not check_perm( user, branch):
        return -1

    task_manage( root_tree )
    return 0
    #}}}


if __name__ == '__main__':
    rt = main()
    sys.exit(rt)


