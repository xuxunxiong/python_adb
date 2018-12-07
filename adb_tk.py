import threading
import time
import os
import yaml
from adb.ab_python import starttime_app, adb_monkey, huoqushebeizhuangtai, caijicpu, getnencun
from ulit.py_excel import qidongceshi, getcpu
from ulit.log import user_log as LOG
from ulit.log import logger

conf_path = os.path.join(os.path.abspath('.'), 'conf\config.yaml')

with open(conf_path, 'r', encoding='utf-8') as fp:
    conf_dict = yaml.load(fp)


@logger('启动app时间测试')
def qidongapp():
    start_tim = []
    cishu = []
    status_shebei = huoqushebeizhuangtai()
    if status_shebei == 'device':
        try:
            packname = conf_dict['packname']
            activty = conf_dict['activty']
            times = conf_dict['times']
        except:
            LOG.info('获取不到测试数据，请检查！')
        if times <= 1 or len(packname) <= 1:
            LOG.info('包命或者包名activity不能为空')
        else:
            if times <= 1:
                LOG.info('次数不能为空')
            else:
                sum = 0
                for i in range(int(times)):
                    start_time = starttime_app(packagename=packname, packagenameactivicy=activty)
                    start_tim.append(int(start_time[1]))

                    cishu.append(i)
                    if start_time is None:
                        break
                    LOG.info('第%s次启动时间：%s' % (i + 1, start_time[1]))
                    sum += int(start_time[1])
                qidongceshi(cishu=cishu, start=start_tim)
                LOG.info('测试报告已经生成，请到当前目录查看')
                LOG.info('测试已经完成')
    else:
        LOG.info('设备连接异常')


@logger('monkey测试')
def monkey_app():
    status_shebei = huoqushebeizhuangtai()
    if status_shebei == 'device':
        try:
            packname = conf_dict['packname']
            seed = conf_dict['seed']
            throttle = conf_dict['throttle']
            touch = conf_dict['touch']
            motion = conf_dict['motion']
            majornav = conf_dict['majornav']
            appswitch = conf_dict['appswitch']
            trackball = conf_dict['trackball']
            syskeys = conf_dict['syskeys']
            count = conf_dict['count']
            log_file_path = conf_dict['log_file_path']

            if len(packname) <= 5:
                LOG.info('请正确填写包名')
            if int(touch) + int(motion) + int(trackball) + int(majornav) + int(syskeys) + int(appswitch) > 100:
                LOG.info('您输入的所有的事件的比例和不能超过100')
            adb_monkey(packagename=packname, s_num=seed, throttle=throttle, pct_touch=touch, pct_motion=motion,
                       pct_trackball=trackball, pct_nav=majornav, pct_syskeys=syskeys, pct_appswitch=appswitch,
                       num=count,
                       logfilepath=log_file_path)
        except:
            LOG.info('monkey 测试出错，原因:%s' % Exception)
    else:
        LOG.info('设备连接异常 请重新连接设备!')


@logger('cpu占用率，内存的测试')
def cpu_app():
    status_shebei = huoqushebeizhuangtai()
    if status_shebei == 'device':
        xingneng_bao = 'com.lalamove.'
        xing = 20
        if len(xingneng_bao) <= 5:
            LOG.info('包名必须真实有效')
        cishu_list = []
        cpu_list = []
        pass_list = []
        i = 0
        for i in range(int(xing)):
            nen_cun = getnencun(xingneng_bao)
            # rescv, send, liulang_sum = liulang(xingneng_bao)
            cpu_caiji = caijicpu(xingneng_bao)
            pass_list.append(int(nen_cun[:-1]))
            LOG.info('第%s次：Pass：%s' % (i, nen_cun))
            cpu_list.append(int(cpu_caiji.split('%')[0]))
            LOG.info('第%s次：CPU占用率：%s' % (i, cpu_caiji))
            # total_list.append(int(liulang_sum))
            # rescv_list.append(int(rescv))
            # send_list.append(int(send))
            # LOG.info('第%s次：总流量：%sk,上传流量:%sk,下载流量：%sk' % (i, liulang_sum, rescv, send))
            i += 1
            cishu_list.append(int(i))
        getcpu(cishu=cishu_list, start_cpu=cpu_list, Pass_list=pass_list)
        LOG.info('测试完成')
    else:
        LOG.info('测试的设备必须正常连接，请注意')


@logger('启用线程来启动测试！采集启动耗时，cpu占用率，内存')
def teread_cpu():
    t3 = threading.Thread(target=qidongapp, args=())
    t3.start()
    t3.join()
    if not t3.is_alive():
        time.sleep(5)
        # threads = []
        # t1 = threading.Thread(target=monkey_app, args=())
        # t2 = threading.Thread(target=cpu_app, args=())
        # threads.append(t1)
        # threads.append(t2)
        # for th in threads:
        #     th.start()
        #     th.join()
        monkey_app()
        time.sleep(5)
        cpu_app()
    LOG.info('线程执行完成')


if __name__ == '__main__':
    LOG.info('测试小程序开始启动！测试开启！')
    try:
        status_shebei = huoqushebeizhuangtai()
        if status_shebei == 'device':
            teread_cpu()
        else:
            LOG('设备未连接或者连接异常!目前连接状态:%s' % status_shebei)
    except Exception as e:
        LOG.info('测试异常，原因：%s' % e)
