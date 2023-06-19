from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import time

load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')


#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#
#    if message.content == f'{PREFIX}call':
#        await message.channel.send("callback!")
#
#    if message.content.startswith(f'{PREFIX}hello'):
#        await message.channel.send('Hello!')


try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")


# 웹 페이지에 GET 요청을 보냅니다.
url = 'https://alba.huplux.com/index.php?region=%EB%B6%80%EC%82%B0&q=s'
response = requests.get(url)

# 응답받은 HTML을 파싱합니다.
soup = BeautifulSoup(response.text, 'html.parser')

# 원하는 내용을 추출합니다.
target_div = soup.find('div', class_='container-fluid')
inner_divs = target_div.find_all('div', class_='col-md-offset-1 col-md-10 col-md-offset-1')

# 사용자에게 날짜 수를 입력받고, 해당 수만큼 날짜를 입력받아 배열에 저장합니다.
while True:
    num_dates = str(1)
    if len(num_dates) > 0 and num_dates.isdigit() and 0 < int(num_dates) < 10000:
        break
    else:
        continue
user_input = []
i=1
for _ in range(int(num_dates)):
    while True:
        date = str("0626")
        i=i+1
        month = date[:2]
        day = date[2:]
        if len(date) == 4 and month.isdigit() and day.isdigit() and 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
            date = f"2023-{month.zfill(2)}-{day.zfill(2)}"
            user_input.append(date)
            date = str("0627")
            month = date[:2]
            day = date[2:]
            date = f"2023-{month.zfill(2)}-{day.zfill(2)}"
            user_input.append(date)
            date = str("0628")
            month = date[:2]
            day = date[2:]
            date = f"2023-{month.zfill(2)}-{day.zfill(2)}"
            user_input.append(date)
            break
        else:
            i=i-1
            print("잘못된 형식입니다. 다시 입력해주세요.")

print(f"입력된 날짜: {user_input}")
cnt = 0
while True:
    cnt=cnt+1
    formatted_cnt = f"{cnt:>8}"
    print(f"===['검색 횟수: {formatted_cnt}']===================={user_input}")
    for div in inner_divs:
        if div.find('div', class_='col-md-12', style='background:#f9c667;  padding: 10px 0px;'):
            table = div.find('table', class_='table table-condensed', id='main_s_recruit_table')
            rows = table.find_all('tr')

            headers = []
            data = []

            for row in rows:
                cells = row.find_all('td')
                if cells:
                    row_data = []
                    for cell in cells:
                        row_data.append(cell.text.strip())
                    data.append(row_data)
                else:
                    header_cells = row.find_all('th')
                    for header_cell in header_cells:
                        headers.append(header_cell.text.strip())

            # 데이터를 각각 다른 이름의 배열로 저장하고 출력
            region = []
            date = []
            job_description = []
            working_hours = []
            gender_age = []
            salary = []
            personnel_status = []

            for row_data in data:
                region.append(row_data[0])
                date.append(row_data[1])
                job_description.append(row_data[2])
                working_hours.append(row_data[3])
                gender_age.append(row_data[4])
                salary.append(row_data[5])
                personnel_status.append(row_data[6])

            for i in range(len(date)):
                if date[i][:10] in user_input:
                    embed = discord.Embed(title=":white_sun_small_cloud:대연동 현재 날씨:white_sun_small_cloud:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00b992)
                    embed.set_thumbnail(url="https://cdn-1.webcatalog.io/catalog/naver-weather/naver-weather-icon-filled-256.webp?v=1675613733392")
                    embed.add_field(name="지역\n", value=f"{region[i]}\n", inline=False)
                    embed.add_field(name="날짜\n", value=f"{date[i]}\n", inline=False)
                    embed.add_field(name="모집내용\n", value=f"{job_description[i]}\n", inline=False)
                    embed.add_field(name="근무시간/신청하기\n", value=f"{working_hours[i]}\n", inline=False)
                    embed.add_field(name="성별/연령\n", value=f"{gender_age[i]}\n", inline=False)
                    embed.add_field(name="급여\n", value=f"{salary[i]}\n", inline=False)
                    embed.add_field(name="인원/상태\n", value=f"{personnel_status[i]}\n", inline=False)
                    embed.add_field(name="\n", value=f"\n", inline=False)
                    embed.set_footer(text="Bot Made by. Shus#7777, 자유롭게 이용해 주시면 됩니다.")
                    await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
            time.sleep(1)
    time.sleep(5)
