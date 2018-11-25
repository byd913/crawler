
WEB_PATH=$(cd `dirname $0`; pwd)
INI_PATH=view.ini
ret_val=0
LOG_PATH="log"
status_file="uwsgi.status"
pid_file="uwsgi.pid"


function rm_if_exist() {
    name=$1
    if [ -e $name ]
    then
        rm -f $name
    fi
}


function start() {
    if [ ! -d ${LOG_PATH} ]; then
        mkdir ${LOG_PATH}
    fi

    local ret_val=0
    uwsgi ${INI_PATH}
    sleep 2
    if [ -e ${status_file} ]; then
        echo "Started Web Server Succ"
    else
        ret_val=1
        echo "Started Web Server Failed"
    fi
    return $ret_val
}


function stop() {
    echo "Stopped "`cat $pid_file`
    uwsgi --stop ${pid_file}
    ret_val=$?
    rm_if_exist ${status_file}
    rm_if_exist ${pid_file}
}


case $1 in
    start)
        start
        ret_val=$?
        ;;
    stop)
        stop
        ret_val=$?
        ;;
    restart)
        stop
        start
        ret_val=$?
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart}"
        ret_val=2
esac
exit $ret_val

