import pytz
from datetime import datetime
from aiocqhttp.exceptions import Error as CQHttpError
from nonebot.plugin import on_command
from nonebot import on_command, CommandSession, SenderRoles

day_map = {0:0, 1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
boss_map = {1:'谢sir', 2:'黄sir', 3:'孙sir', 4:'邓sir', 5:'金sir', 6:'Ni sir', 7:'王sir', 8:'聂sir', 9:'张三'}

def index_add(i):
    i = i + 1
    if i > 9:
        i -= 9
    return i

#group restriction
permit_group = { 912811025 }
banned_people = { 10000, 10001 }
def foo(sender: SenderRoles):
    return sender.is_groupchat and sender.from_group(permit_group) and not sender.sent_by(banned_people)\
    or sender.is_superuser


@on_command('boss', aliases=('排班'), permission=foo)
async def _(session: CommandSession):
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    month = now.month
    day = now.day

    days = 0
    for i in range(month):
        days += day_map[i]
    days += day

    index = days % 9 - 6
    if index <= 0:
        index += 9
    today = f"{now.year}年{now.month}月{now.day}日"
    msg = f'今天是{today} 3天内值班表：\
          \n今天 {index}号：{boss_map[index]}\
          \n明天 {index_add(index)}号：{boss_map[index_add(index)]}\
          \n后天 {index_add(index + 1)}号：{boss_map[index_add(index + 1)]}'

    await session.send(msg)