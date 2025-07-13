import os
import subprocess
import sys

# === إعدادات المستخدم ===
username = "user"
password = "root"
pin = "123456"
crd_code = input("🔐 أدخل كود Google CRD: ").strip()

# === تحقق أولي ===
if not crd_code:
    print("❌ لم يتم إدخال كود CRD.")
    sys.exit(1)
if len(str(pin)) < 6:
    print("❌ يجب أن يكون الـ PIN مكونًا من 6 أرقام أو أكثر.")
    sys.exit(1)

def run(cmd, shell=False, check=True):
    print(f"🔧 تنفيذ: {cmd}")
    if shell:
        subprocess.run(cmd, shell=True, check=check)
    else:
        subprocess.run(cmd.split(), check=check)

# === تحديث النظام ===
run("apt update && apt upgrade -y", shell=True)

# === إنشاء المستخدم بصلاحيات sudo ===
run(f"useradd -m -s /bin/bash {username}")
run(f"echo '{username}:{password}' | chpasswd")
run(f"adduser {username} sudo")

# === تثبيت Chrome Remote Desktop ===
run("wget https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb")
run("dpkg -i chrome-remote-desktop_current_amd64.deb", shell=True)
run("apt install -f -y", shell=True)

# === تثبيت XFCE + الأدوات ===
run("DEBIAN_FRONTEND=noninteractive apt install -y xfce4 xfce4-terminal dbus-x11 xscreensaver")

# إعداد جلسة XFCE لـ CRD
with open("/etc/chrome-remote-desktop-session", "w") as f:
    f.write("exec /etc/X11/Xsession /usr/bin/xfce4-session\n")

# إزالة GNOME Terminal إذا وجد
run("apt remove -y gnome-terminal", shell=True)

# === تثبيت برامج إضافية ===
run("apt install -y telegram-desktop qbittorrent")
run("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
run("dpkg -i google-chrome-stable_current_amd64.deb", shell=True)
run("apt install -f -y", shell=True)

# === autostart لرابط YouTube ===
autostart_path = f"/home/{username}/.config/autostart"
os.makedirs(autostart_path, exist_ok=True)

desktop_entry = '''[Desktop Entry]
Type=Application
Name=YouTubeAuto
Exec=google-chrome https://www.youtube.com/@jor3a-ti9niya/videos
X-GNOME-Autostart-enabled=true
'''
with open(f"{autostart_path}/youtube.desktop", "w") as f:
    f.write(desktop_entry)

run(f"chown -R {username}:{username} /home/{username}/.config", shell=True)

# === إضافة المستخدم لمجموعة CRD ===
run(f"adduser {username} chrome-remote-desktop")

# === تشغيل الأمر النهائي لربط CRD بالحساب ===
run(f"su - {username} -c '{crd_code} --pin={pin}'", shell=True)

# === بدء الخدمة ===
run("systemctl enable chrome-remote-desktop", shell=True)
run("systemctl start chrome-remote-desktop", shell=True)

# === ملخص ===
print("\n✅✅✅ تم التثبيت بنجاح!")
print(f"👤 اسم المستخدم: {username}")
print(f"🔐 كلمة المرور: {password}")
print(f"🔓 PIN لتسجيل الدخول: {pin}")
