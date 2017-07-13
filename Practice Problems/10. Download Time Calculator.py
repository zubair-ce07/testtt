
# coding: utf-8

# In[1]:


# Write a procedure download_time which takes as inputs a file size, the
# units that file size is given in, bandwidth and the units for
# bandwidth (excluding per second) and returns the time taken to download 
# the file.
# Your answer should be a string in the form
# "<number> hours, <number> minutes, <number> seconds"

# Some information you might find useful is the number of bits
# in kilobits (kb), kilobytes (kB), megabits (Mb), megabytes (MB),
# gigabits (Gb), gigabytes (GB) and terabits (Tb), terabytes (TB).

#print 2 ** 10      # one kilobit, kb
#print 2 ** 10 * 8  # one kilobyte, kB

#print 2 ** 20      # one megabit, Mb
#print 2 ** 20 * 8  # one megabyte, MB

#print 2 ** 30      # one gigabit, Gb
#print 2 ** 30 * 8  # one gigabyte, GB

#print 2 ** 40      # one terabit, Tb
#print 2 ** 40 * 8  # one terabyte, TB

# Often bandwidth is given in megabits (Mb) per second whereas file size 
# is given in megabytes (MB).    


# In[15]:


def BitsConversion(filesize, fileunit):
    if fileunit == "kb":
        filesize *= 2**10
    elif fileunit == "kB":
        filesize *= 2**10*8
    elif fileunit == "Mb":
        filesize *= 2**20
    elif fileunit == "MB":
        filesize *= 2**20*8
    elif fileunit == "Gb":
        filesize *= 2**30
    elif fileunit == "GB":
        filesize *= 2**30*8
    elif fileunit == "Tb":
        filesize *= 2**40
    elif fileunit == "TB":
        filesize *= 2**40*8
    return filesize


# In[21]:


def convert_seconds(number):
    hours = number/3600
    hours = int(hours)
    number -= hours*3600
    mins = number/60
    mins = int(mins)
    number -= mins*60
    h = " hours, "
    m = " minutes, "
    s = " seconds"
    if hours == 1:
        h = " hour, "
    if mins == 1:
        m = " minute, "
    if number == 1:
        s = " second"
    return str(hours) + h + str(mins) + m + str(number) + s


# In[22]:


def download_time(filesize, fileUnit, BandWidth, BandWiddthUnit):
    filesize = BitsConversion(filesize, fileUnit)
    BandWidth = BitsConversion(BandWidth,BandWiddthUnit)
    seconds = filesize/BandWidth
    time = convert_seconds(seconds)
    return time


# In[23]:


print download_time(1024,'kB', 1, 'MB')


# In[24]:


print download_time(1024,'kB', 1, 'MB')
#>>> 0 hours, 0 minutes, 1 second

print download_time(1024,'kB', 1, 'Mb')
#>>> 0 hours, 0 minutes, 8 seconds  # 8.0 seconds is also acceptable

print download_time(13,'GB', 5.6, 'MB')
#>>> 0 hours, 39 minutes, 37.1428571429 seconds

print download_time(13,'GB', 5.6, 'Mb')
#>>> 5 hours, 16 minutes, 57.1428571429 seconds

print download_time(10,'MB', 2, 'kB')
#>>> 1 hour, 25 minutes, 20 seconds  # 20.0 seconds is also acceptable

print download_time(10,'MB', 2, 'kb')
#>>> 11 hours, 22 minutes, 40 seconds  # 40.0 seconds is also acceptable


# In[ ]:




