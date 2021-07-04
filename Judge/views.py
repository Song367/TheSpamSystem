from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import time
import re
from machine_learning.contentFilterByMachine import predict_content
from Judge.models import EmailContent, EmailUser
import hashlib
from django.db.models import Q


def Md5Pwd(s):
    md = hashlib.md5()  # 创建md5对象
    md.update(s.encode(encoding='utf-8'))
    return md.hexdigest()


def main(request):
    if request.method == "GET":
        return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        name = request.POST.get("username")
        pwd = request.POST.get("passwd")
        try:
            user_obj = EmailUser.objects.get(user=name)

            if user_obj.password == Md5Pwd(pwd):
                return JsonResponse({"status": 1})
            return JsonResponse({"error": "密码错误", "status": 0})
        except:
            return JsonResponse({"error": "用户不存在", "status": 0})
    elif request.method == "GET":
        return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        name = request.POST.get("username")
        pwd = request.POST.get("passwd")
        user_obj = EmailUser.objects.filter(user=name)
        if not name or not pwd:
            return render(request, 'register.html', {"error": "用户名或者密码不能为空"})
        if len(user_obj) > 0:
            return render(request, 'register.html', {"error": "用户已存在"})
        try:
            h = Md5Pwd(pwd)
            EmailUser.objects.create(user=name, password=h)
            return render(request, 'login.html')
        except:
            return render(request, 'register.html', {"error": "服务器错误"})
    elif request.method == "GET":
        return render(request, 'register.html')


def insert_email(request):
    if request.method == "POST":
        send = request.POST.get("username")
        receive = request.POST.get("receiver")
        title = request.POST.get("title")
        content = request.POST.get("content")
        if send == receive and send != "" and receive!= "":
            return JsonResponse({"result": "", "error": "接收人不能为自己" , "status":0})
        if receive == "":
            return JsonResponse({"result": "", "error": "接收人不能为空", "status": 0})
        if title == "":
            return JsonResponse({"result": "", "error": "标题不能为空", "status": 0})
        if content == "":
            return JsonResponse({"result": "spam", "error": "传入数据为空", "status": 0})
        x = predict_content(content)
        print(x)
        y = 0
        if x[0] == "spam":
            y = 1
        e_objs = EmailUser.objects.filter(user=receive)
        if len(e_objs) == 0:
            return JsonResponse({"result": "", "error": "接收人不存在", "status": 0})
        try:
            EmailContent.objects.create(send_user=send, receive=receive, content=content, category=y, email_title=title)
            return JsonResponse({"status": 1, "error": ""})

        except:
            return JsonResponse({"status": 0, "error": "出入数据出错"})


def delete_email(request):
    if request.method == "POST":
        email_id = request.POST.get("email_id")
        email_obj = EmailContent.objects.get(id=email_id)
        if email_obj:
            email_obj.delete()
            return JsonResponse({"status": 0, "error": ""})
        return JsonResponse({"status": 1, "error": "邮件不存在"})


def query_email_send(request):
    if request.method == "POST":
        send = request.POST.get("username")
        email_objs = list(EmailContent.objects.filter(send_user=send).values())
        for v in email_objs:
            v["datatime"] = v["datatime"].strftime("%Y-%m-%d %H:%M:%S")
        return JsonResponse({"result": email_objs, "error": ""})


def query_email_spam(request):
    if request.method == "POST":
        receive = request.POST.get("username")
        email_objs = list(EmailContent.objects.filter(receive=receive, category=1).values())
        for v in email_objs:
            v["datatime"] = v["datatime"].strftime("%Y-%m-%d %H:%M:%S")
        return JsonResponse({"result": email_objs, "error": ""})


def query_email_receive(request):
    if request.method == "POST":
        receive = request.POST.get("username")
        email_objs = list(EmailContent.objects.filter(receive=receive, category=0).values())
        for v in email_objs:
            v["datatime"] = v["datatime"].strftime("%Y-%m-%d %H:%M:%S")
        return JsonResponse({"result": email_objs, "error": ""})


def hua_tu(request):
    if request.method == "GET":
        from pyecharts import options as opts
        from pyecharts.charts import PictorialBar
        from pyecharts.globals import SymbolType

        location = ["spam", "normal"]
        values = [0, 0]
        username = request.GET.get("username")
        print(username)
        if username != "":
            spam_objs = len(EmailContent.objects.filter(receive=username, category=1))
            normal_objs = len(EmailContent.objects.filter(receive=username, category=0))
            values[0] = spam_objs
            values[1] = normal_objs
        c = (
            PictorialBar()
                .add_xaxis(location)
                .add_yaxis(
                "result",
                values,
                label_opts=opts.LabelOpts(is_show=False),
                symbol_size=18,
                symbol_repeat="fixed",
                symbol_offset=[0, 0],
                is_symbol_clip=True,
                symbol=SymbolType.ROUND_RECT,
            )
                .reversal_axis()
                .set_global_opts(
                title_opts=opts.TitleOpts(title="（个人邮件分类数量对比）"),
                xaxis_opts=opts.AxisOpts(is_show=False),
                yaxis_opts=opts.AxisOpts(
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(opacity=0)
                    ),
                ),
            )
        )

        html_buttom = '''
        <a style="text-decoration: none;color: black;display: block;margin: 60px auto;height: 40px;width: 100px;text-align: center;font-size: 20px;font-weight: bold;line-height: 40px;text-align: center;background-color: #CCFFFF;border-radius: 3px;
    " href="/main/">
        返回首页
    </a>
        '''
        # print(c.render_embed())
        x = c.render_embed().replace("\n", "")
        j = x.index("title")
        # print(x)
        match = re.compile("(.*?)title")
        match2 = re.compile("(.*?)<body>")

        l = match.search(x)

        # print(x[y.span()[1]-7:y.span()[1]])
        # s = x[:l.span()[1] - 8] + html + x[l.span()[1] - 7:]
        # s = s.replace("\n", "")
        # print(s)
        y = match2.search(x)

        b = x[:y.span()[1]] + html_buttom + x[y.span()[1]:]
        # print(b)

        return JsonResponse({"res": b})


def system_index(req):
    return render(req, 'spam.html')


def deal_content(request):
    if request.method == "POST":
        content = request.POST.get("content", "")
        if content == "":
            return JsonResponse({"result": "spam", "error": "", "code": 1})
        x = predict_content(content)
        print(x)
        return JsonResponse({"result": x[0], "error": "", "code": 0})


def every_month_day_emails(request):
    import pyecharts.options as opts
    from pyecharts.charts import Bar3D
    uname = request.GET.get("username")
    # uname = "Song367"
    print(uname)
    month = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
    ]
    days = [str(i) for i in range(32)]

    data = []

    for m in range(1, 13):
        obj = EmailContent.objects.filter(Q(send_user=uname) | Q(receive=uname), datatime__month=m)
        dd = {}
        for o in obj:
            for d in days:
                x = str(d)
                if o.datatime.strftime("%d") == x:
                    if x in dd:
                        dd[x] += 1
                    else:
                        dd[x] = 1
        for k, v in dd.items():
            data.append([m, int(k), v])

    c = (
        Bar3D(init_opts=opts.InitOpts(width="1600px", height="500px"))
            .add(
            series_name="一年内每个月每天邮件处理量",
            data=data,
            xaxis3d_opts=opts.Axis3DOpts(type_="category", data=month, name="月"),
            yaxis3d_opts=opts.Axis3DOpts(type_="category", data=days, name="日"),
            zaxis3d_opts=opts.Axis3DOpts(type_="value", name="数量"),
        )
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                max_=20,
                range_color=[
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ],
            )
        )
    )
    html_buttom = '''
            <a style="text-decoration: none;color: black;display: block;margin: 60px auto;height: 40px;width: 100px;text-align: center;font-size: 20px;font-weight: bold;line-height: 40px;text-align: center;background-color: #CCFFFF;border-radius: 3px;
        " href="/main/">
            返回首页
        </a>
            '''
    x = c.render_embed().replace("\n", "")
    j = x.index("title")
    match2 = re.compile("(.*?)<body>")
    y = match2.search(x)
    b = x[:y.span()[1]] + html_buttom + x[y.span()[1]:]

    return JsonResponse({"res": b})
