
# coding: utf-8

# In[2]:


# Write a procedure, convert_seconds, which takes as input a non-negative 
# number of seconds and returns a string of the form 
# '<integer> hours, <integer> minutes, <number> seconds' but
# where if <integer> is 1 for the number of hours or minutes, 
# then it should be hour/minute. Further, <number> may be an integer
# or decimal, and if it is 1, then it should be followed by second.
# You might need to use int() to turn a decimal into a float depending
# on how you code this. int(3.0) gives 3
#
# Note that English uses the plural when talking about 0 items, so
# it should be "0 minutes".


# In[8]:


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


# In[9]:


print convert_seconds(3661)
#>>> 1 hour, 1 minute, 1 second

print convert_seconds(7325)
#>>> 2 hours, 2 minutes, 5 seconds

print convert_seconds(7261.7)
#>>> 2 hours, 1 minute, 1.7 seconds


# In[ ]:




