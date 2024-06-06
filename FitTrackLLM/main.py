import argparse
import datetime
import os
import google.generativeai as genai

os.environ["http_proxy"]="http://localhost:7890"
os.environ["https_proxy"]="http://localhost:7890"

genai.configure(api_key='AIzaSyB3K8C5uqQTEmkLbQb_EV4OPHPjpmbwxLU')  # 填入自己的api_key

model = genai.GenerativeModel('gemini-1.5-pro')


def get_advice(text):
    text_head = f'''你是一个营养学专家和健身私教，我需要你针对我给定的用户情况给出概述和建议。请你依照下面的用户相关信息（包括前10次运动、饮食、身体指标），概述用户的
1. 当前身体状况和健身情况（基于用户的运动、饮食、身体指标）。请注意，用户记录的数据可能不全，如果某一天没有记录，不一定代表用户没有进行活动。
2. 给出对用户的建议（包括饮食、运动、生活方式等方面的建议），以及对用户每日目标（距离、时间、消耗卡路里）的设置建议。

请注意以下几点要求：
1. 请使用简洁明了的语言，文本限制在300字以内。
2. 请确保文本内容的合理性和科学性。
3. 如果需要提及用户概况，可以引用用户概况中给出的文本，并且引用用户概况中的日期、记录并加以分析是被鼓励的。
4. 生成的文本将直接展示给用户，请不要在文本中包含其他无关语句（如向用户询问更多信息、向用户展示其他无关内容等），也不要在文本开头回复“好的”之类的冗余句子。
5. 生成的文本应该为纯文本，请不要使用markdown，也不要使用小标题、列表等格式。建议按照给定的要求分为两段。
6. 请务必注意：你不得索要其他类型的数据！你只能基于给出的类型的数据进行分析和建议，不应建议用户增加其他类型的数据。不得出现如“建议您记录每次运动后的休息时间”等句子。
7. 你应当以私教的身份进行回答，请以“以下是您的智能建议：”等句子开头，不要以“根据您提供的记录”开头。
8. 请记住，你已经是一个资深的营养师和健身私教。不得在文本最后提出“建议您向有经验的私教咨询”等句子。

今日是{datetime.date.today()}，
下面是用户概况：
'''

    text_end = '''
请依据以上信息，为用户提供概述和建议。'''

    text = text_head + text + text_end

    response = model.generate_content(text)
    return response.text

import re
def format_input_text(text):
    text = text.strip()
    text_list = text.split("\n")
    diet = "饮食：\n| 食物 | 重量 | 摄入卡路里 | 时间 |\n| --- | --- | --- | --- |\n"
    tmp = re.findall("Diets: \[(.*)\]",text_list[1])[0]
    tmp = re.findall("Diet\(id=.*?, username=.*?, foodName=(.*?), weight=(.*?), calories=(.*?), createTime=(.*?)\)",tmp)
    for i in tmp:
        try:
            food = [
                '米饭', '肉类', '蛋类', '豆类', '蔬菜水果', '面食', '果汁', '牛奶', '可乐、雪碧', '水', '咖啡'
            ][int(i[0])]
            unit = [
                'g', 'g', 'g', 'g', 'g', 'g', 'ml', 'ml', 'ml', 'ml', 'ml'
            ][int(i[0])]
            diet += f"| {food} | {i[1]}{unit} | {i[2]}kCal | {i[3]} |\n"
        except Exception as e:
            print(f"无法读取条目：{i}")

    sports = "运动：\n| 运动 | 时长 | 距离 | 消耗卡路里 | 时间 |\n| --- | --- | --- | --- | --- |\n"
    tmp = re.findall("Sports: \[(.*)\]",text_list[2])[0]
    tmp = re.findall("Sport\(id=.*?, username=.*?, GamesName=(.*?), sportsTime=(.*?), sportsDistance=(.*?), calories=(.*?), createTime=(.*?)\)",tmp)
    for i in tmp:
        try:
            sport = [
                '跑步', '骑行', '游泳', '举铁'
            ][int(i[0])]
            sports += f"| {sport} | {float(i[1])/60} 分钟 | {float(i[2])/1000} km | {i[3]}kCal | {i[4]} |\n"
        except Exception as e:
            print(f"无法读取条目：{i}")

    body = "身体指标：\n| 体重 | 体脂率 | 心率 | 时间 |\n| --- | --- | --- | --- |\n"
    tmp = re.findall("HealthCare: \[(.*)\]",text_list[3])[0]
    tmp = re.findall("Health\(id=.*?, username=.*?, weight=(.*?), bodyFatRate=(.*?), heartRate=(.*?), createTime=(.*?)\)",tmp)
    for i in tmp:

        try:
            body += f"| {i[0]}kg | {i[1]}% | {i[2]}bpm | {i[3]} |\n"
        except Exception as e:
            print(f"无法读取条目：{i}")

    return f'''{diet}\n{sports}\n{body}'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help='输入文本路径')
    parser.add_argument('output_path', type=str, help='输出文本路径')


    args = parser.parse_args()
    with open(args.input_path, 'r', encoding='utf-8') as f:
        text = format_input_text(f.read())

    response = get_advice(text)

    with open(args.output_path, 'w', encoding='utf-8') as f:
        f.write(response)
    exit(0)
