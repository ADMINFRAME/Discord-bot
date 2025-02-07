intents.presences = True  
intents.message_content = True  

keep_alive()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์แล้ว! Logged in as {bot.user}")

# ฟังก์ชันส่งข้อมูลโปรไฟล์
async def send_profile_update(member, is_update=False):
    profile_message = f"""
    **ข้อมูลโปรไฟล์ของ {member.name}:**
    - **ID:** {member.id}
    - **ชื่อผู้ใช้:** {member.name}
    - **สถานะ:** {member.status}
    - **วันที่เข้าร่วมเซิร์ฟเวอร์:** {member.joined_at.strftime('%Y-%m-%d')}
    - **วันที่สร้างบัญชี:** {member.created_at.strftime('%Y-%m-%d')}
    - **ป้าย:** {', '.join([role.name for role in member.roles[1:]]) if len(member.roles) > 1 else 'ไม่มี'}
    - **Avatar URL:** {member.avatar.url if member.avatar else "ไม่มี"}
    """

    channel = bot.get_channel(1337508572740976650)  # เปลี่ยนเป็น Channel ID ของคุณ
    if channel:
        if is_update:
            await channel.send(f"**โปรไฟล์อัพเดทของ {member.name}:**\n{profile_message}")
        else:
            await channel.send(profile_message)

# ติดตามการเข้าร่วมของสมาชิกใหม่
@bot.event
async def on_member_join(member):
    try:
        await send_profile_update(member)
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

# ตรวจจับการอัพเดทโปรไฟล์ของสมาชิก
@bot.event
async def on_member_update(before, after):
    try:
        if before.display_name != after.display_name or before.avatar != after.avatar:
            await send_profile_update(after, True)
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการตรวจจับการอัพเดทโปรไฟล์: {e}")

# คำสั่ง !sv เพื่อประกาศข้อความไปยังห้องที่ระบุ
@bot.command()
async def sv(ctx, *, args):
    try:
        announcement, channel_id = args.rsplit(',', 1)
        channel_id = int(channel_id.strip())
        channel = bot.get_channel(channel_id)

        if channel:
            await channel.send(announcement.strip())
            await ctx.reply(f"✅ การประกาศเสร็จสิ้นในห้อง <#{channel_id}>")
        else:
            await ctx.reply('❌ ไม่พบห้องที่ระบุ!')
    except Exception as e:
        await ctx.reply('❌ รูปแบบคำสั่งผิดพลาด! ใช้รูปแบบ: `!sv คำประกาศ, ID ห้อง`')

# ใส่โทเคนของบอทที่นี่
bot.run(TOKEN)
