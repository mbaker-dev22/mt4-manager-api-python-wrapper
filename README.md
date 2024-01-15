# PyMT4ManagerAPI
Python Interface based on MT4 Manager API.

MT4 Manager API is a windows dll which can only be used directly in c/c++ program. With the help of swigwin-3.0.12, I managed to wrap this dll with python. The difficult part is to make the callback function in python called in C/C++. I looked over the internet and came out the solution and Notify_FuncEx in test.py is called when new event comes.

Please copy _MT4ManagerAPI.pyd into C:\Python27\DLLs folder. I don't test it with Python3.

Please use test.py to do testing. For security, I have changed the MT4 server IP and manager account in test.py. Please fill in your MT4 server IP and manager account for testing.

With PyMT4ManagerAPI, you can develop MT4 tools with python.
