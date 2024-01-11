import discord
import asyncio
import json
from datetime import datetime
import requests
import os
from discord.ext import commands

import keep_alive

keep_alive.keep_alive()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')


@bot.event
async def on_member_join(member):
  guild_id = 1162649237314613270  # Your Guild ID
  channel_id = 1162649237822111820  # Your Channel ID

  guild = bot.get_guild(guild_id)
  channel = guild.get_channel(channel_id)

  if channel is not None:
    inviter = await find_inviter(member)
    if inviter:
      embed = discord.Embed(
          title="New Member Joined",
          description=
          f"{member.mention} has joined the server. Invited by {inviter.mention}",
          color=color)
      await channel.send(embed=embed)
    else:
      await channel.send(
          f'{member.name} has joined the server, but the inviter could not be determined.'
      )
  else:
    print(f'Error: Channel with ID {channel_id} not found.')


async def find_inviter(member):
  async for entry in member.guild.audit_logs(
      action=discord.AuditLogAction.invite_create):
    if entry.target.code == member.guild.me.guild.code:
      return entry.user
  return None


#### C O N F I G ####

ADMIN = 1162649237796966423  #EXECUTIVE ROLE
MM = 1162649237796966421  #Staff role
color = 0xffff00
upi_data_path = 'upi_data.json'
ltc_data_path = 'ltc_data.json'
staff_data_path = 'staff.json'
restrict_data_path = 'restrict.json'
trial_mm_role_id = 1162649237796966421
trial_exch_role_id = 1161339457513992293
restricted_role_id = 1161339790839529623
MM_CATEGORY = 1170314484989055017
EXCH_CATEGORY = 1160963474214625290
trigger_data_path = 'trigger_data.json'

# Load existing trigger data or create an empty dictionary if the file doesn't exist

#### H E L P  C O M M A N D ####


@bot.command(name='client', category='Middleman/Exchanger')
@commands.has_role(MM)
async def give_client_role(ctx, user: discord.User):
  client_role_id = 1162649237796966420

  # Get the client role
  client_role = discord.utils.get(ctx.guild.roles, id=client_role_id)

  if client_role:
    # Assign the client role to the mentioned user
    await user.add_roles(client_role)

    # Send a success message in an embed
    embed = discord.Embed(
        title='Role Added',
        description=f'{user.mention} successfully received the client role.',
        color=color)
    await ctx.send(embed=embed)
  else:
    await ctx.send(f'Client role not found. Please check the role ID.')


command_descriptions = {
    'Middleman': {
        '.bal <ltc-address>': 'Check balance',
        '.calc <equation>': 'Calculator',
        '.dtos': 'Display terms of service',
        '.greet': 'Greet message',
        '.ltc': 'Litecoin command',
        '.Upi': 'UPI command',
        '.pyn': 'Paynote command',
        '.rm <Received Amt>': 'Remove command',
        '.ty': 'Thank you message',
        '.remind <User-Mention>': 'Reminder command'
    },
    'ARs': {
        '.addupi <User-Mention> <Upi-Id>': 'Add UPI command',
        '.addltc <User-Mention> <Ltc-Address>': 'Add Litecoin command',
        '.removeltc <User-Mention>': 'Remove Litecoin command',
        '.removeupi <User-Mention>': 'Remove UPI command',
        '.viewupi <User-Mention>': 'View UPI command',
        '.viewltc <User-Mention>': 'View Litecoin command'
    },
    'Admins': {
        '.addmm <User-Mention> <Nickname> <Max-Limit>':
        'Add Middleman command',
        '.embed <Description>': 'Send Embed Message',
        '.addexch <User-Mention> <Nickname> <Max-Limit>':
        'Add Exchanger command',
        '.removemm <User-Mention>': 'Remove Middleman command',
        '.removeexch <User-Mention>': 'Remove Exchanger command',
        '.restrict <User-Mention>': 'Restrict command',
        '.unrestrict <User-Mention>': 'Unrestrict command'
    }
}


# Use this dictionary to generate help commands
@bot.command(name='help')
async def help_command(ctx, category=None):
  if not category:
    help_embed = discord.Embed(
        title='Bot Commands',
        description='List of available commands by category.',
        color=color)
    for category, commands in command_descriptions.items():
      help_embed.add_field(name=category, value='\n'.join(commands.keys()))
    await ctx.send(embed=help_embed)
  else:
    category = category.capitalize()
    if category in command_descriptions:
      help_embed = discord.Embed(title=f'{category} Commands', color=color)
      for command, description in command_descriptions[category].items():
        help_embed.add_field(name=command, value=description)
      await ctx.send(embed=help_embed)
    else:
      await ctx.send(
          "Invalid category. Use `.help` to see available categories.")


##### LOAD JSON FILES #####

# Load existing LTC data or create an empty dictionary if the file doesn't exist

try:
  with open(trigger_data_path, 'r') as file:
    trigger_data = json.load(file)
except FileNotFoundError:
  trigger_data = {}

try:
  with open(ltc_data_path, 'r') as file:
    ltc_data = json.load(file)
except FileNotFoundError:
  ltc_data = {}

try:
  with open(upi_data_path, 'r') as file:
    upi_data = json.load(file)
except FileNotFoundError:
  upi_data = {}

try:
  with open(staff_data_path, 'r') as file:
    staff_data = json.load(file)
except FileNotFoundError:
  staff_data = []

try:
  with open(restrict_data_path, 'r') as file:
    restrict_data = json.load(file)
except FileNotFoundError:
  restrict_data = {}

##### B O T  S T A R T #####


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  await bot.change_presence(status=discord.Status.online, activity=discord.Game("Made By samir.xd"))

###### M M  C O M M A N D S ######


@bot.command(name='dtos', category='Middleman/Exchanger')
@commands.has_role(MM)
async def dtos(ctx):
  embed = discord.Embed(title='Terms of Service', color=color)
  embed.description = '**Please Check Deal Info, Confirm Your Deal, Discuss Tos & Warranty Of That Product.**'
  await ctx.message.delete()
  await ctx.send(embed=embed)


@bot.command(name='greet', category='Middleman/Exchanger')
@commands.has_role(MM)
async def greet(ctx):
  author_id = ctx.author.id
  embed = discord.Embed(
      description=
      f'**Greetings <@{author_id}>, Will be your Middle Man For The Deal, Kindly Drop Dev ID Of Buyer/Seller**',
      color=color)
  await ctx.message.delete()
  await ctx.send(embed=embed)


@bot.command(name='pyn', category='Middleman/Exchanger')
@commands.has_role(MM)
async def pyn(ctx):
  embed = discord.Embed(title='Paynote Information', color=color)
  embed.description = "> Paynote Is Compulsory To Add While Making Payment, I'f You Forget/Didn't Add We Will Take Penalty.\n\n- FAMPAY : **__I Have Received My Product__**\n- OTHER UPI : **__I Have Authorized This Payment & Received My Product__**\n\n- PENALTY\n - 10 RS"
  embed.set_image(
      url=
      'https://media.discordapp.net/attachments/1020524533209383003/1069262338638749716/PhonePay_-_Copy.png'
  )
  await ctx.message.delete()
  await ctx.send(embed=embed)


@bot.command(name='rm')
@commands.has_role(MM)
async def rm(ctx, amt):
  author_mention = ctx.author.mention
  embed = discord.Embed(
      description=
      f'- {author_mention} Has Received {amt}\n- Continue Your Deal\n- Ping When To Release',
      color=color)
  await ctx.message.delete()
  await ctx.send(embed=embed)


@bot.command(name='calc', category='Middleman/Exchanger')
@commands.has_role(MM)
async def calc(ctx, *, equation):
  result = eval(equation)
  embed = discord.Embed(title='Calculator',
                        description=f'Input: {equation}\nResult: {result}',
                        color=0xffff00)
  await ctx.message.delete()
  await ctx.send(embed=embed)


@bot.command(name='ty', category='Middleman/Exchanger')
@commands.has_role(MM)
async def ty(ctx):
  embed = discord.Embed(title='Thanks!',
                        description='Thanks for trusting/dealing with us!',
                        color=color)
  await ctx.send(embed=embed)
  await ctx.message.delete()


@bot.command()
@commands.has_role(MM)
async def bal(ctx, ltcaddress):
  response = requests.get(
      f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')
  if response.status_code == 200:
    data = response.json()
    balance = data['balance'] / 10**8
    total_balance = data['total_received'] / 10**8
    unconfirmed_balance = data['unconfirmed_balance'] / 10**8
  else:
    await ctx.send(
        "\❌ **Failed to retrieve balance. Please check the Litecoin address.**"
    )
    return

  cg_response = requests.get(
      'https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd'
  )
  if cg_response.status_code == 200:
    usd_price = cg_response.json()['litecoin']['usd']
  else:
    await ctx.send("\❌ **Failed to retrieve the current price of Litecoin.**")
    return

  usd_balance = balance * usd_price
  usd_total_balance = total_balance * usd_price
  usd_unconfirmed_balance = unconfirmed_balance * usd_price

  embed = discord.Embed(title="LTC BALANCE",
                        color=color,
                        description=f"ADDRESS :- **{ltcaddress}**")

  embed.add_field(
      name="Confirmed Balance",
      value=f"LTC  :- **{balance}**\nUSD :- **${usd_balance:.2f}**",
      inline=False)
  embed.add_field(
      name="Unconfirmed Balance",
      value=
      f"LTC  :- **{unconfirmed_balance}**\nUSD :- **${usd_unconfirmed_balance:.2f}**",
      inline=False)
  embed.add_field(
      name="Total Ltc Received",
      value=f"LTC  :- **{total_balance}**\nUSD :- **${usd_total_balance:.2f}**",
      inline=False)

  response_message = await ctx.send(embed=embed)

  await asyncio.sleep(60)
  await response_message.delete()


@bot.command(name='remind', category='Admins')
@commands.has_role(
    MM)  # Make sure to replace admin_role_id with the actual admin role ID
async def remind(ctx, user: discord.User):
  # Prepare the embed
  embed = discord.Embed(
      description=
      "- You Are Requested To Come In The Ticket\n- Ticket : {0}\n- As Soon As Possible"
      .format(ctx.channel.mention),
      color=16776960)

  # Send the message to the mentioned user's DM
  try:
    await user.send(content=user.mention, embed=embed)
    await ctx.send(f"Reminder message sent to {user.mention}'s DMs.")
  except discord.HTTPException:
    await ctx.send(
        f"Failed to send the reminder message to {user.mention}. Please make sure the user has DMs enabled."
    )


@bot.command(name='profile', category='Admins')
@commands.has_role(
    MM)  # Make sure to replace admin_role_id with the actual admin role ID
async def view_profile(ctx, user: discord.User = None):
  if user is None:
    user = ctx.author

  user_id = str(user.id)

  # Search for user data in staff_data list
  user_data = None
  for data in staff_data:
    if data['user_id'] == user_id:
      user_data = data
      break

  if user_data:
    # Prepare the profile embed
    embed = discord.Embed(title=f'Profile of {user}', color=color)
    embed.add_field(name='User ID', value=user_data['user_id'], inline=False)
    embed.add_field(name='User Name',
                    value=user_data['user_name'],
                    inline=False)
    embed.add_field(name='Max Limit',
                    value=user_data['max_limit'],
                    inline=False)
    embed.add_field(name='Date Joined',
                    value=user_data['date_joined'],
                    inline=False)
    embed.add_field(name='MM Deals', value=user_data['mm_deals'], inline=False)
    embed.add_field(name='Exch Deals',
                    value=user_data['exch_deals'],
                    inline=False)

    await ctx.send(embed=embed)
  else:
    # If user data is not found
    embed = discord.Embed(
        title=f'Profile of {user}',
        color=color,
        description=
        f'Data for {user.mention} is not available. Contact an admin for assistance.'
    )
    await ctx.send(embed=embed)


@bot.command(name='ltc', category='Admins')
@commands.has_role(MM)
async def get_ltc(ctx):
  user_id = str(ctx.author.id)
  if user_id in ltc_data:
    ltc_address = ltc_data[user_id]
    embed = discord.Embed(title='', description=f'{ltc_address}', color=color)
    await ctx.message.delete()
    await ctx.send(embed=embed)
    await ctx.send("- **__MUST SEND SS/BLOCKCHAIN AFTER PAYING__**")
  else:
    await ctx.send(
        'You have not set an LTC address yet. Please ask any admin for that.')


@bot.command(name='upi', category='Admins')
@commands.has_role(MM)
async def get_upi(ctx):
  user_id = str(ctx.author.id)
  if user_id in upi_data:
    upi_id = upi_data[user_id]
    embed = discord.Embed(title='UPI ID',
                          description=f'UPI ID : {upi_id}',
                          color=0xffff00)

    await ctx.send(embed=embed)
  else:
    await ctx.send(
        'You have not set a UPI ID yet. Please ask any admin for that.')


##### A R   C O M M A N D S #####

# UPI AR


@bot.command(name='addupi', category='Admins')
@commands.has_role(ADMIN)
async def add_upi(ctx, user: discord.User, upi_id):
  user_id = str(user.id)
  upi_data[user_id] = upi_id
  with open(upi_data_path, 'w') as file:
    json.dump(upi_data, file)
  await ctx.send(f'UPI ID for {user.mention} has been saved.')


@bot.command(name='removeupi', category='Admins')
@commands.has_role(ADMIN)
async def remove_upi(ctx, user: discord.User):
  user_id = str(user.id)
  if user_id in upi_data:
    del upi_data[user_id]
    with open(upi_data_path, 'w') as file:
      json.dump(upi_data, file)
    await ctx.send(f'UPI ID for {user.mention} has been removed.')
  else:
    await ctx.send(f'{user.mention} does not have a UPI ID set.')


@bot.command(name='viewupi', category='Admins')
@commands.has_role(ADMIN)
async def view_upi(ctx, user: discord.User = None):
  if user:
    user_id = str(user.id)
    if user_id in upi_data:
      embed = discord.Embed(title='UPI ID',
                            color=color,
                            description=f'UPI ID: {upi_data[user_id]}')
      await ctx.send(embed=embed)
    else:
      await ctx.send(f'{user.mention} does not have a UPI ID set.')
  else:
    if upi_data:
      embed = discord.Embed(title='UPI IDs', color=color)
      for user_id, upi_id in upi_data.items():
        embed.add_field(name=f'User ID: <@{user_id}>',
                        value=f'UPI ID: {upi_id}',
                        inline=False)
      await ctx.send(embed=embed)
    else:
      await ctx.send('No UPI IDs have been set yet.')


# LTC AR


@bot.command(name='addltc', category='Admins')
@commands.has_role(ADMIN)
async def add(ctx, user: discord.User, ltc_address):
  user_id = str(user.id)
  ltc_data[user_id] = ltc_address
  with open(ltc_data_path, 'w') as file:
    json.dump(ltc_data, file)
  await ctx.send(f'LTC address for {user.mention} has been saved.')


@bot.command(name='removeltc', category='Admins')
@commands.has_role(ADMIN)
async def remove_ltc(ctx, user: discord.User):
  user_id = str(user.id)
  if user_id in ltc_data:
    del ltc_data[user_id]
    with open(ltc_data_path, 'w') as file:
      json.dump(ltc_data, file)
    await ctx.send(f'LTC address for {user.mention} has been removed.')
  else:
    await ctx.send(f'{user.mention} does not have an LTC address set.')


@bot.command(name='viewltc', category='Admins')
@commands.has_role(ADMIN)
async def view_ltc(ctx, user: discord.User = None):
  if user:
    user_id = str(user.id)
    if user_id in ltc_data:
      embed = discord.Embed(title='LTC Address',
                            color=color,
                            description=f'LTC Address: {ltc_data[user_id]}')
      await ctx.send(embed=embed)
    else:
      await ctx.send(f'{user.mention} does not have an LTC address set.')
  else:
    if ltc_data:
      embed = discord.Embed(title='LTC IDs', color=color)
      for user_id, ltc_id in ltc_data.items():
        embed.add_field(name=f'User ID: <@{user_id}>',
                        value=f'LTC : **__{ltc_id}__**',
                        inline=False)
      await ctx.send(embed=embed)
    else:
      await ctx.send('No LTC IDs have been set yet.')


@bot.command(name='deal', category='Admins')
@commands.has_role(
  ADMIN)  # Make sure to replace admin_role_id with the actual admin role ID
async def deal_completed(ctx, category, user: discord.User):
  user_id = str(user.id)

  # Check if the user exists in staff_data
  user_data = None
  for data in staff_data:
    if data['user_id'] == user_id:
      user_data = data
      break

  if user_data:
    if category == 'mm':
      user_data['mm_deals'] += 1
    elif category == 'exch':
      user_data['exch_deals'] += 1
    else:
      await ctx.send(
          f"Invalid category. Use 'mm' for Middleman or 'exch' for Exchanger.")
      return

    # Update staff_data with the new deal count
    with open(staff_data_path, 'w') as file:
      json.dump(staff_data, file)

    # Send DM to the mentioned user
    embed = discord.Embed(
        description=f'You have successfully completed 1 deal as {category}.',
        color=color)
    await user.send(embed=embed)

    await ctx.send(f'{user.mention}\'s deal count has been updated.')
  else:
    await ctx.send(
        f'Data for {user.mention} is not available. Contact an admin for assistance.'
    )


#### A D M I N  C O M M A N D S ####


@bot.command(name='embed', category='Admins')
@commands.has_role(
    ADMIN)  # Make sure to replace admin_role_id with the actual admin role ID
async def send_embed(ctx, *, description):
  embed = discord.Embed(description=description, color=color)
  await ctx.send(embed=embed)
  await ctx.message.delete()


@bot.command(name='addmm', category='Admins')
@commands.has_role(
    ADMIN)  # Make sure to replace admin_role_id with the actual admin role ID
async def add_mm(ctx, user: discord.User, nickname, max_limit):
  user_id = str(user.id)
  user_name = str(user)
  date_joined = datetime.now().strftime("%Y-%m-%d")
  mm_deals = 0
  exch_deals = 0

  # Update user nickname and roles
  try:
    await user.edit(nick=f'{nickname} [{max_limit}]')
    trial_mm_role = discord.utils.get(
        ctx.guild.roles, id=trial_mm_role_id)  # Use the defined variable
    MM2 = discord.utils.get(ctx.guild.roles, id=MM)  # Use the defined variable
    await user.add_roles(trial_mm_role)
    await user.add_roles(MM2)
  except discord.HTTPException:
    await ctx.send(
        f"Failed to update user's nickname or roles. Please ensure the bot has the necessary permissions."
    )

  # Add user data to staff_data list
  staff_data.append({
      'user_id': user_id,
      'user_name': user_name,
      'max_limit': max_limit,
      'date_joined': date_joined,
      'mm_deals': mm_deals,
      'exch_deals': exch_deals
  })

  # Save updated staff data to file
  with open(staff_data_path, 'w') as file:
    json.dump(staff_data, file)

  await ctx.send(
      f'{user.mention} SUCCESSFULLY ADDED as MM with nickname {nickname} [{max_limit}] and received MM role.'
  )


# ADDEXCH


@bot.command(name='addexch', category='Admins')
@commands.has_role(
    ADMIN)  # Make sure to replace admin_role_id with the actual admin role ID
async def add_exch(ctx, user: discord.User, nickname, max_limit):
  user_id = str(user.id)
  user_name = str(user)
  date_joined = datetime.now().strftime("%Y-%m-%d")
  mm_deals = 0
  exch_deals = 0

  # Check if the user mentioned as Trial MM role
  trial_mm_role = discord.utils.get(
      ctx.guild.roles, id=trial_mm_role_id)  # Replace with actual role ID
  MM2 = discord.utils.get(ctx.guild.roles, id=MM)
  if trial_mm_role not in user.roles:
    # User doesn't have Trial MM role, send error message in embed
    embed = discord.Embed(
        title='Error',
        description=
        f'{user.mention} must have Trial MM role to get Trial Exchanger role.',
        color=color)
    await ctx.send(embed=embed)
    return

  # Check if user data already exists
  user_exists = any(data['user_id'] == user_id for data in staff_data)

  if not user_exists:
    # Update user nickname
    try:
      await user.edit(nick=f'{nickname} [{max_limit}]')
    except discord.HTTPException:
      await ctx.send(
          f"Failed to update user's nickname. Please ensure the bot has the necessary permissions."
      )

    # Add user data to staff_data list only if it doesn't already exist
    staff_data.append({
        'user_id': user_id,
        'user_name': user_name,
        'max_limit': max_limit,
        'date_joined': date_joined,
        'mm_deals': mm_deals,
        'exch_deals': exch_deals
    })

    # Save updated staff data to file
    with open(staff_data_path, 'w') as file:
      json.dump(staff_data, file)

  # Give user Trial Exchanger role
  trial_exch_role = discord.utils.get(ctx.guild.roles, id=trial_exch_role_id)
  await user.add_roles(trial_exch_role)
  await user.add_roles(MM2)

  await ctx.send(
      f'{user.mention} SUCCESSFULLY ADDED as Exchange user with nickname {nickname} [{max_limit}] and received Trial Exchanger role.'
  )


@bot.command(name='removemm', category='Admins')
@commands.has_role(ADMIN)  # Replace admin_role_id with actual admin role ID
async def remove_mm(ctx, user: discord.User):
  mm_role = discord.utils.get(
      ctx.guild.roles,
      id=trial_mm_role_id)  # Replace mm_role_id with actual MM role ID
  if mm_role in user.roles:
    await user.remove_roles(mm_role)
    await ctx.send(f'{user.mention} no longer has the Middleman role.')
  else:
    await ctx.send(f'{user.mention} does not have the Middleman role.')


@bot.command(name='removeexch', category='Admins')
@commands.has_role(ADMIN)  # Replace admin_role_id with actual admin role ID
async def remove_exch(ctx, user: discord.User):
  exch_role = discord.utils.get(
      ctx.guild.roles, id=trial_exch_role_id
  )  # Replace exch_role_id with actual Exchanger role ID
  if exch_role in user.roles:
    await user.remove_roles(exch_role)
    await ctx.send(f'{user.mention} no longer has the Exchanger role.')
  else:
    await ctx.send(f'{user.mention} does not have the Exchanger role.')


@bot.command(name='restrict', category='Admins')
@commands.has_role(ADMIN)  # Replace admin_role_id with actual admin role ID
async def restrict_user(ctx, user: discord.User):
  restricted_role = discord.utils.get(
      ctx.guild.roles, id=restricted_role_id
  )  # Replace restricted_role_id with actual Restricted User role ID

  # Store user's roles before restricting
  roles_before_restrict = [
      role.id for role in user.roles if role != restricted_role
  ]

  # Remove all roles except Restricted User role
  await user.edit(roles=[restricted_role])

  # Store data in restrict_data
  restrict_data[str(user.id)] = {
      'roles_before_restrict': roles_before_restrict
  }
  with open(restrict_data_path, 'w') as file:
    json.dump(restrict_data, file)

  await ctx.send(f'{user.mention} has been restricted.')


@bot.command(name='unrestrict', category='Admins')
@commands.has_role(ADMIN)  # Replace admin_role_id with actual admin role ID
async def unrestrict_user(ctx, user: discord.User):
  restricted_role = discord.utils.get(
      ctx.guild.roles, id=restricted_role_id
  )  # Replace restricted_role_id with actual Restricted User role ID

  if restricted_role in user.roles:
    # Restore previous roles
    restrict_info = restrict_data.get(str(user.id))
    if restrict_info:
      roles_before_restrict = restrict_info.get('roles_before_restrict', [])

      roles_to_add = [
          discord.utils.get(ctx.guild.roles, id=role_id)
          for role_id in roles_before_restrict if role_id
      ]
      roles_to_add = [role for role in roles_to_add if role is not None]

      # Add the roles back to the user
      await user.edit(roles=roles_to_add)

      # Remove data from restrict_data
      restrict_data.pop(str(user.id), None)
      with open(restrict_data_path, 'w') as file:
        json.dump(restrict_data, file)

      await ctx.send(f'{user.mention} has been unrestricted.')
    else:
      await ctx.send(f'No restriction data found for {user.mention}.')
  else:
    await ctx.send(f'{user.mention} does not have the Restricted User role.')


@bot.command(name='purge', category='Admins')
@commands.has_role(
    ADMIN)  # Make sure to replace ADMIN with your actual admin role ID
async def purge(ctx, amount: int):
  await ctx.channel.purge(limit=amount + 1)
  await ctx.send(f'Purged {amount} messages.', delete_after=5)


@bot.command(name='addtrigger', category='Admins')
@commands.has_role(ADMIN)  # Replace ADMIN with your actual admin role ID
async def add_trigger(ctx, trigger, *, message):
  trigger_data[trigger] = message

  # Save updated trigger data to file
  with open(trigger_data_path, 'w') as file:
    json.dump(trigger_data, file)

  await ctx.send(f'Trigger "{trigger}" added successfully.')


@bot.command(name='removetrigger', category='Admins')
@commands.has_role(ADMIN)  # Replace ADMIN with your actual admin role ID
async def remove_trigger(ctx, trigger):
  if trigger in trigger_data:
    del trigger_data[trigger]

    # Save updated trigger data to file
    with open(trigger_data_path, 'w') as file:
      json.dump(trigger_data, file)

    await ctx.send(f'Trigger "{trigger}" removed successfully.')
  else:
    await ctx.send(f'Trigger "{trigger}" does not exist.')


@bot.command(name='viewtriggers', category='Admins')
@commands.has_role(ADMIN)  # Replace ADMIN with your actual admin role ID
async def view_triggers(ctx):
  if trigger_data:
    embed = discord.Embed(title='Triggers', color=color)
    for trigger, message in trigger_data.items():
      embed.add_field(name=trigger, value=message, inline=False)
    await ctx.send(embed=embed)
  else:
    await ctx.send('No triggers have been set yet.')


@bot.event
async def on_message(message):
  if message.author.bot:
    return

  content = message.content
  if content.startswith('.'):
    command = content.split()[0]
    trigger = command[1:]  # Remove the leading period

    if trigger in trigger_data:
      response = trigger_data[trigger]

      # Send the response in an embed
      embed = discord.Embed(description=response, color=color)
      await message.channel.send(embed=embed)
      await message.delete()

  await bot.process_commands(message)


# Start the bot
TOKEN = 'MTE5NDg5MTYxMTEzMDMwNjU4MA.G1g61i.6dccVFw1O8jaWmR65P87Dxqq4P5MCc_hboCEM0'
bot.run(TOKEN)
