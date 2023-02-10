#!/bin/sh
# Update the version for of a repo
if echo "$1" | grep '^PR[0-9]\+' > /dev/null
then
    repo_dir=/home/adamva/repo/CMPUT404-project-socialdistribution/api/health
    cd $repo_dir
    PR=$1
    RL=`git rev-list --count HEAD` # get the "version" number
    set `git log -1 --date=iso-strict | awk '/^commit/ { print $2; } /^Date:/ { print $2 }'`
    VERS="SD 0.$RL $2 $1 $PR"
    echo $VERS
    read -p "Looks ok before updating ver.txt? " yorn
    case $yorn in
        [Yy]* )
            echo "updating $repo_dir/ver.txt"
            GT=`git rev-parse --show-toplevel` # git top directory of wherever you are
            GT=$repo_dir
            echo "$VERS" > "$repo_dir/ver.txt"
            break
            ;;
        * )
            echo "no action taken"
            break
            ;;
    esac
    cd -
else
    echo "usage: upd-ver <PRnnnn>"
fi
