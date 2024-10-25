# heychat.py
Python SDK for HeyChat

[![pypi version](https://img.shields.io/pypi/v/khl.py?label=latest&logo=pypi)](https://pypi.org/project/heychat/)
![GitHub last commit](https://img.shields.io/github/last-commit/Edint386/heychat.py?logo=github)
![github stars](https://img.shields.io/github/stars/Edint386/heychat.py?style=social)

[![khl server](https://www.kaiheila.cn/api/v3/badge/guild?guild_id=4735647834857317&style=3)](https://kook.top/D2m28x)
[![heychat server](https://api.heibot.cn/badge/server?text=heychat.py)](https://chat.xiaoheihe.cn/idm3x0tv)

## 安装
```shell
pip install heychat
```



## 最简示例

```python
from heychat import Bot, Message

bot = Bot('your_token')

@bot.command('hello')
async def hello(msg: Message):
    await msg.reply('world!')

bot.run()
```

## 功能示例

### 命令参数处理
```python
from heychat import Bot, Message
from random import randint

bot = Bot('your_token')

@bot.command('roll')
async def roll(msg: Message,max_num):
    # 需先前往小黑盒开发平台为注册指令添加变量
    # 如果没有添加变量单纯输入 /roll 100 也可解析（将在官方关闭type5后失效）
    max_num = int(max_num)
    
    await msg.reply(f"你掷出了{randint(1,max_num)}") # 回复消息
    await msg.ctx.channel.send(f"你掷出了{randint(1,max_num)}") # 发送消息

bot.run()
```

### 获取消息内容
```python
from heychat import Bot, Message

bot = Bot('your_token')

@bot.on_message()
async def on_message(msg: Message):
    # 用户
    print(msg.author.username) # 用户名
    print(msg.author.nickname) # 房间昵称
    print(msg.author.id)       # 用户ID

    # 消息
    print(msg.content)         # 消息内容
    print(msg.msg_timestamp)   # 消息时间戳
    
    # 房间
    print(msg.ctx.guild.id)    # 房间ID
    print(msg.ctx.guild.name)  # 房间名
    
    # 频道
    print(msg.ctx.channel.id)  # 频道ID
    print(msg.ctx.channel.name)# 频道名
    

bot.run()
```

### 上传图片 + 富文本构建
```python
from heychat import Bot, Message, MDMessage, Element

bot = Bot('your_token')

@bot.command('hello')
async def hello(msg: Message):

    img_path = "./img.png"
    img_url = await bot.client.upload(img_path) # 上传图片

    md_msg = MDMessage()
    md_msg.append("这是一段文字\n\n")
    md_msg.append(Element.TEXT("这也是一段文字\n\n"))
    md_msg.append(Element.MENTION("18661718")) # @
    md_msg.append(Element.MENTION("all")) # @全体成员
    md_msg.append(Element.MENTION("here")) # @在线成员
    md_msg.append(Element.IMG("https://chat.max-c.com/attachments/2024-09-15/1835322670233686016_UitVbhhcLf.jpg"))

    # or
    
    md_msg = MDMessage("这是一段文字\n\n",
               Element.TEXT("这也是一段文字\n\n"),
               Element.IMG("https://chat.max-c.com/attachments/2024-09-15/1835322670233686016_UitVbhhcLf.jpg"),
               Element.MENTION("18661718"))

    await msg.reply(md_msg)
```

### 事件处理
```python
from heychat import Bot, EventTypes, GuildMemberEvent, ReactionEvent

bot = Bot('your_token')

@bot.on_event(EventTypes.JOINED_GUILD)
async def on_joined_guild(e: GuildMemberEvent):
    # 获取频道以发送消息
    channel = await bot.client.fetch_channel(e.guild.id, "你的欢迎频道id")
    await channel.send(f"欢迎{e.user.username} 加入 {e.guild.name} !")
    
    
@bot.on_event(EventTypes.LEFT_GUILD)
async def on_left_guild(e: GuildMemberEvent):
    channel = await bot.client.fetch_channel(e.guild.id, "频道id")
    await channel.send(f"{e.user.username} 永远的离开了我们🙏")
    

@bot.on_event(EventTypes.ADDED_REACTION)
async def on_added_reaction(e: ReactionEvent):
    channel = await bot.client.fetch_channel(e.guild_id, e.channel_id)
    await channel.send(f"{e.user_id} 给消息 {e.msg_id} 添加了表情 {e.emoji}")
    
bot.run()
```





## TODO
- ✅ MD构建
- ✅ 从 type5 转移至 type50
- ✅ 事件处理
- ❌ 日志




## 贡献
欢迎大家提供建议以及pr！


## 写在最后的省流
抄的[khl.py](https://github.com/TWT233/khl.py)



