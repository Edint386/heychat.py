# heychat.py
Python SDK for HeyChat

## 安装
```shell
pip install aiohttp
```

Python小白不会用pypi，所以就手动下载下来然后把heychat文件夹拖到你的项目里吧（）

## 最简示例

```python
from heychat import Bot, Message

bot = Bot('your_token')

@bot.command('hello')
async def hello(msg: Message):
    await msg.reply('world!')

bot.run()
```

## 更多功能
<details>
    <summary> ✅ 命令参数处理</summary>

    from heychat import Bot, Message
    from random import randint
    
    bot = Bot('your_token')

    @bot.command('roll')
    async def hello(msg: Message,max_num):
        # 需先前往小黑盒开发平台为注册指令添加变量
        # 如果没有添加变量单纯输入 /roll 100 也可解析
        max_num = int(max_num)
        await msg.reply(f"你掷出了{randint(1,max_num)}")

    bot.run()

</details>

<details>
    <summary> ❌ 事件处理</summary>

    @bot.on_event(EventType.JOIN_GUILD)
    async def on_join_guild(event: JoinGuildEvent):
        pass

</details>

## 贡献
欢迎大家提供建议以及pr！


## 写在最后的省流
抄的[khl.py](https://github.com/TWT233/khl.py)  
用的ChatGPT  
对了家人们有没有会pypi的教教我怎么发包（） 太蠢了整不明白


