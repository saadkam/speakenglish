from django.core.management.base import BaseCommand, CommandError
from speak.models import Lesson
import openpyxl

class Command(BaseCommand):
    help = 'Does some magical work'

    def handle(self, *args, **options):

        # run python manage.py add_data and handle function will be called


        # create a new lesson
        # lesson = Lesson()
        # lesson.Name="Lesson 3"
        # lesson.save()

        # path to excel file, here its in the same folder
        # wb=openpyxl.load_workbook('C:\\Users\\Muhammad Ali\\Desktop\\hq.xlsx')
        # sheet = wb.get_sheet_by_name('MCQS')

        # n=0
        # question=[]
        # a=[]
        # b=[]
        # c=[]
        # d=[]

        # Access cell by sheet['A1'].value where A col and 1 is row


        # also send nudes

        # to set is correct check  for green font color
        # if (sheet['B' + str(i)].font.color.rgb == "FF00B050"):

        #
        # for i in range(1,20):
        #       if sheet['A'+str(i)].value:
        #             question.append(sheet['A'+str(i)].value)
        #             n+=1
        #       else:
        #             break
        #
        # n+=1
        #
        # for i in range(1,n):
        #       if sheet['B'+str(i)].value:
        #             a.append(sheet['B'+str(i)].value)
        #       else:
        #             break
        #
        # for i in range(1,n):
        #       if sheet['C'+str(i)].value:
        #             b.append(sheet['C'+str(i)].value)
        #       else:
        #             break
        #
        # for i in range(1,n):
        #       if sheet['D'+str(i)].value:
        #             c.append(sheet['D'+str(i)].value)
        #       else:
        #             break

        self.stdout.write('There are {} things!')

