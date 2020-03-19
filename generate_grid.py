import random
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import smtplib
import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from getpass import getpass

color = random.randint(0, 1)
core_spaces = [0]*8 + [1]*8 + [2]*7 + [3]

if color == random.randint(0,1):
    html_message = "Blue has 9, Red has 8, Blue goes first"
    core_spaces.append(0)
else:
    html_message = "Blue has 8, Red has 9, Red goes first"
    core_spaces.append(1)

random.shuffle(core_spaces)

data = np.reshape(np.array(core_spaces),(5,5))

cmap = colors.ListedColormap(['red', 'blue','#d2b48c','black'])
bounds = [-0.5,0.5,1.5,2.5,3.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots()
ax.imshow(data, cmap=cmap, norm=norm)

ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(-.5, 5, 1));
ax.set_yticks(np.arange(-.5, 5, 1));
ax.set_yticklabels([])
ax.set_xticklabels([])

plt.savefig('new_codenames_grid.png')

me = raw_input("Please enter the sender email: ")
my_password = getpass("Type your password and press enter: ")
you1 = raw_input("Please enter email1: ")
you2 = raw_input("Please enter email2: ")
you = ", ".join([you1,you2])

msg = MIMEMultipart('alternative')
msg['Subject'] = "Grid Generation "+dt.datetime.now().strftime('%I:%M %p')
msg['From'] = me
msg['To'] = you

html = '<html><body><p>'+html_message+'</p><br><img src="cid:image1"></body></html>'
part2 = MIMEText(html, 'html')

msg.attach(part2)

fp = open('new_codenames_grid.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
msg.attach(msgImage)

s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login(me, my_password)

s.sendmail(me, [you1,you2], msg.as_string())
s.quit()
