# heychat.py
Python SDK for HeyChat

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
    <summary> ✅ 获取基础信息</summary>

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

</details>
<details>
    <summary> ✅ MD构建</summary>
    
    import MDMessage
    @bot.on_message()
    async def on_message(msg: Message):

        img_path = "./img.png"
        await upload_img(img_path)

        md_msg = MDMessage()
        md_msg.apeend("这是一段文字")
        md_msg.append(Element.TEXT("这也是一段文字"))
        md_msg.append(Element.MENTION("18661718")) # @
        md_msg.append(Element.IMG("https://chat.max-c.com/attachments/2024-09-15/1835322670233686016_UitVbhhcLf.jpg"))

        # or
        
        md_msg = MDMessage("这是一段文字",
                            Element.TEXT("这也是一段文字"),
                            Element.IMG("https://chat.max-c.com/attachments/2024-09-15/1835322670233686016_UitVbhhcLf.jpg"),
                            Element.MENTION("18661718"))
        

        await msg.reply(md_msg)

</details>


<details>
    <summary> ✅ 支持更多指令变量类型</summary>

    已经看了，觉得不需要适配现在的够用了，如果有具体需求欢迎提出

</details>


<details>
    <summary> ✅ 从type5转移至type50</summary>

    （划掉）等什么时候官方把type5删了再写（划掉）已经写了


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


