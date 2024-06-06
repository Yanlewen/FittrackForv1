import argparse
import datetime
import os
import google.generativeai as genai

os.environ["http_proxy"]="http://localhost:7890"
os.environ["https_proxy"]="http://localhost:7890"

genai.configure(api_key='AIzaSyB3K8C5uqQTEmkLbQb_EV4OPHPjpmbwxLU')  # 填入自己的api_key

model = genai.GenerativeModel('gemini-1.5-pro')

def get_advice(text):
    text_head = f'''你是一个营养学专家和健身私教，我需要你针对我给定的用户情况给出概述和建议。请你依照下面的用户相关信息（包括前10次运动、饮食、身体指标、每日目标），概述用户的
1. 当前身体状况和健身情况（基于用户的运动、饮食、身体指标、每日目标）。请注意，用户记录的数据可能不全，如果某一天没有记录，不一定代表用户没有进行活动。
2. 给出对用户的建议（包括饮食、运动、生活方式等方面的建议）

请注意以下几点要求：
1. 请使用简洁明了的语言，文本限制在300字以内。
2. 请确保文本内容的合理性和科学性。
3. 如果需要提及用户概况，可以引用用户概况中给出的文本，并且引用用户概况中的日期、记录并加以分析是被鼓励的。
4. 生成的文本将直接展示给用户，请不要在文本中包含其他无关语句（如向用户询问更多信息、向用户展示其他无关内容等），也不要在文本开头回复“好的”之类的冗余句子。
5. 生成的文本应该为纯文本，请不要使用markdown，也不要使用小标题、列表等格式。

今日是{datetime.date.today()}，
下面是用户概况：
'''

    text_end = '''
请依据以上信息，为用户提供概述和建议。'''

    text = text_head + text + text_end

    response = model.generate_content(text)
    return response.text

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help='输入文本路径')
    parser.add_argument('output_path', type=str, help='输出文本路径')

    args = parser.parse_args()
    with open(args.input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    response = get_advice(text)

    with open(args.output_path, 'w', encoding='utf-8') as f:
        f.write(response)
