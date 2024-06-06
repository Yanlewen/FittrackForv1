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

if __name__ == "__main__":
    print(format_input_text('''
Username: F.t
Diets: [Diet(id=10, username=F.t, foodName=6, weight=1000.0, calories=500, createTime=2024-05-11T09:42:04), Diet(id=7, username=F.t, foodName=7, weight=100.0, calories=50, createTime=2024-05-07T10:20:44), Diet(id=6, username=F.t, foodName=9, weight=100.0, calories=50, createTime=2024-05-07T10:19:22), Diet(id=5, username=F.t, foodName=6, weight=700.0, calories=350, createTime=2024-05-07T10:19:15), Diet(id=4, username=F.t, foodName=2, weight=700.0, calories=350, createTime=2024-05-07T10:19:10), Diet(id=3, username=F.t, foodName=2, weight=100.0, calories=50, createTime=2024-05-07T10:19:05), Diet(id=2, username=F.t, foodName=1, weight=300.0, calories=150, createTime=2024-05-07T10:18:54), Diet(id=1, username=F.t, foodName=0, weight=300.0, calories=150, createTime=2024-05-07T10:16:45)]
Sports: [Sport(id=26, username=F.t, GamesName=0, sportsTime=180.0, sportsDistance=3000.0, calories=150000.0, createTime=2024-06-06T12:21:51), Sport(id=25, username=F.t, GamesName=0, sportsTime=240.0, sportsDistance=1212.0, calories=60600.0, createTime=2024-05-11T09:41:10), Sport(id=23, username=F.t, GamesName=0, sportsTime=240.0, sportsDistance=1000.0, calories=50000.0, createTime=2024-05-10T11:49:28), Sport(id=22, username=F.t, GamesName=1, sportsTime=60.0, sportsDistance=1.0, calories=50.0, createTime=2024-05-10T11:43:27), Sport(id=7, username=F.t, GamesName=0, sportsTime=180.0, sportsDistance=3000.0, calories=150000.0, createTime=2024-05-07T11:12:59), Sport(id=6, username=F.t, GamesName=0, sportsTime=180.0, sportsDistance=700.0, calories=35000.0, createTime=2024-05-07T11:12:53)]
HealthCare: [Health(id=10, username=F.t, weight=60.0, bodyFatRate=80.0, heartRate=100, createTime=2024-05-11T09:42:58), Health(id=1, username=F.t, weight=60.0, bodyFatRate=20.1, heartRate=82, createTime=2024-05-10T08:47:54)]'''))