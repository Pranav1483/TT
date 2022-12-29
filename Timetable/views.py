import mimetypes
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import re
import pandas as pd
import numpy as np
import xlsxwriter
from pathlib import Path
import os

def generate(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render({}, request))


def make(request):
    data = request.POST.get('data', False)
    if data:
        text = re.split(r'\s+', data)
        start = 0
        for idx, i in enumerate(text):
            if len(i) == 6 and i[:2].isalpha() and i[2:].isdigit():
                start = idx
                break
        tx_list = text[start:]
        tt = {}
        flag = 0
        key = val = ''
        for i in range(len(tx_list) - 1):
            if flag == 0:
                if len(tx_list[i]) == 6 and tx_list[i][:2].isalpha() and tx_list[i][2:].isnumeric():
                    val = tx_list[i]
                elif len(tx_list[i]) == 1 and (
                        tx_list[i + 1] == "Science" or tx_list[i + 1] == "Professional" or tx_list[
                    i + 1] == "Engineering" or
                        tx_list[i + 1] == "Humanities"):
                    key = tx_list[i]
                    flag = 1
            if flag == 1:
                tt[key] = val
                flag = 0
        BASE_DIR = Path(__file__).resolve().parent
        df = pd.read_csv(os.path.join(BASE_DIR, "Slotwise.csv"))
        arr = df.to_numpy()

        for i in range(1, len(arr)):
            for j in range(len(arr[0])):
                if len(arr[i][j]) == 1 or len(arr[i][j]) == 5:
                    for x in tt.keys():
                        if x in arr[i][j]:
                            arr[i][j] = tt[x]
                            break
        for i in range(1, len(arr)):
            for j in range(len(arr[0])):
                if len(arr[i][j]) == 1 or len(arr[i][j]) == 5:
                    arr[i][j] = ''
        arr[0][0] = ''
        a = np.array(arr)
        workbook = xlsxwriter.Workbook(os.path.join(BASE_DIR, 'Timetable.xlsx'))
        worksheet = workbook.add_worksheet()
        r = c = 0

        for i in a:
            c = 0
            for j in i:
                worksheet.write(r, c, j)
                c += 1
            r += 1
        workbook.close()
        filename = 'Timetable.xlsx'
        filepath = os.path.join(BASE_DIR, filename)
        path = open(filepath, 'rb')
        mime_type , _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response    
    else:
        return HttpResponseRedirect(reverse('generate'))

