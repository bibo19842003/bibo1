import configparser
import time
import re
import pandas as pd
import csv
import xlsxwriter


# Config
cf = configparser.ConfigParser()
cf.read('gerrit-log-ana.config')

options = dict(timeout=60)
options.update(cf.items('Log'))

log_tpye = options['type']
log_path = options['path']
log_export = options['export']


# 解析单行日志
def httpd_parse(line):
    dic = {}
    try:
        parse_result = pattern.match(line)
        # ip处理
        ip = parse_result.group("ip")
        if ip.strip() == '-' or ip.strip() == "":
            return False
        dic['ip'] = ip

        # username 处理
        username = parse_result.group("username")
        dic['username'] = username

        # 状态码处理
        status = parse_result.group("status")
        dic['status'] = status

        # 时间处理
        time = parse_result.group("time")
        time = time.replace("+0800", "")
        dic['time'] = time

        # request处理
        request = parse_result.group("request")
        dic['request'] = request

        if "git-upload-pack" in request:
            git_upload_pack = "y"
        else:
            git_upload_pack = "n"
        dic['git-upload-pack'] = git_upload_pack

        if "git-receive-pack" in request:
            git_receive_pack = "y"
        else:
            git_receive_pack = "n"
        dic['git-receive-pack'] = git_receive_pack

        # content_length 处理
        content_length = parse_result.group("content_length")
        dic['content_length'] = content_length

        # latency 处理
        latency = parse_result.group("latency")
        dic['latency'] = latency

        # user_agent处理
        user_agent = parse_result.group("user_agent")
        if "git/" in user_agent:
            git_version = user_agent
        else:
            git_version = "not git"
        dic['git_version'] = git_version

        return dic

    except:
        return False


# 数据统计
def data_count(header, data_list):
    df = pd.DataFrame(data_list)
    for item in header:
        item = pd.value_counts(df[item])
        print(item)
        print("")
    


# 数据导出
def export_data(header, data_list):
    # csv 数据导出，比 excel 少数据统计
    if ( log_export == "csv" ):
        with open('result.csv', 'w', encoding='utf-8', newline='') as fileline:
            writer = csv.DictWriter(fileline, header)
            writer.writeheader()
            writer.writerows(data_list)

    # excel 数据导出，比 csv 多数据统计
    elif ( log_export == "xlsx" ):
        workbook = xlsxwriter.Workbook('result.xlsx')
        worksheet = workbook.add_worksheet("all_data")

        # all_data 写入
        # head 写入
        row = 0
        col = 0
        bold = workbook.add_format({'bold': True})
        for head in header:
            worksheet.write(row, col, head, bold)
            col += 1

        # 数据写入
        for row_num, row_data in enumerate(data_list):
            for col_num, col_data in enumerate(row_data.values()):
                worksheet.write(row_num + 1, col_num, col_data)

        # 数据统计写入
        df = pd.DataFrame(data_list)
        for item in header:
            worksheet = workbook.add_worksheet( item + "_count" )
            item_data = pd.value_counts(df[item]).reset_index()
            row = 0
            worksheet.write(row, 0, item, bold)
            worksheet.write(row, 1, "count", bold)
            for row_data in item_data.values:
                worksheet.write(row + 1, 0, row_data[0])
                worksheet.write(row + 1, 1, row_data[1])
                row += 1

        workbook.close()



# 工作 工作 工作
# 数据处理
if ( log_tpye == "httpd" ):
    pattern = re.compile(r'(?P<ip>.*?) \[(?P<http_thread>.*?)\] (?P<daiyong1>.*?) (?P<username>.*?) \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>.*?) (?P<content_length>.*?) (?P<latency>.*?) (?P<referer>.*?) "(?P<user_agent>.*?)"')
    header = ['ip', 'username', 'status', 'time', 'request', 'git-upload-pack', 'git-receive-pack', 'content_length', 'latency', 'git_version']

    i = 0
    data_list = []
    error_data_list = []

    with open(log_path) as f:
        for line in f:
            line = line.strip()
            result = httpd_parse(line)
            if result:  # 正确数据添加到data_list列表中
                data_list.append(result)
            else:
                error_data_list.append(line)  # 错误数据添加到error_data_list列表中
            i += 1

    print("total lines: ", i)
    print("error lines:", len(error_data_list))
    print("correct lines", len(data_list))

    

elif ( log_path == "sshd" ):
    pass
elif ( log_path == "delete" ):
    pass
elif ( log_path == "gc" ):
    pass
elif ( log_path == "replication" ):
    pass
elif ( log_path == "error" ):
    pass


# 数据统计
# data_count(header, data_list)

# 数据导出
export_data(header, data_list)



# python3
# https://www.cnblogs.com/ssgeek/p/12119657.html
# xlsxwriter.readthedocs.org
