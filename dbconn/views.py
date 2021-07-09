from django.shortcuts import render
import pymysql.connections
import pandas as pd
import matplotlib.pyplot as plt


def mydatacall1():
    mydb = pymysql.Connect(
        host="scadadb.c5lia4zi06l9.us-west-2.rds.amazonaws.com",
        user="dbuser",
        password="GkGk#cyber1204",
        database="scadadb"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM datalog LIMIT 50")
    myresult = mycursor.fetchall()
    datalist = list(myresult)
    df = pd.DataFrame(datalist, columns=['ID', 'CHEFF', 'ENERGY', 'FLOW', 'TIME', 'LEVEL', 'PRESS', 'TEMP'])
    mycursor.close()
    df = round(df, 2)
    return df, datalist


def output(request):
    dfIP, datalistIP = mydatacall1()
    xtime = dfIP['TIME']
    yflow = dfIP['FLOW']
    ytemp = dfIP['ENERGY']
    plt.plot(xtime, yflow)
    plt.xlabel('x values')
    plt.ylabel('y values')
    plt.title('Flow & Temperature Graph')
    plt.legend(['Flow Trend'])
    # save the figure
    fig = plt.gcf()
    fig.savefig('static/images/output.png', dpi=100, bbox_inches='tight')
    plt.show()

    df, datalist = mydatacall1()
    datatohtml = []
    for i in range(df.shape[0]):
        temp = df.loc[i]
        datatohtml.append(dict(temp))
    my_dict = {"arr_users": datatohtml, "img_name": "output.png"}
    return render(request, 'index.html', context=my_dict)


