# heychat.py
Python SDK for HeyChat

[![pypi version](https://img.shields.io/pypi/v/heychat?label=latest&logo=pypi)](https://pypi.org/project/heychat/)
![GitHub last commit](https://img.shields.io/github/last-commit/Edint386/heychat.py?logo=github)
![github stars](https://img.shields.io/github/stars/Edint386/heychat.py?style=social)

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
from heychat import Bot, Message, MDMessage, MDElement

bot = Bot('your_token')

@bot.command('hello')
async def hello(msg: Message):

    img_path = "./img.png"
    img_url = await bot.client.upload(img_path) # 上传图片

    md_msg = MDMessage()
    md_msg.append("这是一段文字\n\n")
    md_msg.append(MDElement.Text("这也是一段文字\n\n"))
    md_msg.append(MDElement.Mention("18661718")) # @
    md_msg.append(MDElement.Mention("all")) # @全体成员
    md_msg.append(MDElement.Mention("here")) # @在线成员
    md_msg.append(MDElement.Image("https://chat.max-c.com/attachments/2024-09-15/1835322670233686016_UitVbhhcLf.jpg"))

    # or
    
    md_msg = MDMessage("这是一段文字\n\n",
               MDElement.Text("这也是一段文字\n\n"),
               MDElement.Image("https://chat.max-c.com/attachments/2024-09-15/1835322670233686016_UitVbhhcLf.jpg"),
               MDElement.Mention("18661718"))

    await msg.reply(md_msg)
```

### 事件处理
```python
from heychat import Bot, EventTypes, GuildMemberEvent, ReactionEvent

bot = Bot('your_token')

@bot.on_event(EventTypes.JOINED_GUILD)
async def on_joined_guild(e: GuildMemberEvent):
    # 获取频道以发送消息
    channel = await bot.client.fetch_channel(e.guild.id, "此处填写你的服务器欢迎频道id")
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

### 卡片消息
```python
from heychat import Bot, Message, EventTypes, BtnClickEvent
from heychat.card import Card, CardMessage, Module, Element, Types
import time

bot = Bot('your_token')

@bot.command('hey')
async def card(msg: Message):
    c = Card()
    c.append(Module.Header('这是一张卡片'))
    c.append(Module.Divider())
    c.append(Module.Section('heychat.py 好用吗？'))
    c.append(Module.ButtonGroup(Element.Button('好用', 'good',Types.Event.SERVER),
                                Element.Button('不好用', 'bad',Types.Event.SERVER,Types.Theme.DEFAULT)))
    cm = CardMessage(c)
    await msg.reply(cm)
    
    # 更多模块
    # 单图
    c.append(Module.ImageGroup('https://imgheybox.max-c.com/web/bbs/2024/11/20/1e73470c46e4bb51fcc06c1c5522a66b.png'))
    # 多图
    c.append(Module.ImageGroup('https://imgheybox.max-c.com/web/bbs/2024/11/20/1e73470c46e4bb51fcc06c1c5522a66b.png',
                          '{图片链接}',
                          '{图片链接}'))
    # 文字 + 图片
    c.append(Module.Section('这是一段文字',Element.Image('https://imgheybox.max-c.com/web/bbs/2024/11/20/1e73470c46e4bb51fcc06c1c5522a66b.png')))
    # 文字 + 按钮
    c.append(Module.Section('这是一段文字',Element.Button('点击跳转','{链接}',Types.Event.LINK)))
    # 文字分割线
    c.append(Module.Divider('这是一条分割线'))
    # 倒计时
    c.append(Module.Countdown(time.time() + 60, Types.CountdownMode.SECOND))
    
    # 多张卡片
    c2 = Card()
    c2.append(Module.Header('这是第二张卡片'))
    cm.append(c2)

# 按钮点击事件示例
@bot.on_event(EventTypes.BTN_CLICKED)
async def on_btn_click(e: BtnClickEvent):
    if e.value == 'good':
        await e.channel.send('开心(*^▽^*)')
    elif e.value == 'bad':
        await e.channel.send('难过(´；ω；`)')
```



## TODO
- ✅ MD构建
- ✅ 从 type5 转移至 type50
- ✅ 事件处理
- ✅ 卡片消息
- ❌ 日志




## 贡献
欢迎大家提供建议以及pr！


## 写在最后的省流
抄的[khl.py](https://github.com/TWT233/khl.py)



